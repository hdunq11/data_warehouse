import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
ticket_db = db["tickets"]
time_db = db["time"]

WEEKDAY_MAP = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}


def c3_rev_by_ticket_type_weekday():
    # Cấu trúc lưu doanh thu theo loại vé và ngày trong tuần
    revenue_by_ticket_weekday = {}

    # Tải dữ liệu
    sales_by_time = list(sales_by_time_db.find())
    ticket_data = {ticket['ticketcode']: ticket for ticket in ticket_db.find()}
    time_data = {time['time_id']: time for time in time_db.find()}

    # Tính toán doanh thu theo loại vé và ngày trong tuần
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])
        ticket = ticket_data.get(sale['ticketcodes'][0])

        if ticket and time_dimension:
            ticket_type = ticket.get('ticket type')
            year, month, day = time_dimension.get('year'), time_dimension.get('month'), time_dimension.get('day')
            revenue = sale['total_sales']

            try:
                weekday = datetime(year, month, day).weekday()
                if ticket_type not in revenue_by_ticket_weekday:
                    revenue_by_ticket_weekday[ticket_type] = {day: 0 for day in WEEKDAY_MAP.keys()}

                revenue_by_ticket_weekday[ticket_type][weekday] += revenue
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day}")

    rows = []
    for ticket_type, weekdays in revenue_by_ticket_weekday.items():
        for day, revenue in weekdays.items():
            rows.append({
                "Ticket_Type": ticket_type,
                "Weekday": WEEKDAY_MAP[day],
                "Revenue": revenue
            })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c3_rev_by_ticket_type_weekday.csv', index=False)
