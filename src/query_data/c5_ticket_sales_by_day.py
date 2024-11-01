import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

WEEKDAY_MAP = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

def c5_ticket_sales_by_day():
    sales_by_day = {day: 0 for day in WEEKDAY_MAP.keys()}

    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])
        if time_dimension:
            year, month, day = time_dimension.get('year'), time_dimension.get('month'), time_dimension.get('day')
            try:
                weekday = datetime(year, month, day).weekday()
                sales_by_day[weekday] += sale['total_ticket']
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day}")

    rows = [{"Weekday": WEEKDAY_MAP[day], "Tickets_Sold": qty} for day, qty in sales_by_day.items()]
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c5_ticket_sales_by_day.csv', index=False)
