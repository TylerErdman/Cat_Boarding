
class Book:

    # table name
    book_table_name = "dbo.Book"

    # column names
    book_book_id_column_name = "Book_ID"
    book_cat_id_column_name = "Cat_ID"
    book_room_id_column_name = "Room_ID"
    book_check_in_column_name = "Check_In"
    book_check_out_column_name = "Check_Out"

    def __init__(self, book_id, cat_id, room_id, check_in, check_out):
        self.book_id = book_id
        self.cat_id = cat_id
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out

    @classmethod
    def get_active_bookings(cls, connection):
        get_active_bookings_query = f"Select {Book.book_book_id_column_name}, {Book.book_cat_id_column_name}, " \
                                    f"{Book.book_room_id_column_name}, {Book.book_check_in_column_name}, " \
                                    f"{Book.book_check_out_column_name} " \
                                    f"From {Book.book_table_name} " \
                                    f"WHERE {Book.book_check_in_column_name} < GETDATE() AND " \
                                    f"GETDATE() < {Book.book_check_out_column_name};"
        active_bookings_list = []

        book_attribute_list = connection.run_query(get_active_bookings_query)

        for row in book_attribute_list:
            book = Book(row[0], row[1], row[2], row[3], row[4])
            active_bookings_list.append(book)

        return active_bookings_list

    @classmethod
    def get_full_book_list(cls, connection):

        book_full_table_query = f"Select {Book.book_book_id_column_name}, {Book.book_cat_id_column_name}, " \
                               f"{Book.book_room_id_column_name}, {Book.book_check_in_column_name}, " \
                               f"{Book.book_check_out_column_name} " \
                               f"From {Book.book_table_name} " \
                               f"ORDER BY {Book.book_book_id_column_name};"

        booking_attributes = connection.run_query(book_full_table_query)
        booking_list = []

        for row in booking_attributes:
            book_record = Book(row[0], row[1], row[2], row[3], row[4])
            booking_list.append(book_record)

        return booking_list

    @classmethod
    def check_in_cat(cls, connection, selected_room, selected_cat, checkout_date):
        cat_checked_in_query = f"INSERT INTO {Book.book_table_name}({Book.book_cat_id_column_name}, " \
                               f"{Book.book_room_id_column_name}, {Book.book_check_out_column_name}) " \
                               f"VALUES(?, ?, ?)"

        arguments = [selected_cat.cat_id, selected_room.room_id, checkout_date]
        connection.update_data(cat_checked_in_query, arguments)

    @classmethod
    def update_book_checkout_date(cls, connection, book_id, new_checkout_date):
        update_booking_checkout_date_query = f"UPDATE {Book.book_table_name} " \
                                             f"SET {Book.book_check_out_column_name} = '{new_checkout_date}' " \
                                             f"WHERE {Book.book_book_id_column_name} = {book_id};"
        connection.update_data(update_booking_checkout_date_query)
