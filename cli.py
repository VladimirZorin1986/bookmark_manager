import commands
from option import Option


OPTIONS = {
    'A': Option('Add bookmark', commands.AddBookmarkCommand()),
    'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
    'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
    'D': Option('Delete bookmark', commands.DeleteBookmarkCommand()),
    'Q': Option('Quit', commands.QuitCommand())
}


def print_options(options: dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def get_option_choice() -> Option:
    while (choice := input().upper()) not in OPTIONS:
        print('Invalid choice. Try again...')
    return OPTIONS.get(choice)


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()
    print_options(OPTIONS)
    chosen_option = get_option_choice()
    print(chosen_option.choose())



