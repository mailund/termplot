import argparse
import sys
from enum import unique
from functools import partial
from typing import Iterator

import uniplot
from xxlimited import Str

plot = partial(uniplot.plot, height=15, width=80)


def skip_comments(inp: Iterator[str]) -> Iterator[str]:
    for line in inp:
        if not line.startswith("#"):
            yield line


def load_data(fnames: list[str]) -> Iterator[dict[str, list[str]]]:
    for fname in fnames:
        with open(fname) as inp:
            lines = skip_comments(inp)
            header = [h.strip() for h in next(lines).split(",")]
            cols: list[list[Str()]] = [[] for _ in header]
            for line in lines:
                for d, v in zip(cols, line.split(",")):
                    d.append(v.strip())

        data = {h: v for h, v in zip(header, cols)}
        assert len(cols) > 0
        data["__file__"] = [fname] * len(cols[0])
        yield data


def merge_data(data: Iterator[dict[str, list[float]]]) -> dict[str, list[float]]:
    merged = {}
    for d in data:
        for k, v in d.items():
            if k not in merged:
                merged[k] = v
            else:
                merged[k].extend(v)
    return merged


def split(keys: list[str], values: list[float]) -> list[list[float]]:
    unique_keys = set(keys)
    split_values = []
    for key in unique_keys:
        split_values.append([float(v) for k, v in zip(keys, values) if k == key])
    return split_values


def plot_data(
    keys: list[str], data: dict[str, list[float]], col: str | None = None
) -> None:
    for key in keys:
        vals = (
            [float(v) for v in data[key]]
            if col is None
            else split(data[col], data[key])
        )
        print(len(vals), len(vals[0]))
        plot(vals, title=key, lines=True, color=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="+", type=argparse.FileType("r"))
    parser.add_argument("--keys", type=str)

    args = parser.parse_args()
    if not args.keys:
        print("Please provide keys to plot")
        sys.exit(1)

    keys = [key.strip() for key in args.keys.split(",")]
    data = merge_data(load_data([f.name for f in args.input]))
    plot_data(keys, data, "sample")
