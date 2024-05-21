import argparse
import sys
from functools import partial
from typing import Iterator

import uniplot

plot = partial(uniplot.plot, height=15, width=80)


def skip_comments(inp: Iterator[str]) -> Iterator[str]:
    for line in inp:
        if not line.startswith("#"):
            yield line


def load_data(fnames: list[str]) -> Iterator[dict[str, list[float]]]:
    for fname in fnames:
        with open(fname) as inp:
            lines = skip_comments(inp)
            header = [h.strip() for h in next(lines).split(",")]
            cols: list[list[float]] = [[] for _ in header]
            for line in lines:
                for d, v in zip(cols, line.split(",")):
                    d.append(float(v))

        yield {h: v for h, v in zip(header, cols)}


def plot_data(keys: list[str], data: list[dict[str, list[float]]]) -> None:
    for key in keys:
        plot([d[key] for d in data], title=key, lines=True, color=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="+", type=argparse.FileType("r"))
    parser.add_argument("--keys", type=str)

    args = parser.parse_args()
    if not args.keys:
        print("Please provide keys to plot")
        sys.exit(1)

    keys = [key.strip() for key in args.keys.split(",")]
    data = list(load_data([f.name for f in args.input]))
    plot_data(keys, data)
