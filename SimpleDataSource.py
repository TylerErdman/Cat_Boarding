import pyodbc


class SimpleDataSource:

    @classmethod
    def get_connection(cls):

        return pyodbc.connect('DRIVER={SQL Server}; SERVER=localhost; DATABASE=Cat_Boarding')
