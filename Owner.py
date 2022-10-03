from DataConnection import DataConnection
from Utilities import Utilities


class Owner:
    # table name
    owner_table_name = "dbo.Owner"

    # column names
    owner_id_column_name = "Owner_ID"
    owner_first_name_column_name = "Owner_First_Name"
    owner_last_name_column_name = "Owner_Last_Name"
    owner_area_code_column_name = "Owner_Area_Code"
    owner_phone_number_column_name = "Owner_Phone_Number"
    owner_street_address_column_name = "Owner_Address"
    owner_city_column_name = "Owner_City"
    owner_state_column_name = "Owner_State"
    owner_zipcode_column_name = "Owner_Zipcode"
    owner_date_added_column_name = "Owner_Date_Added"

    # ownership table name
    ownership_table_name = "dbo.Ownership"

    def __init__(self, primary_key, first_name, last_name):
        self.primary_key = primary_key
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def display_all_owners(cls):
        # Display all Owners

        connection = DataConnection()
        owner_list = Owner.get_list_of_owners(connection)

        underline_unicode_on = '\33[4m'
        underline_unicode_off = '\33[m'
        print("Here are the existing Owners.")
        print()
        print(underline_unicode_on + "id  | name" + underline_unicode_off)

        for owner in owner_list:
            width_needed = 2 - len(str(owner.primary_key))
            print(owner.primary_key, " " * width_needed, "|", owner.first_name, owner.last_name)

        connection.close_connection()

    @classmethod
    def add_owner(cls):

        connection = DataConnection()

        insert_owner_query = f"INSERT INTO {Owner.owner_table_name}({Owner.owner_first_name_column_name}, " \
                             f"{Owner.owner_last_name_column_name},{Owner.owner_area_code_column_name}, " \
                             f"{Owner.owner_phone_number_column_name}, {Owner.owner_street_address_column_name}, " \
                             f"{Owner.owner_city_column_name}, {Owner.owner_state_column_name}, " \
                             f"{Owner.owner_zipcode_column_name}) VALUES(?, ?, ?, ?, ?, ?, ?, ?);"
        arguments_list = Owner.collect_args_to_add_owner()

        connection.update_data(insert_owner_query, arguments_list)

        print()

        newest_owner = Owner.get_newest_owner(connection)

        print(f"Owner {newest_owner.first_name} {newest_owner.last_name} inserted!")

        connection.close_connection()

    @classmethod
    def collect_args_to_add_owner(cls):
        arguments_list = []

        print("Time to enter a new owner!")
        arguments_list.append(input("Owner First Name: "))
        arguments_list.append(input("Owner Last Name: "))
        Owner.get_valid_area_code(arguments_list)
        Owner.get_valid_phone_number(arguments_list)
        arguments_list.append(input("Street Address: "))
        arguments_list.append(input("City: "))
        Owner.get_two_letter_state_symbol(arguments_list)
        Owner.get_valid_zipcode(arguments_list)

        return arguments_list

    @classmethod
    def get_two_letter_state_symbol(cls, arguments_list):
        valid = False
        while not valid:
            state_letters = input("State(The two letter symbol): ")
            if len(state_letters) == 2:
                arguments_list.append(state_letters)
                valid = True
            else:
                print("Invalid State Designation")

    @classmethod
    def get_valid_phone_number(cls, arguments_list):

        valid = False
        while not valid:
            phone_number = input("Phone Number: ")
            if len(phone_number) == 7:
                try:
                    int(phone_number)
                    formatted_phone_number = Utilities.add_a_dash_to_phone_number(phone_number)
                    arguments_list.append(formatted_phone_number)
                    valid = True
                except ValueError:
                    print("Phone number contains stray characters!")
                    print("Please try again.")
            elif len(phone_number) == 8 and phone_number[3] == "-":
                arguments_list.append(phone_number)
                valid = True
            else:
                print("Invalid Phone Number")

    @classmethod
    def get_valid_area_code(cls, arguments_list):
        valid = False
        while not valid:
            area_code = input("Phone Area Code(No Parenthesis): ")
            if len(area_code) == 3:
                try:
                    int(area_code)
                    arguments_list.append(area_code)
                    valid = True
                except ValueError:
                    print("Error: Area code contains characters besides numbers")
            else:
                print("Invalid Area Code")

    @classmethod
    def get_valid_zipcode(cls, arguments_list):
        valid = False
        while not valid:
            zip_code = input("Zipcode(the first 5 digits): ")
            if len(zip_code) == 5:
                try:
                    int(zip_code)
                    arguments_list.append(zip_code)
                    valid = True
                except ValueError:
                    print("Error: Zipcode contains more than numbers")
            else:
                print("Error: Invalid Zipcode")

    @classmethod
    def delete_owner(cls):
        # function to delete an owner and their ownership

        connection = DataConnection()

        print("Preparing to delete an Owner!")
        print()

        owner_selected = Owner.select_an_owner(connection)

        # if not cancelled the number of selection is valid
        if owner_selected != -1:

            Owner.delete_owners_ownership(connection, owner_selected.primary_key)

            Owner.delete_owner_by_pk(connection, owner_selected.primary_key)

            print()
            print("All trace of ownership of cats deleted!")
            print("...")

            print(f"Owner named {owner_selected.first_name} {owner_selected.last_name} deleted!")
        else:
            print("Deletion cancelled!")

        print()
        connection.close_connection()

    @classmethod
    def get_owner_list_ordered_by_pk(cls, connection):

        owner_pk_and_name_list = []
        get_owner_query = f"Select {Owner.owner_id_column_name}, {Owner.owner_first_name_column_name}, " \
                          f"{Owner.owner_last_name_column_name} FROM {Owner.owner_table_name} " \
                          f"Order By {Owner.owner_id_column_name}"

        owner_pk_and_name_cursor = connection.run_query(get_owner_query, None)

        for row in owner_pk_and_name_cursor:
            owner_pk_and_name_list.append(row)

        return owner_pk_and_name_list

    @classmethod
    def delete_owners_ownership(cls, connection, primary_key_selected):
        # Delete trace of cat ownership by selecting the owners primary key
        deletion_query_ownership = f"DELETE {Owner.ownership_table_name} " \
                                   f"WHERE {Owner.owner_id_column_name} = {primary_key_selected};"

        connection.update_data(deletion_query_ownership, None)

    @classmethod
    def delete_owner_by_pk(cls, connection, primary_key_selected):
        # Delete owners by selecting their primary key
        deletion_query_owner = f"DELETE {Owner.owner_table_name} " \
                               f"WHERE {Owner.owner_id_column_name} = {primary_key_selected};"

        connection.update_data(deletion_query_owner, None)

    @classmethod
    def select_an_owner(cls, connection):
        # retrieve all owners in order
        owner_list = Owner.get_list_of_owners(connection)
        owner_to_select = Utilities.make_a_selection(owner_list, "Owner")
        return owner_to_select

    @classmethod
    def get_list_of_owners(cls, connection):

        owner_list_by_pk = Owner.get_owner_list_ordered_by_pk(connection)
        owner_list = []

        # store all owner information accordingly in order
        for row in owner_list_by_pk:
            owner = Owner(row[0], row[1], row[2])
            owner_list.append(owner)

        return owner_list

    @classmethod
    def update_owner_address(cls):
        connection = DataConnection()
        print("Prepare to update Owner address!")

        # Use selection to pull an owner
        owner_selected = Owner.select_an_owner(connection)
        arguments_list = []

        owner_update_address_query = f"UPDATE {Owner.owner_table_name} " \
                                     f"SET {Owner.owner_street_address_column_name} = ?, " \
                                     f"{Owner.owner_city_column_name} = ?, " \
                                     f"{Owner.owner_state_column_name} = ?, " \
                                     f"{Owner.owner_zipcode_column_name} = ? " \
                                     f"WHERE {Owner.owner_id_column_name} = ?;"

        if owner_selected != -1:

            print("Ready to update!")
            print()

            # input the new values
            arguments_list.append(input("Street Address: "))
            arguments_list.append(input("City: "))
            Owner.get_two_letter_state_symbol(arguments_list)
            Owner.get_valid_zipcode(arguments_list)

            # doing this here ensures the primary key variable is correct
            arguments_list.append(owner_selected.primary_key)

            connection.update_data(owner_update_address_query, arguments_list)

            print()
            print(f"Owner {owner_selected.first_name} {owner_selected.last_name}'s address has been updated!")

        else:
            print("Update cancelled!")

        connection.close_connection()

    @classmethod
    def get_newest_owner(cls, connection):
        # returns the newest owner typically the one just inserted
        owner_list = Owner.get_list_of_owners(connection)
        newest_owner = owner_list[len(owner_list) - 1]

        return newest_owner
