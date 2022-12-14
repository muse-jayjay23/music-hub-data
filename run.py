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
        print("Example: 10,20,30,40,50,60\n")

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


def update_interest_worksheet(data):
    """
    Update the google sheet with the data inputted by the user
    """
    print("Updating interest worksheet...\n")
    interest_worksheet = SHEET.worksheet('interest')
    interest_worksheet.append_row(data)
    print("Interest worksheet updated successfully!\n")


data = get_interest_data()
interest_data = [int(num) for num in data]
update_interest_worksheet(interest_data)
