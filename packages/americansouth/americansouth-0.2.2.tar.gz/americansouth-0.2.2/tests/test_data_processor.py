from americansouth.data_processor import DataProcessor
from americansouth.repository import JsonRepository


def test_process_data_basic(sample_data_file):
    repository = JsonRepository(str(sample_data_file))
    processor = DataProcessor(repository)
    records = processor.process_data()

    assert len(records) == 2
    assert records[0][1] == 79.13
    assert records[1][1] == 85.33


def test_process_data_daily_usage(complex_data_file):
    repository = JsonRepository(str(complex_data_file))
    processor = DataProcessor(repository)
    records = processor.process_data()

    amounts = [record[1] for record in records]
    assert amounts == [50.0, 75.0, 100.0]

    prev_amount = 0
    daily_usages = []
    for record in records:
        amount = record[1]
        daily_usages.append(amount - prev_amount)
        prev_amount = amount

    assert daily_usages == [50.0, 25.0, 25.0]
