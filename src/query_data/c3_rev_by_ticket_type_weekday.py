import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
ticket_db = db["tickets"]
time_db = db["time"]


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
        ticket = ticket_data.get(sale['ticketcodes'][0])  # Giả định chỉ lấy mã vé đầu tiên cho tính toán

        if ticket and time_dimension:
            ticket_type = ticket.get('ticket type')
            year = time_dimension.get('year')
            month = time_dimension.get('month')
            day = time_dimension.get('day')
            revenue = sale['total_sales']

            # Chuyển đổi ngày thành ngày trong tuần
            try:
                weekday = datetime(year, month, day).weekday()  # weekday() trả về 0 (Thứ Hai) đến 6 (Chủ Nhật)
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day} in sale record {sale}")
                continue

            # Khởi tạo nếu chưa có loại vé và ngày trong tuần
            if ticket_type not in revenue_by_ticket_weekday:
                revenue_by_ticket_weekday[ticket_type] = {day: 0 for day in range(7)}

            # Cộng dồn doanh thu theo loại vé và ngày trong tuần
            revenue_by_ticket_weekday[ticket_type][weekday] += revenue

    # Chuyển đổi dữ liệu và lưu thành CSV
    rows = []
    for ticket_type, weekdays in revenue_by_ticket_weekday.items():
        for day, revenue in weekdays.items():
            rows.append({
                "Ticket_Type": ticket_type,
                "Weekday": day,
                "Revenue": revenue
            })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c3_rev_by_ticket_type_weekday.csv', index=False)
