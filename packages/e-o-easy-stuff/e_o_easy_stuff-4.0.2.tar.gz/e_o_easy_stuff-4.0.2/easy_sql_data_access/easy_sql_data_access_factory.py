from easy_sql_data_access.easy_open_data_connection import easy_open_data_connection
from easy_sql_data_access.easy_sql_data_access import EasySQLDataAccess


class EasySQLDataAccessFactory:
    def __init__(self, constr: str):
        self.constr = constr

    @staticmethod
    def init_using_credentials(server: str, database: str, username: str, password: str):
        constr = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server={server};"
            f"Database={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Authentication=ActiveDirectoryPassword;"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        return EasySQLDataAccessFactory(constr)

    def open_data_access(self, autocommit: bool = True) -> EasySQLDataAccess:
        with easy_open_data_connection(self.constr, autocommit) as con:
            return EasySQLDataAccess(con)

    @staticmethod
    def open_data_access_using_connection(con):
        return EasySQLDataAccess(con)
