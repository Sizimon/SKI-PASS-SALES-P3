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
SHEET = GSPREAD_CLIENT.open('SKI_PASS_SALES')

def user_sales_input():
    '''
    Ask the user to input the sales numbers. 
    Use a loop to validate the string input by the user.
    Throw an error prompt if the data input is in incorrect format.
    '''
    while True:
        print('------------------------------------------------------------')
        print('Welcome, I hope you have had a good day.')
        print('Please enter in the daily pass sales for today below.')
        print('Enter the data for our 5 locations seperated by commas.')
        print('EG. 546, 259, 1203, 455, 756')
        print('------------------------------------------------------------\n')
        
        user_daily_sales = input('Enter the daily pass sales for today:\n')
        print(f'The daily pass sales for today were: {user_daily_sales}.')

        print('\nNow enter the weekly pass sales.\n')
        user_weekly_sales = input('Enter the weekly pass sales for today:\n')
        print(f'The weekly pass sales for today were: {user_weekly_sales}.')

        daily_sales = user_daily_sales.split(',')
        weekly_sales = user_weekly_sales.split(',')

        if data_validation(daily_sales, weekly_sales):
            print('The data you entered is valid.')
            print('Confirm that you have entered the correct data, you cannot resubmit.')
            while True:
                confirm = input('Type Y for Yes or N for No:\n')
                if confirm == 'Y':
                    print('You have confirmed todays sales.')
                    return daily_sales, weekly_sales
                elif confirm == 'N':
                    print('Resubmit your sales numbers.')
                    run()
                    break
                else:
                    print('Invalid choice, valid choices are; Y or N.')
            break
                    

def data_validation(value1, value2):
    '''
    Use a try statement to convert values provided by user into integers.
    Check if the values submitted by the user total 5 seperate values.
    Throw a value error if the values provided do not total 5.
    Throw a tailored error for a different error.
    '''
    try:
        [int(value) for value in value1]
        [int(value) for value in value2]
        if len(value1) != 5 or len(value2) != 5:
            raise ValueError(
                f'You need to provide 5 values, you provided {len(value1)} and {len(value2)}.'
            )
    except ValueError as e:
            print(f'Invalid data: {e}, Please try again.\n')
            return False
    return True    


user_sales_input()