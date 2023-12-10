import csv

locators = {}

def read_data_from_csv():
    with open("D:/100DaysCoding/AmberStudent/QA-Assessment/AmberStudent-QA-Assignment/resources/locators.csv", mode='r') as file:
        # locators = {}
        reader = csv.DictReader(file)
        for row in reader:
            locators[row['element']] = {'type': row['locator'],  'value': row['locator-value'].replace(';', ',')}
    return locators

def read_user_credentials_from_csv():
    with open("D:/100DaysCoding/AmberStudent/QA-Assessment/AmberStudent-QA-Assignment/resources/user.csv", mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            email = row['email']
            password = row['password']
    return email, password

# print(read_user_credentials_from_csv())