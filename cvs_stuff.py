import csv
import os

filename = "settings.csv"

def file_exists(filename):
    return os.path.isfile(filename)

def add_record(filename, record):
    # Append a record to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(record)
    print(f"Record {record} added.")

def remove_record(filename, condition_func):
    # Remove records that meet the condition specified by condition_func
    if not file_exists(filename):
        print("File does not exist.")
        return

    records_to_keep = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        records_to_keep = [record for record in reader if not condition_func(record)]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(records_to_keep)
    print("Records removed if condition met.")

def display_records(filename):
    if not file_exists(filename):
        print("File does not exist.")
        return

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for record in reader:
            print(record)

def read_record(filename):
    if not file_exists(filename):
        print("File does not exist.")
        return

    with open(filename, mode='r') as file:
        a = []
        reader = csv.reader(file)
        for record in reader:
            a.append(record)
    return a