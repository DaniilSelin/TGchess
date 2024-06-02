from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from telegram.ext import InlineQueryHandler, CallbackQueryHandler, filters, ConversationHandler
from telegram.ext import ChosenInlineResultHandler, CommandHandler, ApplicationBuilder, ContextTypes, Updater, \
    MessageHandler

import Chess
from keyboard_default import keyboard_default, keyboard_empty
from copy import deepcopy
from Chess import *
# прикольная библеотека для создания простеньких классов
from enum import Enum

draw_black = {
    "King": "○",
    "Queen": "◇",
    "Rook": "▢",
    "Bishop": "△",
    "Knight": "▽",
    "Pown": "◎",
}

draw_white = {
    "King": "⬤",
    "Queen": "◆",
    "Rook": "■",
    "Bishop": "▲",
    "Knight": "▼",
    "Pown": "◉",
}

game = {}

count = 0


# Функция для получения символа фигуры по ее типу и цвету
def get_symbol(piece_type, color) -> str:
    if color != 1:
        return draw_black[piece_type]
    else:
        return draw_white[piece_type]


def Redraw_Board(engine, /, swap_pown = 0):
    board = engine.board

    keyboard_now = []
    # Проходим по всем клеткам доски и заполняем их символами фигур
    for y in range(8):
        row = []
        for x in range(8):
            symbol = " "  # По умолчанию пустая клетка
            pos_fig = engine.search_board([y, x])
            if pos_fig is None:
                engine.status_game *= -1
                pos_fig = engine.search_board([y, x])
                engine.status_game *= -1

            if pos_fig is not None:
                # Проверяем наличие фигуры на данной позиции
                symbol = get_symbol(pos_fig.gettype, pos_fig.color)
            row.append(InlineKeyboardButton(symbol, callback_data=f'{y},{x}'))

        keyboard_now.append(row)
    if engine.status_mate == 1:
        keyboard_now.append([InlineKeyboardButton(text=f'Mate! Adios!', callback_data="Mate")])

    elif engine.status_pat == 1:
        keyboard_now.append([InlineKeyboardButton(text="This is Pat the fucking loser", callback_data="Pat")])

    elif engine.status_check == 1:
        keyboard_now.append([InlineKeyboardButton(text="Is this really the check?", callback_data="Mate")])

    elif swap_pown == 1:
        if engine.status_game != 1:
            keyboard_now.append([InlineKeyboardButton(text="◇", callback_data="Queen"),
                                 InlineKeyboardButton(text="▽", callback_data="Knight"),
                                 InlineKeyboardButton(text="▢", callback_data="Rook"),
                                 InlineKeyboardButton(text="△", callback_data="Bishop"),
                                 ])
        else:
            keyboard_now.append([InlineKeyboardButton(text="◆", callback_data="Queen"),
                                 InlineKeyboardButton(text="▼", callback_data="Knight"),
                                 InlineKeyboardButton(text="■", callback_data="Rook"),
                                 InlineKeyboardButton(text="▲", callback_data="Bishop"),
                                 ])

    else:
        keyboard_now.append([InlineKeyboardButton(text="Nothing interesting", callback_data="Nothing")])

    board = InlineKeyboardMarkup(keyboard_now)

    return board


def Construct_Board() -> Chess.Board:
    black_stuff = [0] * 16
    for i in range(8):
        black_stuff[i] = Pawn([6, i], -1)

    black_stuff[8] = Rook([7, 0], -1)
    black_stuff[9] = Rook([7, 7], -1)

    black_stuff[10] = Knight([7, 1], -1)
    black_stuff[11] = Knight([7, 6], -1)
    black_stuff[12] = Bishop([7, 2], -1)
    black_stuff[13] = Bishop([7, 5], -1)
    black_stuff[14] = Queen([7, 3], -1)
    black_stuff[15] = King([7, 4], -1)

    white_stuff = [0] * 16
    for i in range(8):
        white_stuff[i] = Pawn([1, i], 1)

    white_stuff[8] = Rook([0, 0], 1)
    white_stuff[9] = Rook([0, 7], 1)
    white_stuff[10] = Knight([0, 1], 1)
    white_stuff[11] = Knight([0, 6], 1)
    white_stuff[12] = Bishop([0, 2], 1)
    white_stuff[13] = Bishop([0, 5], 1)
    white_stuff[14] = Queen([0, 3], 1)
    white_stuff[15] = King([0, 4], 1)

    engine = Board(black_stuff, white_stuff)
    engine.build()
    return engine


class Struct():
    def __init__(self, message_id):
        self.message_id = message_id
        self.users_id = {}
        self.users_state = {}
        self.users_color = {}
        self.figure = Rook([0, 0], 1)
        self.keyboard = deepcopy(keyboard_default)
        self.activ_user = 0  # start state for users
        self.position_transformation = 0
        self.engine = Construct_Board()

    def __len__(self):
        return len(self.users_id) #лучше kexit
    def get_first(self):
        key = next(iter(self.users_id))
        value = self.users_id[key]
        return key, value

# состояния
class State(Enum):
    CHOICE_FIGURE, CHOICE_MOVE, MOVE, MOVE_OPP, CHOICE_TRANS = range(5);


async def chess(update: Updater, context: ContextTypes.DEFAULT_TYPE) -> None:
    global inline_results, active_game, count
    count += 1
    query_struct = update.inline_query

    # требуется массив сосбсна кнопок, у нас он уже типо есть,
    result = [
        InlineQueryResultArticle(
            id=f'{query_struct.from_user.id}',
            title='Шахматы',
            input_message_content=InputTextMessageContent(
                "Ожидание игроков"
            ),
            description="Игра в шахматы с другом",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Присоединиться к игре [0/2]", callback_data='Get Second')]]
            ),
        )]

    await update.inline_query.answer(result)


async def button(update: Updater, context: ContextTypes.DEFAULT_TYPE) -> None:
    global active_game
    # хонест май реакгн на обезьянью активность в чате
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_name = query.from_user.username
    message_id = query.inline_message_id

    if message_id not in game:
        print(user_id)
        game[message_id] = Struct(message_id)

        game[message_id].users_id[user_id] = user_name
        game[message_id].users_color[user_id] = 1
        #game[message_id].users_id[1580208131] = "Gooon04"

        input_message_content = "@" + str(user_name) + " ждёт оппонента..."
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                "Присоединиться к игре [1/2]", callback_data='Get Second')]]
        )

        await query.edit_message_text(input_message_content, reply_markup=markup)

    elif len(game[message_id]) == 1:
        first_id, first_name = game[message_id].get_first()

        if user_id != first_id:

            game[message_id].users_id[user_id] = user_name

            game[message_id].active_user = user_id

            game[message_id].users_state[user_id] = State.CHOICE_FIGURE
            game[message_id].users_state[first_id] = State.CHOICE_FIGURE

            game[message_id].users_color[user_id] = -1

            input_message_content = f'@{first_name} vs @{user_name}'
            board = InlineKeyboardMarkup(deepcopy(keyboard_default))

            await query.edit_message_text(input_message_content, reply_markup=board)
        else:
            return None
    else:
        # State = Game
        Game_Now = game[message_id]
        print(Game_Now.users_state)
        first_id, second_id = game[message_id].users_id.keys()

        if user_id != first_id and user_id != second_id:
            return None

        if user_id != Game_Now.active_user:
            return None

        if Game_Now.users_state[user_id] == State.CHOICE_FIGURE:
            position_figure = query.data

            figure_check_color = Game_Now.engine.search_board([int(position_figure[0]), int(position_figure[2])])

            if figure_check_color is not None:

                if figure_check_color.color == Game_Now.users_color[user_id]:
                    Game_Now.figure = figure_check_color
                else:
                    return None

                Game_Now.users_state[user_id] = State.CHOICE_MOVE

            else :
                return None

        elif Game_Now.users_state[user_id] == State.CHOICE_MOVE:
            position_move = query.data
            position_move = [int(position_move[0]), int(position_move[2])]

            if Game_Now.figure.gettype == "Pown":
                if position_move[0] == 7 or position_move[0] == 0:
                    Game_Now.users_state[user_id] = State.CHOICE_TRANS
                    Game_Now.keyboard = Redraw_Board(Game_Now.engine, swap_pown=1)
                    input_message_content = f'Choice the figure, @{Game_Now.users_id[user_id]}'

                    await query.edit_message_text(text=input_message_content, reply_markup=Game_Now.keyboard)
                    Game_Now.position_transformation = position_move
                    return None
            print(Game_Now.users_state)



            interactive_motion = Game_Now.figure.motion(Game_Now.engine)

            if position_move in interactive_motion:

                Game_Now.figure.interactive(
                    [position_move[0], position_move[1]],
                    Game_Now.figure.position,
                    Game_Now.engine,
                )

                # перерисовываем нашу доску согласно плану на доске в engine
                Game_Now.keyboard = Redraw_Board(Game_Now.engine)

                #Game_Now.engine.status_game *= -1

                for user_new_active in Game_Now.users_state.keys():
                    if user_id != user_new_active:
                        Game_Now.active_user = user_new_active
                        input_message_content = f' @{Game_Now.users_id[user_id]} is waiting for the @{Game_Now.users_id[user_new_active]} move'

                Game_Now.users_state[
                    Game_Now.active_user
                ] = State.CHOICE_FIGURE

                Game_Now.users_state[user_id] = State.MOVE_OPP

                await query.edit_message_text(text= input_message_content, reply_markup=Game_Now.keyboard)

            else:
                Game_Now.users_state[user_id] = State.CHOICE_FIGURE

        elif Game_Now.users_state[user_id] == State.CHOICE_TRANS:

            transformation = query.data

            if len(transformation) <= 3:
                Game_Now.users_state[user_id] = State.CHOICE_FIGURE
                Game_Now.keyboard = Redraw_Board(Game_Now.engine)
                for user_new_active in Game_Now.users_state.keys():
                    if user_id != user_new_active:
                        input_message_content = f' @{Game_Now.users_id[user_new_active]} is waiting for the @{Game_Now.users_id[user_id]} move'
                await query.edit_message_text(text= input_message_content, reply_markup=Game_Now.keyboard)
                return None

            position_move = Game_Now.position_transformation

            #interactive_motion = Game_Now.figure.motion(Game_Now.engine)

            Game_Now.figure.interactive(
                [position_move[0], position_move[1]],
                Game_Now.figure.position,
                Game_Now.engine,
                figure_im= transformation
            )

            Game_Now.keyboard = Redraw_Board(Game_Now.engine)

            for user_new_active in Game_Now.users_state.keys():
                if user_id != user_new_active:
                    Game_Now.active_user = user_new_active
                    input_message_content = f' @{Game_Now.users_id[user_id]} is waiting for the @{Game_Now.users_id[user_new_active]} move'

            Game_Now.users_state[
                Game_Now.active_user
            ] = State.CHOICE_FIGURE

            Game_Now.users_state[user_id] = State.MOVE_OPP

            await query.edit_message_text(text=input_message_content, reply_markup=Game_Now.keyboard)



TOKEN = "5863452591:AAFsAS4rN_RZ-exh0mX7C1-PHWCEB-YZd68"
# создание экземпляра бота через `ApplicationBuilder`
application = ApplicationBuilder().token(TOKEN).build()

inline_caps_handler = InlineQueryHandler(callback=chess)
application.add_handler(inline_caps_handler)

application.add_handler(CallbackQueryHandler(callback=button, block=False))

application.run_polling(poll_interval=0.1)
"""
cow_handler = ConversationHandler(
    states= {

    }
)
"""
# командный обработчки, буквально для \command...
# telegram.ext.CommandHandler(command, callback, filters=None, block=True, has_args=None)
# command первый аргумент образует лист, содержащий список строк следующих за командо, то бишь за \
# чтобы игнорить редакт сообщения в атрибут filter пихаем ~filters.UpdateType.EDITED_MESSAGE
# второй аргумент callback - Будет вызвана, когда check_update() определит, что обновление должно быть обработано этим обработчиком.
# можно поставить блок на дальнейшую работу вроде как потока при помощи атрибута block (bool, optional).
# https://docs.python-telegram-bot.org/en/stable/telegram.ext.commandhandler.html
# start_handler = CommandHandler(command= 'start',callback= start)
# метод класс для добавления нового хендлера, порядок важен!
# application.add_handler(start_handler)

# https://docs.python-telegram-bot.org/en/stable/telegram.ext.inlinequeryhandler.html
# telegram.ext.InlineQueryHandler(callback, pattern=None, block=True, chat_types=None)
# для настройки на определенные события юзай атрибут pattern


# telegram.ext.CallbackQueryHandler(callback, pattern=None, block=True)
# callback - вызывается когда решит update, который хрен пойии как работает
# бесполезный хендлер


# telegram.ext.MessageHandler(filters, callback, block=True)sdfsds
# самый такой стандартный хенлдлер, обрбатывает станардтные сообщения и тп
# https://docs.python-telegram-bot.org/en/stable/telegram.ext.filters.html - полехные фильтры
# https://docs.python-telegram-bot.org/en/stable/telegram.ext.messagehandler.html -class hendler
# unknown_handler = MessageHandler(filters= filters.ALL, callback= unknown)
# application.add_handler(unknown_handler)

# по сути telegram.ext.Updater.start_polling(), то бишь просто упрощенный вариант
# использования updater...
# ту можно посмотреть то, через какие костыли он запускается - https://docs.python-telegram-bot.org/en/stable/telegram.ext.application.html
