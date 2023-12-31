import pandas as pd
import argparse as ap
from datetime import date, timedelta, datetime
import pyexcel as pe
import openpyxl
from file_setup import get_dir, file_check
from statistics import obtain_data, visualize

def cli_parse():
    parser = ap.ArgumentParser(description="A CLI program to track your daily mood.")

    parser.add_argument("-e", "--enter", action="store_true", help="Input your daily mood.")
    parser.add_argument("-l", "--late", action="store_true", help="Use if you are submitting past 11:59pm.")
    parser.add_argument("-i", "--important", action="store_true", help="Mark as an important day.")
    parser.add_argument("-d", "--enter-date", type=str, help="Enter data for a specific day (yyyymmdd).", default=None)
    parser.add_argument("-t", "--test", action="store_true", help="fuck you")

    args = parser.parse_args()

    if args.test:
        sprdsht_dir = get_dir()
        file_check(sprdsht_dir)
        dates, moods = obtain_data(30, sprdsht_dir)
        visualize(dates, moods)

    if args.enter or args.enter_date:
        late = args.late
        importance = args.important
        input_date = args.enter_date
        mood = get_mood()
        desc = get_desc()
        sprdsht_dir = get_dir()
        file_check(sprdsht_dir)
        write_mood(mood, late, desc, importance, input_date, sprdsht_dir)
        if args.enter_date:
            sort_data(sprdsht_dir)

def sort_data(sprdsht_dir: str):
    wb = openpyxl.load_workbook(sprdsht_dir)
    ws = wb.active

    excel_data = []
    for row in ws.iter_rows(min_row = 2, values_only = True):
        excel_data.append(row)

    excel_data.sort(key=lambda row:datetime.strptime(row[0], '%Y-%m-%d'))

    ws.delete_rows(2, ws.max_row-1)

    for row in excel_data:
        ws.append(row)

    wb.save(sprdsht_dir)

def get_desc() -> str:
    return input("Please input a short description of your mood throughout the day: ")

def get_mood() -> int:
    mood = input("Please input your mood, from 1-10: ")
    try:
        mood_int = int(mood)
    except:
        print("Please input an integer.")
        return get_mood()
    if int(mood) > 10:
        print("Please enter an appropriate number.")
        return get_mood()
    else:
        return mood_int

def exists(input_date: str, ws) -> bool:
    if ws.max_row >= 2:
        for rows in range(1, ws.max_row):
            if ws.cell(row=rows, column=1).value == input_date:
                return True
        return False

def write_mood(mood: int, late: bool, desc: str, importance: bool, input_date: str, sprdsht_dir: str) -> None:
    if input_date != None:
        input_date = datetime.strptime(input_date, '%Y%m%d').date()
    elif not late:
        input_date = date.today()
    else:
        input_date = date.today() - timedelta(days = 1)

    wb = openpyxl.load_workbook(sprdsht_dir)
    ws = wb.active
    data = [str(input_date), str(mood), importance, desc]

    if exists(str(input_date), ws):
        print("You've already entered data.")
        exit()

    ws.append(data)
    wb.save(sprdsht_dir)

def main():
    cli_parse()

if __name__ == "__main__":
    main()
