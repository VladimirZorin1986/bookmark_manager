import sys
import typing as t
from abc import ABCMeta, abstractmethod
from datetime import datetime
from database.db_manager import DatabaseManager
from database.db_config import DB_NAME
import requests


db = DatabaseManager(DB_NAME)


def get_info(data: dict[str, str], is_need_timestamp) -> tuple[dict[str, str], t.Optional[str]]:
    return {
        'title': data['name'],
        'url': data['html_url'],
        'notes': data.get('description')
    }, data['created_at'] if is_need_timestamp else None


class Command(metaclass=ABCMeta):
    """
    Base class for implementing Command Pattern
    """
    @abstractmethod
    def execute(self, *args, **kwargs) -> t.Any:
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
    def execute(self, data: dict[str, str], timestamp: t.Optional[datetime] = None) -> str:
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
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


class ImportGithubStarsCommand(Command):
    """
    Imports stared bookmarks from Github
    Implements Command Pattern
    """
    def execute(self, data: dict[str, t.Union[str, bool]]):
        add_command = AddBookmarkCommand()
        bookmarks = requests.get(f'https://api.github.com/users/{data["username"]}/starred').json()
        bookmarks_count = len(bookmarks)
        for bookmark_info in bookmarks:
            add_command.execute(*get_info(bookmark_info, data['is_save_timestamp']))
        return f'Imported {bookmarks_count} bookmarks from starred repos!'




