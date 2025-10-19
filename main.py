import argparse
import csv
from collections import defaultdict
from tabulate import tabulate

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--report', required=True, choices=['average-rating'])
    return parser.parse_args()

def read_csv_files(file_paths):
    data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['price'] = float(row['price'])
                row['rating'] = float(row['rating'])
                data.append(row)
    return data

def generate_average_rating_report(data):
    brand_ratings = defaultdict(list)
    for row in data:
        brand_ratings[row['brand']].append(row['rating'])
    
    report = [
        {'brand': brand, 'average_rating': sum(ratings) / len(ratings)}
        for brand, ratings in brand_ratings.items()
    ]
    report.sort(key=lambda x: x['average_rating'], reverse=True)
    return report

def display_report(report, report_type):
    if report_type == 'average-rating':
        headers = ['Brand', 'Average Rating']
        table = [[item['brand'], item['average_rating']] for item in report]
        print(tabulate(table, headers=headers, tablefmt='grid', floatfmt=".2f"))

def main():
    args = parse_arguments()
    data = read_csv_files(args.files)
    report_functions = {
        'average-rating': generate_average_rating_report
    }
    if args.report in report_functions:
        report = report_functions[args.report](data)
        display_report(report, args.report)
    else:
        print(f"Unknown report type: {args.report}")

if __name__ == '__main__':
    main()
