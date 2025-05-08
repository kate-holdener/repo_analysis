import csv
from collections import defaultdict
from datetime import datetime

def process_csv(file_path):
    summary = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'hours': set()}))

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row

        for row in reader:
            if len(row) < 2:
                continue  # Skip rows that don't have at least timestamp and email

            timestamp = row[0]
            email = row[1]

            try:
                # Extract the date and hour from the timestamp
                dt = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S')
                date = dt.date()
                hour = dt.strftime('%H')

                summary[email][str(date)]['count'] += 1
                summary[email][str(date)]['hours'].add(hour)
            except ValueError:
                print(f"Skipping invalid timestamp: {timestamp}")

    return summary

def write_summary_to_csv(summary, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Email", "Date", "Row Count", "Hours"])
        for email, dates in summary.items():
            for date, data in sorted(dates.items()):
                hours_list = ",".join(sorted(data['hours']))
                writer.writerow([email, date, data['count'], hours_list])

def main():
    input_file_path = input("Enter the path to the CSV file: ")
    output_file_path = input("Enter the path to the output CSV file: ")
    summary = process_csv(input_file_path)
    write_summary_to_csv(summary, output_file_path)
    print(f"Summary written to {output_file_path}")

if __name__ == "__main__":
    main()

