from telethon.tl.types import User
from full_name import get_full_name


class TgCommand:
    JUST_HELP = "/help"
    HELP = "/karma_help"
    KARMA = "/my_karma"
    ALL_KARMA = "/all_karma"

    @staticmethod
    def get_list_for(sender: User):
        return f'{get_full_name(sender)}, вот мои команды:' \
               f'\n\t{TgCommand.HELP} - выводит список команд' \
               f'\n\t{TgCommand.KARMA} - показывает вашу карму' \
               f'\n\t{TgCommand.ALL_KARMA} - показывает карму у всех, у кого она > 0'
