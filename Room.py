from Book import Book
from Utilities import Utilities


class Room:
    # table names
    room_table_name = "dbo.Room"
    check_in_table_name = "dbo.Check_In"

    # column names
    room_id_column_name = "Room_ID"
    room_name_column_name = "Room_Name"
    room_capacity_column_name = "Room_Capacity"

    def __init__(self, room_id, room_name, room_capacity):
        self.room_id = room_id
        self.room_name = room_name
        self.room_capacity = room_capacity
        self.full = False

    @classmethod
    def get_room_list(cls, connection):

        get_room_list_query = f"SELECT {Room.room_id_column_name}, {Room.room_name_column_name}, " \
                              f"{Room.room_capacity_column_name} " \
                              f"FROM {Room.room_table_name} " \
                              f"ORDER BY {Room.room_id_column_name}"

        room_attribute_list = connection.run_query(get_room_list_query)
        room_list = []

        for row in room_attribute_list:
            room = Room(row[0], row[1], row[2])
            room_list.append(room)

        return room_list

    @classmethod
    def get_valid_openings_room_list(cls, connection):

        room_list = Room.get_room_list(connection)

        active_bookings_list = Book.get_active_bookings(connection)

        for room in room_list:
            for book in active_bookings_list:
                if room.room_id == book.room_id:
                    room.room_capacity -= 1

        return room_list

    @classmethod
    def select_a_room(cls, current_rooms_list):
        room_to_select = Utilities.make_a_selection(current_rooms_list, "Room")
        return room_to_select
