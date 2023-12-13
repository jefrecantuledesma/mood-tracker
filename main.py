import pandas as pd
import argparse as ap
from datetime import date, timedelta
import pyexcel as pe

def cli_parse():
    parser = ap.ArgumentParser(description="A CLI program to track your daily mood.")

    parser.add_argument("-e", "--enter", action="store_true", help="Input your daily mood.")
    parser.add_argument("-l", "--late", action="store_true", help="Use if you are submitting past 11:59pm.")

    args = parser.parse_args()

    if args.enter:
        late = args.late
        mood = get_mood()
        desc = get_desc()
        write_mood(mood, late, desc)

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

def exists(input_date: str, sheet) -> bool:
    #rows = sheet.number_of_rows()
    if int(sheet.number_of_rows()) >= 2:
        last_row = sheet.column[0][-1]
        second_last_row = sheet.column[0][-2]
        if last_row or second_last_row == input_date:
            return True
        else: 
            return False
    else:
        return False

def write_mood(mood: int, late: bool, desc: str):
    if not late:
        input_date = date.today()
    else:
        input_date = date.today() - timedelta(days = 1)

    file = "/home/fribbit/Documents/personal_documents/journaling/mood_tracker.ods"

    data = [str(input_date), str(mood), desc]

    sheet = pe.get_sheet(file_name=file)
    if exists(str(input_date), sheet):
        print("You've already entered data.")
        return "Penis"

    sheet.row += data
    sheet.save_as(file)

def main():
    cli_parse()

if __name__ == "__main__":
    main()
