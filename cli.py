import os
import typing as t
import commands
from option import Option


def get_user_input(label: str, required=True) -> t.Optional[str]:
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def convert_input_to_bool(inp):
    return inp.lower() == 'y'


def get_new_bookmark_data() -> dict[str, t.Optional[str]]:
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }


def get_bookmark_id_for_deletion() -> int:
    return int(get_user_input('Enter a bookmark ID to delete'))


def get_github_stars_info():
    return {
        'username': get_user_input('Github username'),
        'is_save_timestamp': convert_input_to_bool(get_user_input('Save original timestamp [Y/N]: '))
    }


OPTIONS = {
    'A': Option('Add bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
    'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
    'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
    'D': Option('Delete bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
    'G': Option('Import Github stars', commands.ImportGithubStarsCommand(), prep_call=get_github_stars_info),
    'Q': Option('Quit', commands.QuitCommand())
}


def print_options(options: dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def get_option_choice() -> Option:
    while (choice := input('Choose option: ').upper()) not in OPTIONS:
        print('Invalid choice. Try again...')
    return OPTIONS.get(choice)


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop():
    clear_screen()
    print_options(OPTIONS)
    chosen_option = get_option_choice()
    chosen_option.choose()
    _ = input('Click Enter to return to main menu...')


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()




