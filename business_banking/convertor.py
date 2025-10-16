# import csv
# import re
#
# LOG_FILE = 'logs/app.log'  # Adjust path if needed
# CSV_FILE = 'logs.csv'
#
# def parse_log_line(line):
#
#     pattern = r'^\[(.*?)\] (\w+) in (\w+): (.*)$'
#     match = re.match(pattern, line)
#     if match:
#         timestamp, level, module, message = match.groups()
#         return timestamp, level, module, message
#     else:
#         return None, None, None, line.strip()
#
# def convert_log_to_csv(log_file=LOG_FILE, csv_file=CSV_FILE):
#     with open(log_file, 'r', encoding='utf-8') as log_f, \
#          open(csv_file, 'w', newline='', encoding='utf-8') as csv_f:
#
#         writer = csv.writer(csv_f)
#         writer.writerow(['Timestamp', 'Level', 'Module', 'Message'])
#
#         for line in log_f:
#             timestamp, level, module, message = parse_log_line(line)
#             writer.writerow([timestamp, level, module, message])
#
# if __name__ == '__main__':
#     convert_log_to_csv()
#     print(f"Converted log file '{LOG_FILE}' to CSV file '{CSV_FILE}'")

import csv
import re
import os

LOG_FILE = 'logs/app.log'  # Adjust path if needed
CSV_FILE = 'logs.csv'

def parse_log_line(line):
    pattern = r'^\[(.*?)\] (\w+) in (\w+): (.*)$'
    match = re.match(pattern, line)
    if match:
        timestamp, level, module, message = match.groups()
        return timestamp, level, module, message
    else:
        return None, None, None, line.strip()

def convert_log_to_csv(log_file=LOG_FILE, csv_file=CSV_FILE):
    file_exists = os.path.exists(csv_file)

    with open(log_file, 'r', encoding='utf-8') as log_f, \
         open(csv_file, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csv_f:

        writer = csv.writer(csv_f)

        # Write header only if file is new
        if not file_exists:
            writer.writerow(['Timestamp', 'Level', 'Module', 'Message'])

        for line in log_f:
            timestamp, level, module, message = parse_log_line(line)
            writer.writerow([timestamp, level, module, message])

if __name__ == '__main__':
    convert_log_to_csv()
    print(f"Converted log file '{LOG_FILE}' to CSV file '{CSV_FILE}'")
