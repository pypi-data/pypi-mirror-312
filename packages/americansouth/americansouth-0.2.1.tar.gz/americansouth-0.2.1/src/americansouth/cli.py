import argparse
import dataclasses
import typing


@dataclasses.dataclass
class CliArgs:
    data_file: str


def parse_args() -> CliArgs:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("data_file", help="Path to data.json file")
    args: typing.Any = parser.parse_args()
    return CliArgs(data_file=args.data_file)
