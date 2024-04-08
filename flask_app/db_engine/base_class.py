from abc import ABC, abstractmethod


class DBBaseClass(ABC):
    @abstractmethod
    def get_db_connection(self, **kwargs):
        "DB Connection"

    @abstractmethod
    def execute_query(self, **kwargs):
        "Method to execute Query"
