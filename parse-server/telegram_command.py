from telethon.tl.types import User


class TCommand:
    JUST_HELP = "/help"
    HELP = "/karma_help"
    KARMA = "/my_karma"
    ALL_KARMA = "/all_karma"

    @staticmethod
    def get_list_for(sender: User):
        return f'{sender.first_name}, вот мои команды:' \
               f'\n\t{TCommand.HELP} - выводит список команд' \
               f'\n\t{TCommand.KARMA} - показывает вашу карму' \
               f'\n\t{TCommand.ALL_KARMA} - показывает карму у всех, у кого она > 0'
