from SimpleDataSource import SimpleDataSource


class DataConnection:

    def __init__(self):
        self.connection = SimpleDataSource.get_connection()

    def run_query(self, query, arguments=None):
        if arguments is None:
            arguments = []
        cursor = self.connection.cursor()
        result_set = cursor.execute(query, arguments)
        return result_set

    def update_data(self, query, arguments=None):
        if arguments is None:
            arguments = []
        cursor = self.connection.cursor()
        cursor.execute(query, arguments)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
