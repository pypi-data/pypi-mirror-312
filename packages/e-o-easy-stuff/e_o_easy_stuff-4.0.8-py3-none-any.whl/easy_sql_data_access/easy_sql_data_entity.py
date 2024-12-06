from typing import Generic, TypeVar

from easy_sql_data_access.easy_sql_data_access_factory import EasySQLDataAccessFactory

T = TypeVar('T')


class EasySQLDataEntity(Generic[T]):
    def __init__(self, data_access_factory: EasySQLDataAccessFactory, table_name: str, id_column_name: str = "Id"):
        self.data_access_factory = data_access_factory
        self.table_name = table_name
        self.id_column_name = id_column_name
        pass

    def update(self, id: any, entity: T):
        sql = f"UPDATE {self.table_name} SET " + ', '.join(
            [f"{key} = ?" for key in entity.keys()]) + f" WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, tuple(entity.values()) + (id,))

        pass

    def patch(self, id: any, entity: dict[str, any]):
        sql = f"UPDATE {self.table_name} SET " + ', '.join(
            [f"{key} = ?" for key in entity.keys()]) + f" WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, tuple(entity.values()) + (id,))

        pass

    def insert(self, entity: T):
        sql = f"INSERT INTO {self.table_name} ({', '.join(entity.keys())}) VALUES ({', '.join(['?' for _ in entity.keys()])})"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, tuple(entity.values()))

        pass

    def delete(self, id: any):
        sql = f"DELETE FROM {self.table_name} WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            data_access.execute_with_parameters(sql, (id,))

        pass

    def get_list(self) -> list[T]:
        sql = f"SELECT * FROM {self.table_name}"
        with self.data_access_factory.open() as data_access:
            return data_access.query_list_dict(sql)

    def get_list_with_filters(self, filters: dict[str, any]) -> list[T]:
        sql = f"SELECT * FROM {self.table_name} WHERE " + ' AND '.join([f"{key} = ?" for key in filters.keys()])
        with self.data_access_factory.open() as data_access:
            return data_access.query_list_dict(sql)

    def get(self, id: any) -> T:
        sql = f"SELECT * FROM {self.table_name} WHERE {self.id_column_name} = ?"
        with self.data_access_factory.open() as data_access:
            return data_access.query_list_dict(sql, (id,))[0]

        pass

    def get_with_filters(self, filters: dict[str, any]) -> T:
        sql = f"SELECT * FROM {self.table_name} WHERE " + ' AND '.join([f"{key} = ?" for key in filters.keys()])
        with self.data_access_factory.open() as data_access:
            return data_access.query_list_dict(sql, tuple(filters.values()))[0]

        pass
