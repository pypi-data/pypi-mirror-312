import json
import logging
import os
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def pickle_save(path, name, obj):
    with open(path + name, "wb") as f:
        pickle.dump(obj, f)
    return obj


def pickle_load(path, name):
    with open(path + name, "rb") as f:
        obj = pickle.load(f)
    return obj


def iqr_remove_outliers(data, q1_set=25, q3_set=75):
    """https://en.wikipedia.org/wiki/Interquartile_range"""
    q1 = np.percentile(data, q1_set)
    q3 = np.percentile(data, q3_set)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data >= lower_bound) & (data <= upper_bound)]


def filter_array(arr):
    invalid_mask = np.logical_or(np.isnan(arr), np.isinf(arr))
    return arr[~invalid_mask]


def set_df_print(max_rows=None, max_cols=None, width=None, max_colwidth=None):
    pd.set_option("display.max_rows", max_rows)
    pd.set_option("display.max_columns", max_cols)
    pd.set_option("display.width", width)
    pd.set_option("max_colwidth", max_colwidth)


def url_download(url, data_dir, fname=None, chunk_size=1024):
    """Downloads file from url to data_dir.

    Parameters
    ----------
    url : str
        URL of file to download.
    data_dir : str
        Downloaded in this directory (needs to exist).
    fname : str, optional
        File name, by default None.
    chunk_size : int, optional
        Chunk size for downloading, by default 1024

    References
    [1] - https://gist.github.com/yanqd0/c13ed29e29432e3cf3e7c38467f42f51

    Returns
    -------
    str
        File name.

    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if fname is None:
        fname = data_dir + url.split("/")[-1]
    else:
        fname = data_dir + fname

    if Path(fname).is_file() is not True:
        logging.info(f"Started downloading from {url} ...")

        resp = requests.get(url, stream=True)
        total = int(resp.headers.get("content-length", 0))

        with open(fname, "wb") as file, tqdm(
            desc=fname, total=total, unit="iB", unit_scale=True, unit_divisor=1024
        ) as bar:
            for data in resp.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)
    else:
        logging.info(f"Already downloaded {fname}!")

    return fname


def load_dataset_variables(file_dir):
    json_path = file_dir + "/variables.json"

    with open(json_path, "r") as j:
        contents = json.loads(j.read())

    return contents


def get_file_size(f, convert_to="gb"):
    byte_size = os.path.getsize(f)

    if convert_to.lower() == "gb":
        return byte_size / 1024 / 1024 / 1024
    elif convert_to.lower() == "mb":
        return byte_size / 1024 / 1024
    elif convert_to.lower() == "kb":
        return byte_size / 1024
    else:
        return byte_size


def get_ms_time():
    return time.time_ns() // 1_000_000
