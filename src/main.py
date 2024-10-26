from src.import_data import import_customer
from src.import_data import import_film

# Gọi hàm import_customer từ file import_customer.py
if __name__ == "__main__":
    import_customer.import_customer()
    import_film.import_film()