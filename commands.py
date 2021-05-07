import sys
from typing import Any
from abc import ABCMeta, abstractmethod
from datetime import datetime
from database.db_manager import DatabaseManager
from database.db_config import DB_NAME


db = DatabaseManager(DB_NAME)


class Command(metaclass=ABCMeta):
    """
    Base class for implementing Command Pattern
    """
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        ...


class CreateBookmarksTableCommand(Command):
    """
    Command for create table bookmarks in database
    Implements Command Pattern
    """
    def execute(self) -> None:
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null'
        })


class AddBookmarkCommand(Command):
    """
    Command for adding new bookmark in database
    Implements Command Pattern
    """
    def execute(self, data: dict[str, str]) -> str:
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added successfully!'


class ListBookmarksCommand(Command):
    """
    Command for output the list of existing bookmarks
    Implements Command Pattern
    """
    def __init__(self, order_by: str = 'date_added') -> None:
        self._order_by = order_by

    def execute(self) -> list:
        return db.select('bookmarks', order_by_clause=self._order_by).fetchall()


class DeleteBookmarkCommand(Command):
    """
    Command for delete bookmark info
    Implements Command Pattern
    """
    def execute(self, data: int) -> str:
        db.delete('bookmarks', {'id': data})
        return 'Bookmark was deleted successfully!'


class QuitCommand(Command):
    """
    Immediately quits application
    Implements Command Pattern
    """
    def execute(self):
        sys.exit()



