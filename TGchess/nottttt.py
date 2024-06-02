from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import InlineQueryHandler, CallbackQueryHandler, filters
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, Updater, MessageHandler

async def start(update, context):
    # ожидание отправки сообщения по сети - нужен `await`
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Используйте инлайн-запрос для начала игры!")

async def button(update, context):

    query = update.callback_query
    print(update.callback_query['data'])
    await query.answer(text="Некуда присоединяться! Шахмат ещё нет!")
    keyboard = [
        [InlineKeyboardButton("♖", callback_data='a8'), InlineKeyboardButton("♘", callback_data='b8'),
         InlineKeyboardButton("♗", callback_data='c8'), InlineKeyboardButton("♕", callback_data='d8'),
         InlineKeyboardButton("♔", callback_data='e8'), InlineKeyboardButton("♗", callback_data='f8'),
         InlineKeyboardButton("♘", callback_data='g8'), InlineKeyboardButton("♖", callback_data='h8')],
        [InlineKeyboardButton("♟", callback_data='a7'), InlineKeyboardButton("♟", callback_data='b7'),
         InlineKeyboardButton("♟", callback_data='c7'), InlineKeyboardButton("♟", callback_data='d7'),
         InlineKeyboardButton("♟", callback_data='e7'), InlineKeyboardButton("♟", callback_data='f7'),
         InlineKeyboardButton("♟", callback_data='g7'), InlineKeyboardButton("♟", callback_data='h7')],
        [InlineKeyboardButton(" ", callback_data='a6'), InlineKeyboardButton(" ", callback_data='b6'),
         InlineKeyboardButton(" ", callback_data='c6'), InlineKeyboardButton(" ", callback_data='d6'),
         InlineKeyboardButton(" ", callback_data='e6'), InlineKeyboardButton(" ", callback_data='f6'),
         InlineKeyboardButton(" ", callback_data='g6'), InlineKeyboardButton(" ", callback_data='h6')],
        [InlineKeyboardButton(" ", callback_data='a5'), InlineKeyboardButton(" ", callback_data='b5'),
         InlineKeyboardButton(" ", callback_data='c5'), InlineKeyboardButton(" ", callback_data='d5'),
         InlineKeyboardButton(" ", callback_data='e5'), InlineKeyboardButton(" ", callback_data='f5'),
         InlineKeyboardButton(" ", callback_data='g5'), InlineKeyboardButton(" ", callback_data='h5')],
        [InlineKeyboardButton(" ", callback_data='a4'), InlineKeyboardButton(" ", callback_data='b4'),
         InlineKeyboardButton(" ", callback_data='c4'), InlineKeyboardButton(" ", callback_data='d4'),
         InlineKeyboardButton(" ", callback_data='e4'), InlineKeyboardButton(" ", callback_data='f4'),
         InlineKeyboardButton(" ", callback_data='g4'), InlineKeyboardButton(" ", callback_data='h4')],
        [InlineKeyboardButton(" ", callback_data='a3'), InlineKeyboardButton(" ", callback_data='b3'),
         InlineKeyboardButton(" ", callback_data='c3'), InlineKeyboardButton(" ", callback_data='d3'),
         InlineKeyboardButton(" ", callback_data='e3'), InlineKeyboardButton(" ", callback_data='f3'),
         InlineKeyboardButton(" ", callback_data='g3'), InlineKeyboardButton(" ", callback_data='h3')],
        [InlineKeyboardButton("▪", callback_data='a2'), InlineKeyboardButton("♙", callback_data='b2'),
         InlineKeyboardButton("▪", callback_data='c2'), InlineKeyboardButton("♙", callback_data='d2'),
         InlineKeyboardButton("▪", callback_data='e2'), InlineKeyboardButton("♙", callback_data='f2'),
         InlineKeyboardButton("▪", callback_data='g2'), InlineKeyboardButton("♙", callback_data='h2')],
        [InlineKeyboardButton("■", callback_data='a1'), InlineKeyboardButton("▼", callback_data='b1'),
         InlineKeyboardButton("▲", callback_data='c1'), InlineKeyboardButton("◆", callback_data='d1'),
         InlineKeyboardButton("●", callback_data='e1'), InlineKeyboardButton("▲", callback_data='f1'),
         InlineKeyboardButton("xytq", callback_data='e109'), InlineKeyboardButton("xyq", callback_data='f198'),
         InlineKeyboardButton("▼", callback_data='g1'), InlineKeyboardButton("■", callback_data='h1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='xyй', reply_markup=reply_markup)

async def chess(update, context):
    query = update.inline_query.query
    print(update.inline_query)
    if not query:

        return
    keyboard = [
        [InlineKeyboardButton("■", callback_data='a8'), InlineKeyboardButton("▼", callback_data='b8'),
         InlineKeyboardButton("▲", callback_data='c8'), InlineKeyboardButton("◆", callback_data='d8'),
         InlineKeyboardButton("⬤", callback_data='e8'), InlineKeyboardButton("▲", callback_data='black'),
         InlineKeyboardButton("▼", callback_data='g8'), InlineKeyboardButton("■", callback_data='h8')],
        [InlineKeyboardButton("◉", callback_data='a7'), InlineKeyboardButton("◉", callback_data='b7'),
         InlineKeyboardButton("◉", callback_data='c7'), InlineKeyboardButton("◉", callback_data='d7'),
         InlineKeyboardButton("◉", callback_data='e7'), InlineKeyboardButton("◉", callback_data='f7'),
         InlineKeyboardButton("◉", callback_data='g7'), InlineKeyboardButton("◉", callback_data='h7')],
        [InlineKeyboardButton(" ", callback_data='a6'), InlineKeyboardButton(" ", callback_data='b6'),
         InlineKeyboardButton(" ", callback_data='c6'), InlineKeyboardButton(" ", callback_data='d6'),
         InlineKeyboardButton(" ", callback_data='e6'), InlineKeyboardButton(" ", callback_data='f6'),
         InlineKeyboardButton(" ", callback_data='g6'), InlineKeyboardButton(" ", callback_data='h6')],
        [InlineKeyboardButton(" ", callback_data='a5'), InlineKeyboardButton(" ", callback_data='b5'),
         InlineKeyboardButton(" ", callback_data='c5'), InlineKeyboardButton(" ", callback_data='d5'),
         InlineKeyboardButton(" ", callback_data='e5'), InlineKeyboardButton(" ", callback_data='f5'),
         InlineKeyboardButton(" ", callback_data='g5'), InlineKeyboardButton(" ", callback_data='h5')],
        [InlineKeyboardButton(" ", callback_data='a4'), InlineKeyboardButton(" ", callback_data='b4'),
         InlineKeyboardButton(" ", callback_data='c4'), InlineKeyboardButton(" ", callback_data='d4'),
         InlineKeyboardButton(" ", callback_data='e4'), InlineKeyboardButton(" ", callback_data='f4'),
         InlineKeyboardButton(" ", callback_data='g4'), InlineKeyboardButton(" ", callback_data='h4')],
        [InlineKeyboardButton(" ", callback_data='a3'), InlineKeyboardButton(" ", callback_data='b3'),
         InlineKeyboardButton(" ", callback_data='c3'), InlineKeyboardButton(" ", callback_data='d3'),
         InlineKeyboardButton(" ", callback_data='e3'), InlineKeyboardButton(" ", callback_data='f3'),
         InlineKeyboardButton(" ", callback_data='g3'), InlineKeyboardButton(" ", callback_data='h3')],
        [InlineKeyboardButton("◎", callback_data='a2'), InlineKeyboardButton("◎ ", callback_data='b2'),
         InlineKeyboardButton("◎", callback_data='c2'), InlineKeyboardButton("◎ ", callback_data='d2'),
         InlineKeyboardButton("◎", callback_data='e2'), InlineKeyboardButton("◎", callback_data='f2'),
         InlineKeyboardButton("◎", callback_data='g2'), InlineKeyboardButton("◎", callback_data='h2')],
        [InlineKeyboardButton("▢", callback_data='a1'), InlineKeyboardButton("▽", callback_data='b1'),
         InlineKeyboardButton("△", callback_data='c1'), InlineKeyboardButton("◇", callback_data='d1'),
         InlineKeyboardButton("○", callback_data='e1'), InlineKeyboardButton("△", callback_data='f1'),
         InlineKeyboardButton("▽", callback_data='g1'), InlineKeyboardButton("▢", callback_data='h1')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    results = []
    results.append(
        InlineQueryResultArticle(
            id='1',
            title='Шахматы',
            input_message_content=InputTextMessageContent("@"+str(update.inline_query['from_user']['username'])+" ждёт оппонента..."),
            description="Игра в шахматы с другом",
            reply_markup=reply_markup
        ),)
    await context.bot.answer_inline_query(update.inline_query.id, results)
    """
       board = [
           InlineQueryResultArticle(
               id="f{query_struct.from_user.id}",
               title='Шахматы',
               input_message_content=InputTextMessageContent(
                   "@" + str(update.inline_query['from_user']['username']) + " ждёт оппонента..."),
               description="Игра в шахматы с другом",
               reply_markup= InlineKeyboardMarkup(keyboard_default)
           ), ]
       active_game[query_struct.from_user.id] = deepcopy(keyboard_default)
       await update.inline_query.answer(board)"""

async def unknown(update, context):
    print(update)
    #await context.bot.send_message(chat_id=1280753537, text="xyй")

if __name__ == '__main__':

    TOKEN = "5863452591:AAFsAS4rN_RZ-exh0mX7C1-PHWCEB-YZd68"
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()

    #командный обработчки, буквально для \command...
    #telegram.ext.CommandHandler(command, callback, filters=None, block=True, has_args=None)
    #command первый аргумент образует лист, содержащий список строк следующих за командо, то бишь за \
    #чтобы игнорить редакт сообщения в атрибут filter пихаем ~filters.UpdateType.EDITED_MESSAGE
    #второй аргумент callback - Будет вызвана, когда check_update() определит, что обновление должно быть обработано этим обработчиком.
    #можно поставить блок на дальнейшую работу вроде как потока при помощи атрибута block (bool, optional).
    #https://docs.python-telegram-bot.org/en/stable/telegram.ext.commandhandler.html
    start_handler = CommandHandler(command= 'start',callback= start)
    #метод класс для добавления нового хендлера, порядок важен!
    application.add_handler(start_handler)

    #telegram.ext.CallbackQueryHandler(callback, pattern=None, block=True)
    #callback - вызывается когда решит update, который хрен пойии как работает
    application.add_handler(CallbackQueryHandler(callback= button))

    inline_caps_handler = InlineQueryHandler(chess)
    application.add_handler(inline_caps_handler)

    unknown_handler = MessageHandler(filters.ALL, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()