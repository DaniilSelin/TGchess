from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
keyboard_default = [
    [InlineKeyboardButton("■", callback_data='0,0'), InlineKeyboardButton("▼", callback_data='0,1'), InlineKeyboardButton("▲", callback_data='0,2'), InlineKeyboardButton("◆", callback_data='0,3'),
     InlineKeyboardButton("⬤", callback_data='0,4'), InlineKeyboardButton("▲", callback_data='0,5'), InlineKeyboardButton("▼", callback_data='0,6'), InlineKeyboardButton("■", callback_data='0,7')],
    [InlineKeyboardButton("◉", callback_data='1,0'), InlineKeyboardButton("◉", callback_data='1,1'), InlineKeyboardButton("◉", callback_data='1,2'), InlineKeyboardButton("◉", callback_data='1,3'),
     InlineKeyboardButton("◉", callback_data='1,4'), InlineKeyboardButton("◉", callback_data='1,5'), InlineKeyboardButton("◉", callback_data='1,6'), InlineKeyboardButton("◉", callback_data='1,7')],
    [InlineKeyboardButton(" ", callback_data='2,0'), InlineKeyboardButton(" ", callback_data='2,1'), InlineKeyboardButton(" ", callback_data='2,2'), InlineKeyboardButton(" ", callback_data='2,3'),
     InlineKeyboardButton(" ", callback_data='2,4'), InlineKeyboardButton(" ", callback_data='2,5'), InlineKeyboardButton(" ", callback_data='2,6'), InlineKeyboardButton(" ", callback_data='2,7')],
    [InlineKeyboardButton(" ", callback_data='3,0'), InlineKeyboardButton(" ", callback_data='3,1'), InlineKeyboardButton(" ", callback_data='3,2'), InlineKeyboardButton(" ", callback_data='3,3'),
     InlineKeyboardButton(" ", callback_data='3,4'), InlineKeyboardButton(" ", callback_data='3,5'), InlineKeyboardButton(" ", callback_data='3,6'), InlineKeyboardButton(" ", callback_data='3,7')],
    [InlineKeyboardButton(" ", callback_data='4,0'), InlineKeyboardButton(" ", callback_data='4,1'), InlineKeyboardButton(" ", callback_data='4,2'), InlineKeyboardButton(" ", callback_data='4,3'),
     InlineKeyboardButton(" ", callback_data='4,4'), InlineKeyboardButton(" ", callback_data='4,5'), InlineKeyboardButton(" ", callback_data='4,6'), InlineKeyboardButton(" ", callback_data='4,7')],
    [InlineKeyboardButton(" ", callback_data='5,0'), InlineKeyboardButton(" ", callback_data='5,1'), InlineKeyboardButton(" ", callback_data='5,2'), InlineKeyboardButton(" ", callback_data='5,3'),
     InlineKeyboardButton(" ", callback_data='5,4'), InlineKeyboardButton(" ", callback_data='5,5'), InlineKeyboardButton(" ", callback_data='5,6'), InlineKeyboardButton(" ", callback_data='5,7')],
    [InlineKeyboardButton("◎", callback_data='6,0'), InlineKeyboardButton("◎", callback_data='6,1'), InlineKeyboardButton("◎", callback_data='6,2'), InlineKeyboardButton("◎", callback_data='6,3'),
     InlineKeyboardButton("◎", callback_data='6,4'), InlineKeyboardButton("◎", callback_data='6,5'), InlineKeyboardButton("◎", callback_data='6,6'), InlineKeyboardButton("◎", callback_data='6,7')],
    [InlineKeyboardButton("▢", callback_data='7,0'), InlineKeyboardButton("▽", callback_data='7,1'), InlineKeyboardButton("△", callback_data='7,2'), InlineKeyboardButton("◇", callback_data='7,3'),
     InlineKeyboardButton("○", callback_data='7,4'), InlineKeyboardButton("△", callback_data='7,5'), InlineKeyboardButton("▽", callback_data='7,6'), InlineKeyboardButton("▢", callback_data='7,7')]
]

keyboard_empty = [
    [InlineKeyboardButton(" ", callback_data='0,0'), InlineKeyboardButton(" ", callback_data='0,1'), InlineKeyboardButton(" ", callback_data='0,2'), InlineKeyboardButton(" ", callback_data='0,3'),
     InlineKeyboardButton(" ", callback_data='0,4'), InlineKeyboardButton(" ", callback_data='0,5'), InlineKeyboardButton(" ", callback_data='0,6'), InlineKeyboardButton(" ", callback_data='0,7')],
    [InlineKeyboardButton(" ", callback_data='1,0'), InlineKeyboardButton(" ", callback_data='1,1'), InlineKeyboardButton(" ", callback_data='1,2'), InlineKeyboardButton(" ", callback_data='1,3'),
     InlineKeyboardButton(" ", callback_data='1,4'), InlineKeyboardButton(" ", callback_data='1,5'), InlineKeyboardButton(" ", callback_data='1,6'), InlineKeyboardButton(" ", callback_data='1,7')],
    [InlineKeyboardButton(" ", callback_data='2,0'), InlineKeyboardButton(" ", callback_data='2,1'), InlineKeyboardButton(" ", callback_data='2,2'), InlineKeyboardButton(" ", callback_data='2,3'),
     InlineKeyboardButton(" ", callback_data='2,4'), InlineKeyboardButton(" ", callback_data='2,5'), InlineKeyboardButton(" ", callback_data='2,6'), InlineKeyboardButton(" ", callback_data='2,7')],
    [InlineKeyboardButton(" ", callback_data='3,0'), InlineKeyboardButton(" ", callback_data='3,1'), InlineKeyboardButton(" ", callback_data='3,2'), InlineKeyboardButton(" ", callback_data='3,3'),
     InlineKeyboardButton(" ", callback_data='3,4'), InlineKeyboardButton(" ", callback_data='3,5'), InlineKeyboardButton(" ", callback_data='3,6'), InlineKeyboardButton(" ", callback_data='3,7')],
    [InlineKeyboardButton(" ", callback_data='4,0'), InlineKeyboardButton(" ", callback_data='4,1'), InlineKeyboardButton(" ", callback_data='4,2'), InlineKeyboardButton(" ", callback_data='4,3'),
     InlineKeyboardButton(" ", callback_data='4,4'), InlineKeyboardButton(" ", callback_data='4,5'), InlineKeyboardButton(" ", callback_data='4,6'), InlineKeyboardButton(" ", callback_data='4,7')],
    [InlineKeyboardButton(" ", callback_data='5,0'), InlineKeyboardButton(" ", callback_data='5,1'), InlineKeyboardButton(" ", callback_data='5,2'), InlineKeyboardButton(" ", callback_data='5,3'),
     InlineKeyboardButton(" ", callback_data='5,4'), InlineKeyboardButton(" ", callback_data='5,5'), InlineKeyboardButton(" ", callback_data='5,6'), InlineKeyboardButton(" ", callback_data='5,7')],
    [InlineKeyboardButton(" ", callback_data='6,0'), InlineKeyboardButton(" ", callback_data='6,1'), InlineKeyboardButton(" ", callback_data='6,2'), InlineKeyboardButton(" ", callback_data='6,3'),
     InlineKeyboardButton(" ", callback_data='6,4'), InlineKeyboardButton(" ", callback_data='6,5'), InlineKeyboardButton(" ", callback_data='6,6'), InlineKeyboardButton(" ", callback_data='6,7')],
    [InlineKeyboardButton(" ", callback_data='7,0'), InlineKeyboardButton(" ", callback_data='7,1'), InlineKeyboardButton(" ", callback_data='7,2'), InlineKeyboardButton(" ", callback_data='7,3'),
     InlineKeyboardButton(" ", callback_data='7,4'), InlineKeyboardButton(" ", callback_data='7,5'), InlineKeyboardButton(" ", callback_data='7,6'), InlineKeyboardButton(" ", callback_data='7,7')]
]



