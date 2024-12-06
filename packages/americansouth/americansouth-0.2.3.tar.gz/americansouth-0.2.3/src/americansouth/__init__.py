import sys

from .cli import parse_args
from .data_processor import DataProcessor
from .display import DisplayManager
from .repository import JsonRepository


def main() -> int:
    args = parse_args()

    repository = JsonRepository(args.data_file)
    processor = DataProcessor(repository)
    display = DisplayManager()

    records = processor.process_data()

    display.print_headers()

    prev_amount: float = 0.0
    for record in records:
        display.print_record(record, prev_amount)
        prev_amount = record[1]

    return 0


if __name__ == "__main__":
    sys.exit(main())
