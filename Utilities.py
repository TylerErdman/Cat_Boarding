import datetime


class Utilities:

    @classmethod
    def make_a_selection(cls, object_list, object_type_string):

        selection = ""
        object_list_size = len(object_list)

        cls.print_correct_object_interface(object_list, object_type_string)

        print()
        done = False
        cancelled = False
        selection_as_an_int = None

        # if there are no owners to select then auto cancelled
        if object_list_size == 0:
            print(f"Error: No {object_type_string}!")
            cancelled = True

        print("Type Q to quit!")
        while not done and not cancelled:

            # retrieve the int as a string, if not an int give error message, then repeat
            try:
                selection = input(f"Enter the number of the {object_type_string} to select: ")
                selection_as_an_int = int(selection) - 1
                # Check if the selection is valid within the range of the list
                if object_list_size > selection_as_an_int >= 0:
                    done = True
                else:
                    print("Error: not a valid int for selection!")

            except ValueError:
                if selection.upper() == "Q":
                    cancelled = True
                else:
                    print("Error: selection not an integer!")

        if not cancelled:
            return object_list[selection_as_an_int]
        else:
            return -1

    @classmethod
    def print_correct_object_interface(cls, object_list, object_type_string):
        # check object type and print specific interface
        if object_type_string.upper() == "ROOM":
            Utilities.print_room_interface(object_list)
        elif object_type_string.upper() == "OWNER":
            Utilities.print_owner_interface(object_list)
        elif object_type_string.upper() == "CAT":
            Utilities.print_cat_interface(object_list)

    @classmethod
    def print_cat_interface(cls, cat_list):
        # format and print the interface
        index = 1
        for cat in cat_list:
            print(f"{index})", cat.cat_name + ", " + cat.cat_color + ", " + cat.cat_breed)
            index += 1

    @classmethod
    def print_room_interface(cls, room_list):
        # format and print the interface
        index = 1
        for room in room_list:
            print(f"{index})", room.room_name + ": Available Openings: " + str(room.room_capacity))
            index += 1

    @classmethod
    def print_owner_interface(cls, owner_list):
        # format and print the interface
        index = 1
        for owner in owner_list:
            print(f"{index})", owner.first_name, owner.last_name)
            index += 1

    @classmethod
    def get_valid_checkout_date(cls):
        print("type Q to exit")
        current_date = datetime.datetime.today()
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)

        done = False
        while not done:
            checkout_date = input("Please enter a checkout date(MM/DD/YYYY):")
            if checkout_date.upper() == "Q":
                done = True
            else:
                try:
                    checkout_date = datetime.datetime.strptime(checkout_date, "%m/%d/%Y")

                    if checkout_date >= current_date:
                        return checkout_date
                except ValueError:
                    print("Invalid Date!")

        return -1

    @classmethod
    def add_a_dash_to_phone_number(cls, phone_number):
        # split a string and add a dash
        first_half = phone_number[:3]
        second_half = phone_number[3:]
        formatted_number = first_half + "-" + second_half
        return formatted_number
