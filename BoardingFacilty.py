from Owner import Owner
from Cat import Cat


def main():
    # print welcome tab
    print("--Welcome to Cat Boarding LLC Owner Management Software--")
    print()

    choices = ["View all Owners", "Add a new Owner", "Delete current Owner",
               "Update current Owner address", "Other Functionality", "Exit"]

    make_selection_and_execute(choices)


def make_selection_and_execute(choices):

    amt_of_selections = len(choices)
    done = False
    while not done:
        print("What would you like to do with Owners today?")
        print()

        # print selection interface
        index = 1
        for option in choices:
            print(f"{index}) {option}")
            index += 1

        # error handling to ensure int and valid selection
        try:
            selection = int(input("Make a selection: ")) - 1
            print()

            if amt_of_selections > selection >= 0:
                # if selection is Exit, exit the loop
                if selection == amt_of_selections - 1:
                    print("Thank You, Good Bye")
                    done = True
                else:
                    execute_selected_choice(choices[selection])

            else:
                print("Error: not a valid selection")
        except ValueError:
            print("Error: selection not a valid int")


def execute_selected_choice(choice_string):
    # checking choice, running the appropriate function
    if choice_string == "View all Owners":
        Owner.display_all_owners()
    elif choice_string == "Add a new Owner":
        Owner.add_owner()
    elif choice_string == "Delete current Owner":
        Owner.delete_owner()
    elif choice_string == "Update current Owner address":
        Owner.update_owner_address()
    elif choice_string == "Other Functionality":
        Cat.make_choice_with_cats()


if __name__ == "__main__":
    main()


# Main Functionality Programmed

# Cat functions

# display_all_cats()
# insert_new_cat()
# add_cat_ownership()
# checkin_cat_to_room()
# update_cat_checkout_date()

# Owner functions

# Owner.display_all_owners()
# Owner.add_owner()
# Owner.delete_owner()
# Owner.update_owner_address()
