
import os.path
from tabulate import tabulate

#======================The beginning of the class======================
class Shoe():
    """Shoe class object"""
    sale = False  # Default shoe not on promotional sale

    def __init__(self, country, code, product, cost, quantity):
        """Shoe object constructor"""
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_code(self):
        """Returns shoe code"""
        return self.code

    def get_cost(self):
        """Returns shoe cost in £ to two decimal places"""
        cost = f"{self.cost / 100:.2f}"
        return cost

    def get_quantity(self):
        """Returns shoe quantity in stock"""
        return self.quantity

    def add_stock(self, order):
        """
        Adds order to stock
        Args:
            order(int): size of order to add

        Returns:
            New stock count
        """
        self.quantity += order
        return self.quantity

    def sale_on(self):
        """Change Shoe sale attribute to True"""
        self.sale = True

    def sale_off(self):
        """Change Shoe sale attribute to False"""
        self.sale = False

    def __str__(self):
        """Returns a string representation of the Shoe object"""
        if self.sale:
            sale_status = "On Sale"
        else:
            sale_status = "Not on Sale"
        return (f"\nCountry:\t\t{self.country}\
              \nCode:\t\t\t{self.code}\
              \nProduct:\t\t{self.product}\
              \nCost:\t\t\t£{self.get_cost()}\
              \nQuantity:\t\t{self.quantity}\
              \nSale Status:\t{sale_status}")


#==============================Shoe list===============================
shoe_list = []

#=====================Functions outside the class======================
def read_shoes_data():
    """Reads shoes data from inventory.txt, creates Shoe objects and
    appends to shoe_list, displays success or not"""
    # Cheks inventory file exists, returns Bool and error message if
    # not
    inventory_file = check_file(inventory_name)
    # Continues if file found
    while inventory_file:
        try:
            with open(inventory_name, "r") as inventory:
                lines = inventory.readlines()
                # Iterate over each line in file, skipping first line
                for index in range(1, len(lines)):
                    # Remove "\n" from end and split line string into
                    # a list
                    shoe = lines[index].strip().split(",")
                    shoe_list.append(Shoe(shoe[0],
                                          shoe[1],
                                          shoe[2],
                                          int(shoe[3]),
                                          int(shoe[4])
                                          ))
                print(f"\nInventory successfully imported from",
                      f"'{inventory.name}'")
                # Ends function once complete
                return None
        # Cost and quantity converted to integers to allow addition for
        # restock and to ensure minimum/maximum determination is
        # correct, so non-int values needs error handling
        except ValueError:
            print("\tInvalid value(s) for costs or quantities in "
                  + inventory.name)
            break
    # Ends function if file not found
    print("\tCannot import stock from file")
    return None


def capture_shoes():
    """Capture user input to Shoe object and append to shoe_list"""
    country = input("\nEnter country: ")
    # Determine if code given is valid and not a repeat
    while True:
        code = input("Enter code: ")
        if not check_code(code):
            continue
        else:
            if l_search(code, shoe_codes()) is None:
                break
            print("\tCode already assigned to previous product:")
            index_repeat = l_search(code, shoe_codes())
            print(shoe_list[index_repeat])
            if cont():
                continue
            return False
    product = input("Enter product: ")
    # Error handling for cost and quantity inputs
    while True:
        try:
            cost = int(input("Enter cost (in pence): "))
            break
        except ValueError:
            print("\tInvalid cost. Input should be an integer")
            continue
    while True:
        try:
            quantity = int(input("Enter quantity in stock: "))
            break
        except ValueError:
            print("\tInvalid quantity. Input should be an integer")
            continue

    shoe_list.append(Shoe(country, code, product, cost, quantity))
    # Print last list entry as proof of addition
    print(shoe_list[-1])
    print("\n\tShoe successfully added to list")

    # Update inventory file
    if check_file(inventory_name):
        with open(inventory_name, "a") as inventory:
            line = f"{country},{code},{product},{cost},{quantity}\n"
            inventory.write(line)
            print(f"\t'{inventory.name}' updated")
            return None
    else:
        print("\tCannot update inventory file")
        return None


def view_all():
    """Print all shoe information"""
    # shoe_class_to_str() iterates over list of objects to create list
    # of lists
    shoe_table = [["Country", "Code", "Product", "Cost", "Quantity"]]
    for index in range(len(shoe_list)):
        country = shoe_list[index].country
        code = shoe_list[index].code
        product = shoe_list[index].product
        cost_float = shoe_list[index].cost / 100
        cost = f"£{cost_float:.2f}"
        quantity = shoe_list[index].quantity
        shoe_table.append([country, code, product, cost, quantity])
    # Print in tabulated form
    print("\n" + tabulate(shoe_table, headers="firstrow"))


def re_stock():
    """Determines shoe with minimum stock, asks whether to restock"""
    # Determine index of lowest quantity, key argument used to return
    # index. Solution found https://stackoverflow.com/questions/2474015/getting-the-index-of-the-returned-max-or-min-item-using-max-min-on-a-list
    min_quantity = min(shoe_qtys())
    min_index = min(range(len(shoe_qtys())), key=shoe_qtys().__getitem__)
    shoe_list[min_index].sale_off()  # Set sale to off while low stock

    # Print result
    print(f"\nLowest stock determined to be {min_quantity} units for",
          f"\n{shoe_list[min_index]}")

    inventory_file = check_file(inventory_name)
    if not inventory_file:
        print("\tCannot update stock")

    # Ask whether to restock product if inventory file found
    while inventory_file:
        restock = input("\nWould you like to restock product?\n\t").lower()
        if (restock == "y") or (restock == "yes"):
            # Error handling for yes/no input
            while True:
                try:
                    order = int(input("\nEnter quantity to order:\n\t"))
                    break
                except ValueError:
                    print("\tInvalid quantity. Input should be an integer")
                    continue

            # Update shoe_list and convert shoe_list to list of lists
            shoe_list[min_index].add_stock(order)
            shoe_str_list = shoe_class_to_list(shoe_list)

            # Add "\n" to end of lines and convert to single str
            for index in range(len(shoe_str_list)):
                shoe_str_list[index][3] = str(shoe_str_list[index][3])
                shoe_str_list[index][4] = (str(shoe_str_list[index][4]) + "\n")
                shoe_str_list[index] = ",".join(shoe_str_list[index])

            # Overwrite inventory file and display updated info
            with open(inventory_name, "r+") as inventory:
                inventory.writelines(shoe_str_list)
                print(f"\nProduct inventory updated\n{shoe_list[min_index]}\n")
            break

        elif (restock == "n") or (restock == "no"):
            return None

        else:
            print("\tInvalid input. Please enter yes or no")
            continue
    return None


def shoe_class_to_list(shoes):
    """
    Method to convert list of Shoe objects into list of lists
    Args:
        shoes(list): list of Shoe objects

    Returns:
        List of lists with headers for tabulating index 0
    """
    shoe_list_list = [["Country", "Code", "Product", "Cost", "Quantity"]]
    for index in range(len(shoe_list)):
        country = shoe_list[index].country
        code = shoe_list[index].code
        product = shoe_list[index].product
        cost = shoe_list[index].cost
        quantity = shoe_list[index].quantity
        shoe_list_list.append([country, code, product, cost, quantity])
    return shoe_list_list


def search_shoe():
    """Search for shoe with code"""
    # Create list of codes from shoe_list
    codes = shoe_codes()

    while True:
        target = input("\nEnter shoe code: ")
        # Check code is valid (8 char, for 3 letters, last 5 numbers)
        if not check_code(target):
            continue  # Loop back if code not valid
        else:
            # Search for code (linear as list unordered)
            index_target = l_search(target, codes)
            if (index_target is not None):
                print(shoe_list[index_target])
                break
            else:
                print("\tShoe not found in inventory")
                break


def l_search(target, items):
    """
    Linear search algorithm
    Args:
        target(str): Target to search for
        items(list): List to search within

    Returns:
        Index of target if found, otherwise None
    """
    for index in range(len(items)):
        if (items[index] == target):
            return index
    return None


def check_code(code):
    """
    Method to check if given code is in the form 'ABC12345'
    Args:
        code(str): Code to check

    Returns:
        Returns True if valid, otherwise False with message
    """
    # Check length (must be 8 characters)
    if (len(code) != 8):
        print("\tInvalid code. Shoe codes should be 8 characters long\n")
        return False
    # Check first 3 have no numbers, last 5 have no letters
    l = any(c.isdigit() for c in code[0:3])  # Check for numbers
    n = any(c.isalpha() for c in code[3:8])  # Check for letters
    if (not l) and (not n):
        return True
    else:
        print("\tInvalid code. Shoe code must be in the form 'ABC12345'")
        return False


def value_per_item():
    """Calculate value in inventory for each product"""
    shoe_values = []
    for index in range(len(shoe_list)):
        value = shoe_list[index].cost * shoe_list[index].quantity
        shoe_values.append(value)

    # Add value column to tabulated view of shoes
    shoe_table = [["Country", "Code", "Product", "Cost", "Quantity", "Value"]]
    for index in range(len(shoe_list)):
        country = shoe_list[index].country
        code = shoe_list[index].code
        product = shoe_list[index].product
        cost_float = shoe_list[index].cost / 100
        cost = f"£{cost_float:.2f}"
        quantity = shoe_list[index].quantity
        value_float = shoe_values[index] / 100
        value = f"£{value_float:.2f}"
        shoe_table.append([country, code, product, cost, quantity, value])
    print("\n" + tabulate(shoe_table, headers="firstrow"))


def highest_qty():
    """Determine product with most stock and set a sale"""
    # Same approach as in re_stock() method
    max_quantity = max(shoe_qtys())
    max_index = max(range(len(shoe_qtys())), key=shoe_qtys().__getitem__)
    shoe_list[max_index].sale_on()  # Set sale to on while stock high

    # Print result
    print(f"\nLargest stock determined to be {max_quantity} units for"
          + f"\n{shoe_list[max_index]}\n\n\tSale now on")


def check_file(file):
    """
    Method to check if inventory file exists
    Args:
        file(str): Name of inventory file:

    Returns:
        Bool: True if file exists, otherwise False and displays error
    """
    inventory_file = os.path.isfile(file)
    if inventory_file:
        return True
    else:
        print("\n\tInventory file not found")
        return False


def shoe_codes():
    """Create list of shoe codes from shoe_list"""
    shoe_codes = []
    for index in range(len(shoe_list)):
        code = shoe_list[index].code
        shoe_codes.append(code)
    return shoe_codes


def shoe_qtys():
    """Create list of shoe quantities from shoe_list"""
    shoe_quantities = []
    for index in range(len(shoe_list)):
        qty = shoe_list[index].quantity
        shoe_quantities.append(qty)
    return shoe_quantities


def sep():
    """Print line separator"""
    print(separator)


def cont():
    """Ask whether to continue or not, return Bool"""
    cont = input("Continue? [Y/N]: ").lower()
    while True:
        if (cont == "y"):
            return True
        elif (cont == "n"):
            print("\nBye bye!")
            return False
        else:
            cont = input("\n\tEnter Y or N: ").lower()
            continue


#===========================Variable Set Up============================
separator = 79 * "_"

# Variable declared so no typo/mismatches in usage and easily modified
inventory_name = "inventory.txt"

# Setting up table of options
option0 = ["quit", "End the program"]
option1 = ["import", "Import inventory from file"]
option2 = ["input", "Input new product information"]
option3 = ["view", "View all product information"]
option4 = ["restock", "Restock advice"]
option5 = ["search", "Search shoes by code"]
option6 = ["value", "View total product values in stock"]
option7 = ["sale", "Promotional sale advice"]

options_list = [
        option1, option2, option3, option4, option5, option6, option7, option0
        ]

options_dict = dict(options_list)

options_table = [["", "Choice", "Description"]]
opt_index = 0
for key in options_dict:
    opt_index += 1
    # So quit option with input 0 is listed last
    if opt_index == len(options_dict):
        opt_index = 0
    value = options_dict[key]
    options_table.append([opt_index, key, value])

#==============================Main Menu===============================
read_shoes_data()  # Initialises shoes list from external file
print("\nWelcome to the inventory console. Options are as follows:\n")
while True:
    print(tabulate(options_table, headers="firstrow"))
    sep()

    choice = input("Enter the number or keyword your choice: ")
    # Re-imports data from file
    if (choice == "1") or (choice == option1[0]):
        read_shoes_data()
        sep()
    # Receives input for new product entry
    elif (choice == "2") or (choice == option2[0]):
        if capture_shoes() is not False:
            sep()
            if not cont():
                break
            continue
        else:
            break
    # View table of all products
    elif (choice == "3") or (choice == option3[0]):
        view_all()
        sep()
        if not cont():
            break
        continue
    # Restock determination and stock update
    elif (choice == "4") or (choice == option4[0]):
        re_stock()
        sep()
        if not cont():
            break
        continue
    # Product code search tool
    elif (choice == "5") or (choice == option5[0]):
        search_shoe()
        sep()
        if not cont():
            break
        continue
    # Stock value calculator
    elif (choice == "6") or (choice == option6[0]):
        value_per_item()
        sep()
        if not cont():
            break
        continue
    # Promotional sale determinator
    elif (choice == "7") or (choice == option7[0]):
        highest_qty()
        sep()
        if not cont():
            break
        continue
    # Ends program
    elif (choice == "0") or (choice == option0[0]):
        break
    else:
        # In the case of invalid choice,  displays message and loops
        print("\n\tInvalid input"
              "\n\tPlease choose from the following options:")
        continue