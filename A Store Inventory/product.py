from peewee import *
import csv
from datetime import datetime

database = SqliteDatabase('inventory.db')

class Product(Model):
    # Set up the model with the columns/fields required
    name = TextField(null = False)
    price = IntegerField(null = False)
    quantity = IntegerField(null = False)
    updated = DateField(null = False)

    class Meta:
        database = database # This model uses the inventory.db database

def create_tables():
    # create the product table using the model object
    with database:
        database.create_tables([Product])

def add_product(product):
    try:
        # see if there is a matching product in the database
        existing_product = Product.get(Product.name == product.name)

        # there is an existing product so we need to check the date updated
        if product.updated > existing_product.updated:
            # update the existing product in the database as it has been updated more recently
            existing_product.price = product.price
            existing_product.quantity = product.quantity
            existing_product.updated = product.updated

            # save the updates
            existing_product.save()

            print(existing_product.name + " updated")
    except DoesNotExist:
        # save the product in the database as it does not exist
        product.save()

        print(product.name + " added")

def add_inventory():
    # open the CSV file to create products
    with open('inventory.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        next(readCSV, None)  # skip the headers

        # read each row of CSV data
        for row in readCSV:
            # store each row field
            name = row[0]
            price = row[1]
            quantity = row[2]
            updated = row[3]

            # sanitize the name field to remove quotes
            name = name.replace('\"', '')

            # sanitize the price field to be in cents
            price = price.replace('$', '')
            price = price.replace('.', '')

            # create a product model for the row
            product = Product(name=name, price=price, quantity=quantity, updated=updated)

            # call a function to add the product to the database
            add_product(product)

def view_product():
    product_id = input("Enter a product ID: ")

    try:
        # see if there is a product in the database with the given ID
        product = Product.get(Product.id == product_id)

        print("Product found\n\tname: " + product.name + "\n\tquantity: " + str(product.quantity) + "\n\tprice: " + str(product.price) + "\n\tlast updated on: " + product.updated)
    except DoesNotExist:
        # unknown product
        print("Could not find a product with ID: " + product_id)

def get_string_input(prompt):
    # loop until valid input is provided
    value = None
    while value is None:
        # remove any whitespace around the input
        submitted_value = input(prompt).strip()

        # check the provided input for a valid value
        if submitted_value:
            value =  submitted_value
        else:
            print("Please enter a value")

    return value

def get_number_input(prompt):
    # loop until valid input is provided
    number = None
    while number is None:
        # remove any whitespace around the input
        submitted_value = input(prompt).strip()

        try:
            # convert the provided input to a number
            number = float(submitted_value)

            # ensure the given number is valid
            if number < 1:
                number = None
                print("Please enter a number greater than 0")
        except ValueError:
            print("Please enter a number")

    return number

def insert_new_product():
    product_name = get_string_input("Enter a product name: ")
    product_price = get_number_input("Enter a product price: ")
    product_quantity = get_number_input("Enter a product quantity: ")
    product_updated = get_string_input("Enter a product updated date: ")

    # create a product model
    product = Product(name=product_name, price=product_price, quantity=product_quantity, updated=product_updated)

    # call a function to add the product to the database
    add_product(product)

def backup_database():
    print("Backing up database:")

    # field names
    fields = ['Name', 'Price', 'Quantity', 'Date Updated']

    # data rows of csv file
    rows = [ ['Nikhil', 'COE', '2', '9.0'],
            ['Sanchit', 'COE', '2', '9.1'],
            ['Aditya', 'IT', '2', '9.3'],
            ['Sagar', 'SE', '1', '9.5'],
            ['Prateek', 'MCE', '3', '7.8'],
            ['Sahil', 'EP', '2', '9.1']]

    # name of csv file
    filename = "backup.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # fetch all products
        for product in Product.select():
            row = [product.name, product.quantity, product.price, product.updated]

            # write the product row
            csvwriter.writerow(row)

    print("Back up complete")

def output():
    print("\n\nEntire database:")
    for product in Product.select():
        print("\t" + product.name, product.quantity, product.price, product.updated)

def delete():
    tables = database.get_tables()
    if len(tables) == 0:
        return

    for product in Product.select():
        product.delete_instance()

def menu():
    print("\n\n")

    while True:
        print("View a single product's inventory => v")
        print("Add a new product to the database => a")
        print("Make a backup of the entire inventory => b")
        print("Quit => q")

        selection = input("Choice: ")

        # process the option selected
        if selection:
            # lowercase the selection for easier processing
            selection = selection.lower()

            if selection == "v":
                view_product()
            elif selection == "a":
                insert_new_product()
            elif selection == "b":
                backup_database()
            elif selection == "q":
                print("Quitting")
                break

        print()

if __name__ == '__main__':
    delete()
    create_tables()
    add_inventory()

    menu()

    output()
