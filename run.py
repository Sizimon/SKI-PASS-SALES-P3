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
        print('============================================================\n')
        print('Welcome, I hope you have had a good day.\n')
        print('Please enter in the daily pass sales for today below.')
        print('Enter the data for our 5 locations seperated by commas.\n')
        print('Order: Are, Borgafjall, Hovden, Val de Saire, Zakopane.')
        print('EG. 546, 259, 1203, 455, 756\n')
        print('------------------------------------------------------------\n')

        user_daily_sales = input('Enter the daily pass sales for today:\n')
        print(f'The daily pass sales for today were: {user_daily_sales}.\n')
        print('------------------------------------------------------------\n')

        user_weekly_sales = input('Enter the weekly pass sales for today:\n')
        print(f'The weekly pass sales for today were: {user_weekly_sales}.\n')
        print('------------------------------------------------------------\n')

        daily_sales = user_daily_sales.split(',')
        weekly_sales = user_weekly_sales.split(',')

        if data_validation(daily_sales, weekly_sales):
            print('The data you entered is valid.')
            print('Confirm that you have entered the correct data.\n')
            while True:
                confirm = input('Type Y for Yes or N for No:\n')
                if confirm == 'Y':
                    print('You have confirmed todays sales.\n')
                    return daily_sales, weekly_sales
                elif confirm == 'N':
                    print('Resubmit your sales numbers.\n')
                    main()
                else:
                    print('Invalid choice, valid choices are; Y or N.\n')
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


def update_worksheet(data, worksheet):
    '''
    Grabs the integers from the user input,
    and updates them into the designated worksheet.
    '''
    print('------------------------------------------------------------\n')
    print(f'{worksheet} is now updating...')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row([int(x) for x in data])
    print(f'{worksheet} has now updated successfully.\n')


def calculate_total_pass_sales(sum1, sum2):
    '''
    After input and confirmation from user, calculate total pass sales from day
    by summing all the numbers input in daily row together, adding them to all
    numbers summed in weekly row.
    '''
    print('------------------------------------------------------------\n')
    print('Calculating the total sales...\n')

    daily_data = [int(num) for num in sum1]
    weekly_data = [int(num) for num in sum2]
    total_data = [num1 + num2 for num1, num2 in zip(daily_data, weekly_data)]

    return total_data


def calculate_revenue_from_pass(sum1, sum2):
    '''
    Ask the user if they would like to calculate revenue from the pass sales.
    Initiate a sequence which calculates the revenue from daily passes, then weekly passes.
    Add them together to produce total revenue.
    Daily Pass is Priced at $25
    Weekly Pass is Priced at $125
    '''
    print('------------------------------------------------------------\n')
    proceed = input('Proceed with revenue calculations? (Y/N)\n')
    if proceed == 'Y':
        print('Calculating total revenue...\n')

        daily_revenue = [int(x) * 25 for x in sum1]
        weekly_revenue = [int(x) * 125 for x in sum2]
        total_revenue = [num1 + num2 for num1, num2 in zip(daily_revenue, weekly_revenue)]
        return total_revenue
    elif proceed == 'N':
        print('\nAborting revenue calculations.')
        main()


def calculate_net_from_pass(sum):
    '''
    Tell the user that the net will be calculated and ask them to commence the sequence,
    the program will then take the calculated revenue from before and take off the sales tax
    to produce a net.
    '''
    print('------------------------------------------------------------\n')
    proceed = input('Proceed with the net revenue calculations? (Y/N)\n')
    if proceed == 'Y':
        print('Calculating net revenue...\n')
        total_net = [int(x) * 67/100 for x in sum]
        return total_net
    elif proceed == 'N':
        print('\nAborting net calculations.')
        main()


def expected_pass_sales(sum1, sum2):
    '''
    Gives the user feedback based on pass sales from the day,
    including an average daily sales expectancy, and displays whether they are
    below or above the average.
    '''
    expected_dict_daily = {
            0: ['Are', 165],
            1: ['Borgafjall', 48],
            2: ['Hovden', 102],
            3: ['Val De Saire', 322],
            4: ['Zakopane', 204]
        }
    expected_dict_weekly = {
            0: ['Are', 74],
            1: ['Borgafjall', 23],
            2: ['Hovden', 68],
            3: ['Val De Saire', 192],
            4: ['Zakopane', 134]
    }
    print('------------------------------------------------------------\n')
    print('All data successfully submitted.')
    proceed = input('Would you like to see expected pass sales? (Y/N)\n')
    print('------------------------------------------------------------\n')
    if proceed == 'Y':
        for key, value in expected_dict_daily.items():
            print(f'{value[0]} has a target daily pass sales of {value[1]}')
            print(f'Todays daily pass sales were {sum1[key]}\n')
        for key, value in expected_dict_weekly.items():
            print(f'{value[0]} has a target weekly pass sales of {value[1]}')
            print(f'Todays weekly pass sales were {sum2[key]}\n')
    elif proceed == 'N':
        print('Ending the program, thank you for your submissions.')
        main()


def main():
    '''
    Run all program functions
    '''
    data = user_sales_input()
    if data:
        daily_sales = data[0]
        update_worksheet(daily_sales, 'DAILY')
        weekly_sales = data[1]
        update_worksheet(weekly_sales, 'WEEKLY')
        total_sales = calculate_total_pass_sales(daily_sales, weekly_sales)
        update_worksheet(total_sales, 'TOTAL')
        revenue_data = calculate_revenue_from_pass(daily_sales, weekly_sales)
        update_worksheet(revenue_data, 'GROSS')
        net_data = calculate_net_from_pass(revenue_data)
        update_worksheet(net_data, 'NET')
        expected_pass_sales(daily_sales, weekly_sales)
        print('============================================================')


main()
