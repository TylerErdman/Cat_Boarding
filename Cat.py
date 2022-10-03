from DataConnection import DataConnection
from Owner import Owner
from Room import Room
from Utilities import Utilities
from Book import Book


class Cat:

    # table names
    cat_table_name = "dbo.Cat"
    ownership_table_name = "dbo.Ownership"

    # column names
    cat_id_column_name = "Cat_ID"
    cat_name_column_name = "Cat_Name"
    cat_color_column_name = "Cat_Color"
    cat_breed_column_name = "Cat_Breed"
    cat_birthday_column_name = "Cat_Birthday"

    ownership_cat_id_column = "Cat_ID"
    ownership_owner_id_column = "Owner_ID"

    def __init__(self, cat_id, cat_name, cat_color, cat_breed, cat_birthday):
        self.cat_id = cat_id
        self.cat_name = cat_name
        self.cat_color = cat_color
        self.cat_breed = cat_breed
        self.cat_birthday = cat_birthday

    @classmethod
    def display_all_cats(cls):
        # Display all Cats
        connection = DataConnection()

        all_cats = Cat.get_list_of_all_cats(connection)
        print("Here are the existing cats.")
        print("id : name, color(s), breed, and birthday")
        for cat in all_cats:
            print(str(cat.cat_id) + ":", cat.cat_name + ", " + cat.cat_color
                  + ", " + cat.cat_breed + ", " + cat.cat_birthday)

        connection.close_connection()

    @classmethod
    def get_list_of_all_cats(cls, connection):
        # Get a list of all cats ordered by primary key
        get_cat_list = f"SELECT {Cat.cat_id_column_name}, {Cat.cat_name_column_name}, " \
                       f"{Cat.cat_color_column_name}, {Cat.cat_breed_column_name}, {Cat.cat_birthday_column_name} " \
                       f"FROM {Cat.cat_table_name} " \
                       f"ORDER BY {Cat.cat_id_column_name};"
        cat_list_attributes = connection.run_query(get_cat_list)
        cat_list = []

        for row in cat_list_attributes:
            cat = Cat(row[0], row[1], row[2], row[3], row[4])
            cat_list.append(cat)

        return cat_list

    @classmethod
    def insert_new_cat(cls):
        # Create and insert a new cat
        connection = DataConnection()
        insert_cat_query = f"INSERT INTO {Cat.cat_table_name}({Cat.cat_name_column_name}, " \
                           f"{Cat.cat_color_column_name},{Cat.cat_breed_column_name}, " \
                           f"{Cat.cat_birthday_column_name}) VALUES(?, ?, ?, ?);"

        arguments = Cat.get_args_to_add_cat()

        connection.update_data(insert_cat_query, arguments)

        connection.close_connection()

    @classmethod
    def get_args_to_add_cat(cls):

        arguments = []
        print("Time to add a new cat!")
        print("...")
        arguments.append(input("Cat Name: "))
        arguments.append(input("Cat Color: "))
        arguments.append(input("Cat Breed: "))
        arguments.append(input("Cat Birthday(YYYY-MM-DD): "))

        return arguments

    @classmethod
    def add_cat_ownership(cls):
        # adding ownership to a cat
        connection = DataConnection()

        ownership_query = f"INSERT INTO {Cat.ownership_table_name}({Cat.cat_id_column_name}, " \
                          f"{Owner.owner_id_column_name}) VALUES(?, ?);"

        print("Select Cat to add ownership to")
        cat = Cat.select_cat(connection)
        print("Select Owner")
        owner = Owner.select_an_owner(connection)

        arguments = [cat.cat_id, owner.primary_key]

        if cat != -1 and owner != -1:
            print("Ownership established!")
            connection.run_query(ownership_query, arguments)
        else:
            print("Ownership assignment cancelled!")

        connection.close_connection()

    @classmethod
    def select_cat(cls, connection):
        cat_list = Cat.get_list_of_all_cats(connection)
        cat_to_select = Utilities.make_a_selection(cat_list, "Cat")
        return cat_to_select

    @classmethod
    def checkin_cat_to_room(cls):
        connection = DataConnection()

        print("Time to check in a Cat!")

        selected_cat = Cat.select_cat(connection)

        print("Select Room for Cat")
        print()
        current_rooms_capacity_list = Room.get_valid_openings_room_list(connection)

        done = False
        if selected_cat == -1:
            print("Check In Cancelled!")
            done = True

        while not done:
            selected_room = Room.select_a_room(current_rooms_capacity_list)
            if selected_room == -1:
                print("Check In Cancelled!")
                done = True
            elif selected_room.room_capacity == 0:
                print("No more space left in that room, please select another")
            else:
                checkout_date = Utilities.get_valid_checkout_date()
                if checkout_date != -1:
                    Book.check_in_cat(connection, selected_room, selected_cat, checkout_date)
                else:
                    print("Check In Cancelled!")
                done = True

    @classmethod
    def update_cat_checkout_date(cls):

        connection = DataConnection()
        active_cats_with_bookings = Cat.get_active_booked_cats_and_bookings(connection)
        just_active_cats = []
        selected_booking = ""

        print("Prepare to update Cat's checkout date!")

        for cats_books in active_cats_with_bookings:
            just_active_cats.append(cats_books[0])

        selected_cat = Utilities.make_a_selection(just_active_cats, "Cat")

        for cats_books in active_cats_with_bookings:
            if cats_books[0] == selected_cat:
                selected_booking = cats_books[1]

        valid_date = Utilities.get_valid_checkout_date()

        Book.update_book_checkout_date(connection, selected_booking.book_id, valid_date)

    @classmethod
    def get_active_booked_cats_and_bookings(cls, connection):

        active_bookings = Book.get_active_bookings(connection)
        cats = Cat.get_list_of_all_cats(connection)
        active_cats_and_bookings_list = []
        for book in active_bookings:
            for cat in cats:
                if book.cat_id == cat.cat_id:
                    active_cats_and_bookings_list.append([cat, book])

        return active_cats_and_bookings_list

    @classmethod
    def make_choice_with_cats(cls):

        possible_cat_choices = ["Display all Cats", "Insert New Cat", "Add Owner to Cat",
                                "Check in Cat", "Update Existing Cat Checkout Date", "Exit"]
        amt_of_selections = len(possible_cat_choices)

        done = False
        while not done:
            print("What would you like to do with Owners today?")
            print()

            index = 1
            for option in possible_cat_choices:
                print(f"{index}) {option}")
                index += 1

            try:
                selection = int(input("Make a selection: ")) - 1
                print()

                if amt_of_selections > selection >= 0:
                    if selection == amt_of_selections - 1:
                        done = True
                    else:
                        Cat.do_selection(possible_cat_choices[selection])

                else:
                    print("Error: not a valid selection")
            except ValueError:
                print("Error: selection not a valid int")

    @classmethod
    def do_selection(cls, string):
        if string == "Display all Cats":
            Cat.display_all_cats()
        elif string == "Insert New Cat":
            Cat.insert_new_cat()
        elif string == "Add Owner to Cat":
            Cat.add_cat_ownership()
        elif string == "Check in Cat":
            Cat.checkin_cat_to_room()
        elif string == "Update Existing Cat Checkout Date":
            Cat.update_cat_checkout_date()




