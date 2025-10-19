import pytest
from io import StringIO
import csv
import os
from collections import defaultdict
from main import read_csv_files, generate_average_rating_report, display_report

@pytest.fixture
def sample_csv(tmp_path):
    data = [
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'}
    ]
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
        writer.writeheader()
        writer.writerows(data)
    return str(file_path)

def test_read_csv_files(sample_csv):
    data = read_csv_files([sample_csv])
    assert len(data) == 3
    assert data[0]['brand'] == 'apple'
    assert data[0]['rating'] == 4.9
    assert data[1]['price'] == 1199.0

@pytest.fixture
def sample_data():
    return [
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': 999.0, 'rating': 4.9},
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': 1199.0, 'rating': 4.8},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': 199.0, 'rating': 4.6},
        {'name': 'iphone 14', 'brand': 'apple', 'price': 799.0, 'rating': 4.8}
    ]

def test_generate_average_rating_report(sample_data):
    report = generate_average_rating_report(sample_data)
    assert len(report) == 3
    assert report[0]['brand'] == 'apple'
    assert report[0]['average_rating'] == pytest.approx(4.85)
    assert report[1]['brand'] == 'samsung'
    assert report[1]['average_rating'] == 4.8
    assert report[2]['brand'] == 'xiaomi'
    assert report[2]['average_rating'] == 4.6

def test_display_report(capsys, sample_data):
    report = generate_average_rating_report(sample_data)
    display_report(report, 'average-rating')
    captured = capsys.readouterr()
    expected = (
        "+---------+------------------+\n"
        "| Brand   |   Average Rating |\n"
        "+=========+==================+\n"
        "| apple   |             4.85 |\n"
        "+---------+------------------+\n"
        "| samsung |             4.80 |\n"
        "+---------+------------------+\n"
        "| xiaomi  |             4.60 |\n"
        "+---------+------------------+\n"
    )
    assert captured.out == expected