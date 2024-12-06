import json
from pathlib import Path

import pytest


@pytest.fixture
def sample_data_file(tmp_path) -> Path:
    data = [
        {
            "date": "2024-11-13",
            "amount": 79.13,
            "amountUnits": "GB",
            "total": 400,
            "totalUnits": "GB",
            "overage": 0,
            "overageUnits": "GB",
            "scrapedAt": "2024-11-13T06:17:28.611Z",
        },
        {
            "date": "2024-11-14",
            "amount": 85.33,
            "amountUnits": "GB",
            "total": 400,
            "totalUnits": "GB",
            "overage": 0,
            "overageUnits": "GB",
            "scrapedAt": "2024-11-14T04:07:23.819Z",
        },
    ]

    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps(data))
    return data_file


@pytest.fixture
def complex_data_file(tmp_path) -> Path:
    data = [
        {
            "date": "2024-11-13",
            "amount": 50.0,
            "amountUnits": "GB",
            "total": 400,
            "totalUnits": "GB",
            "overage": 0,
            "overageUnits": "GB",
            "scrapedAt": "2024-11-13T00:00:00Z",
        },
        {
            "date": "2024-11-14",
            "amount": 75.0,
            "amountUnits": "GB",
            "total": 400,
            "totalUnits": "GB",
            "overage": 0,
            "overageUnits": "GB",
            "scrapedAt": "2024-11-14T00:00:00Z",
        },
        {
            "date": "2024-11-15",
            "amount": 100.0,
            "amountUnits": "GB",
            "total": 400,
            "totalUnits": "GB",
            "overage": 0,
            "overageUnits": "GB",
            "scrapedAt": "2024-11-15T00:00:00Z",
        },
    ]

    data_file = tmp_path / "complex_data.json"
    data_file.write_text(json.dumps(data))
    return data_file
