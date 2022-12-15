import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Music_Hub_Data')


def get_interest_data():
    """
    Get interest figures input from the user.
    Run a while loop to collect valid data from user which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter interest data from this term.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 1,2,3,4,5,6\n")

        data_str = input("Enter your data here: \n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid, thank you.")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    If strings cannot be converted into int it will raise the error as well as
    if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Combine the two seperate update worksheet functions into the same one using f strings and a 
    new variable worksheet to update the specific worksheet needed.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_update = SHEET.worksheet(worksheet)
    worksheet_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")


def calculate_surplus_data(interest_row):
    """
    Compare interest with stock and calculate the surplus for each instrument.
    The surplus = interest figure subtracted from the stock:
    - Positive surplus indicates spare instruments
    - Negative surplus indicates extra made when stock was needed to be loaned from other music services.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, interest in zip(stock_row, interest_row):
        surplus = int(stock) - interest
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_interest():
    """
    Collects columns of data from interest worksheet so we can use this for the estimate
    calculation of stock needed
    """
    interest = SHEET.worksheet("interest")

    columns = []
    for ind in range(1, 7):
        column = interest.col_values(ind)
        columns.append(column[-5:])
        print(columns)

    return columns


def main():
    """
    Runs all main functions
    """
    data = get_interest_data()
    interest_data = [int(num) for num in data]
    update_worksheet(interest_data, 'interest')
    new_surplus_data = calculate_surplus_data(interest_data)
    update_worksheet(new_surplus_data, 'surplus')


print("Thank you for using Music Hub Data Automation!\n")
main()
