from __future__ import annotations

import os
import shutil
from functools import cached_property
from pathlib import Path
from typing import Generator
from uuid import uuid4

import numpy as np
import pandas as pd
from numpy import ndarray

from sdgx.data_connectors.dataframe_connector import DataFrameConnector
from sdgx.data_loader import DataLoader

DEFAULT_CACHE_ROOT = os.getenv("SDG_NDARRAY_CACHE_ROOT", "./.ndarry_cache")


class NDArrayLoader:
    """
    Cache ndarray in disk, allow slice and random access.

    Support for storing two-dimensional data by columns.
    """

    def __init__(self, cache_root: str | Path = DEFAULT_CACHE_ROOT, save_to_file=True) -> None:
        self.store_index = 0
        self.cache_root = Path(cache_root).expanduser().resolve()
        self.save_to_file = save_to_file
        if save_to_file:
            self.cache_root.mkdir(exist_ok=True, parents=True)
        else:
            self.ndarray_list = []

    @staticmethod
    def get_auto_save(raw_data) -> NDArrayLoader:
        save_to_file = True
        if isinstance(raw_data, pd.DataFrame) or (
            isinstance(raw_data, DataLoader)
            and isinstance(raw_data.data_connector, DataFrameConnector)
        ):
            save_to_file = False
        return NDArrayLoader(save_to_file=save_to_file)

    @cached_property
    def subdir(self) -> str:
        """
        Prevent collision of cache files.
        """
        return uuid4().hex

    @cached_property
    def cache_dir(self) -> Path:
        """Cache directory for storing ndarray."""

        return self.cache_root / self.subdir

    def _get_cache_filename(self, index: int) -> Path:
        return self.cache_dir / f"{index}.npy"

    def store(self, ndarray: ndarray):
        """
        Spliting and storing columns of ndarry to disk, one by one.
        """
        if self.save_to_file:
            self.cache_dir.mkdir(exist_ok=True, parents=True)
            for ndarray in np.split(ndarray, indices_or_sections=ndarray.shape[1], axis=1):
                np.save(self._get_cache_filename(self.store_index), ndarray)
                self.store_index += 1
        else:
            for ndarray in np.split(ndarray, indices_or_sections=ndarray.shape[1], axis=1):
                self.ndarray_list.append(ndarray)
                self.store_index += 1

    def load(self, index: int) -> ndarray:
        """
        Load ndarray from disk by index of column.
        """
        if self.save_to_file:
            return np.load(self._get_cache_filename(int(index)))
        else:
            return self.ndarray_list[index]

    def cleanup(self):
        if self.save_to_file:
            try:
                shutil.rmtree(self.cache_dir, ignore_errors=True)
            except AttributeError:
                pass
        self.store_index = 0

    def iter(self) -> Generator[ndarray, None, None]:
        for i in range(self.store_index):
            yield self.load(i)

    def get_all(self) -> ndarray:
        return np.concatenate([array for array in self.iter()], axis=1)

    @cached_property
    def __shape_0(self):
        return self.load(0).shape[0]

    @property
    def shape(self) -> tuple[int, int]:
        return self.__shape_0, self.store_index

    def __len__(self):
        return self.shape[0]

    def __getitem__(self, key: int | slice | tuple[int | slice, int | slice]):
        if not isinstance(key, tuple):
            # NDArrayLoader[:], NDArrayLoader[1]
            return np.concatenate([self.load(i)[key] for i in range(self.store_index)], axis=1)
        else:
            # NDArrayLoader[:, 1], NDArrayLoader[1, :], NDArrayLoader[:, :]
            x_slice, y_slice = key
            if not isinstance(y_slice, slice):
                # NDArrayLoader[:, 1]
                return self.load(y_slice)[x_slice].squeeze(axis=1)
            if not isinstance(x_slice, slice):
                # NDArrayLoader[1, :]
                return np.concatenate(
                    [
                        self.load(i)[x_slice]
                        for i in range(
                            y_slice.start or 0,
                            min(y_slice.stop or self.store_index, self.store_index),
                            y_slice.step or 1,
                        )
                    ],
                )
            else:
                # NDArrayLoader[:, :]
                return np.concatenate(
                    [
                        self.load(i)[x_slice]
                        for i in range(
                            y_slice.start or 0,
                            min(y_slice.stop or self.store_index, self.store_index),
                            y_slice.step or 1,
                        )
                    ],
                    axis=1,
                )

    def __del__(self):
        self.cleanup()
