class TgCommand:
    HELP = "help"
    KARMA = "my_karma"
    ALL_KARMA = "karma"
    MUTE = "mute"

    @staticmethod
    def get_list_for():
        return f'\n\t!{TgCommand.HELP} - выводит список команд' \
               f'\n\t!{TgCommand.KARMA} - показывает вашу карму' \
               f'\n\t!{TgCommand.ALL_KARMA} - показывает карму у всех, у кого она > 0'
