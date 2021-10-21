import telebot
import setting
import allmessage
import pickle
from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator
# import questionandanswer

print("##################\nCreated by Ernest\n##################")
bot = telebot.TeleBot(setting.token)
#
# with open('database.pickle', 'wb') as f:
#     pickle.dump(questionandanswer.questions, f)
@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    ua = types.KeyboardButton(text=allmessage.ua)
    ru = types.KeyboardButton(text=allmessage.ru)
    markup.add(ua, ru)
    bot.send_message(message.from_user.id, allmessage.first_message, reply_markup=markup)
#
@bot.message_handler(content_types=['text'])
def gettext(message):
    if message.text == allmessage.ua:
        first_message_ua(message)
    if message.text == allmessage.ru:
        first_message_ru(message)
    if message.text == allmessage.button_change_language_ua:
        change_language(message)
    if message.text == allmessage.button_change_language_ru:
        change_language(message)
    if message.text == allmessage.button_average_questions_ua or message.text == allmessage.button_average_questions_ru:
        average_questions_ua(message)
    if message.text == allmessage.button_back_ua:
        first_message_ua(message)
    if message.text == allmessage.button_back_ru:
        first_message_ru(message)
    if message.text == allmessage.button_question_ua or message.text == allmessage.button_contacts_ua:
        contacts_ua(message)
    if message.text == allmessage.button_question_ru or message.text == allmessage.button_contacts_ru:
        contacts_ru(message)
    if message.text == allmessage.button_admin_ru or message.text == allmessage.button_admin_ua:
        for i in setting.admins:
             if i == message.from_user.id:
                 adminpanel(message)
    if message.text == allmessage.button_new_post:
        for i in setting.admins:
            if i == message.from_user.id:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
                cancel = types.KeyboardButton(text=allmessage.button_cancel)
                markup.add(cancel)
                bot.send_message(message.from_user.id, allmessage.add_name, reply_markup=markup)
                bot.register_next_step_handler(message, addname)
    if message.text == allmessage.button_delete_post:
        for i in setting.admins:
            if i == message.from_user.id:
                bot.send_message(message.from_user.id, allmessage.number_delete_post)
                bot.register_next_step_handler(message, delpost)
    if message.text == allmessage.button_edit_post:
        for i in setting.admins:
            if i == message.from_user.id:
                bot.send_message(message.from_user.id, allmessage.edit_post)
                bot.register_next_step_handler(message, editpost)
    if message.text == allmessage.button_cancel:
        for i in setting.admins:
            if i == message.from_user.id:
                adminpanel(message)

#
@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(call.message.chat.id, call.message.message_id)
    average_questions_ua(call.message, page)
#
def first_message_ua(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    averagequestions = types.KeyboardButton(text=allmessage.button_average_questions_ua)
    contacts = types.KeyboardButton(text=allmessage.button_contacts_ua)
    admin = types.KeyboardButton(text=allmessage.button_admin_ua)
    change_language = types.KeyboardButton(text=allmessage.button_change_language_ua)
    for i in setting.admins:
         if i == message.from_user.id:
             markup.add(admin)
    markup.add(averagequestions, contacts, change_language)
    bot.send_message(message.from_user.id, allmessage.first_message_ua, reply_markup=markup)
#
def first_message_ru(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    averagequestions = types.KeyboardButton(text=allmessage.button_average_questions_ru)
    contacts = types.KeyboardButton(text=allmessage.button_contacts_ru)
    admin = types.KeyboardButton(text=allmessage.button_admin_ru)
    change_language = types.KeyboardButton(text=allmessage.button_change_language_ru)
    for i in setting.admins:
         if i == message.from_user.id:
             markup.add(admin)
    markup.add(averagequestions, contacts, change_language)
    bot.send_message(message.from_user.id, allmessage.first_message_ru, reply_markup=markup)
#
def change_language(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    ua = types.KeyboardButton(text=allmessage.ua)
    ru = types.KeyboardButton(text=allmessage.ru)
    markup.add(ua, ru)
    bot.send_message(message.from_user.id, allmessage.change_language_ua, reply_markup=markup)
#
def average_questions_ua(message, page=1):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    try:
        paginator = InlineKeyboardPaginator(len(questions), current_page=page, data_pattern='character#{page}')
        question = allmessage.popular_question + '\n'
        page = page - 1
        question += questions[page]['text'] + "\n" + questions[page]['discription'] + "\n" + questions[page]['link']
        bot.send_message(message.chat.id, question, reply_markup=paginator.markup, parse_mode='Markdown')
    except:
        bot.send_message(message.from_user.id, allmessage.Error)
#
def contacts_ua(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text = allmessage.button_back_ua)
    markup.add(back)
    bot.send_message(message.from_user.id, allmessage.question_ua, reply_markup=markup)
#
def contacts_ru(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text = allmessage.button_back_ru)
    markup.add(back)
    bot.send_message(message.from_user.id, allmessage.question_ru, reply_markup=markup)
#
def adminpanel(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    back = types.KeyboardButton(text=allmessage.button_back_ru)
    newpost = types.KeyboardButton(text=allmessage.button_new_post)
    deletepost = types.KeyboardButton(text=allmessage.button_delete_post)
    editpost = types.KeyboardButton(text=allmessage.button_edit_post)
    markup.add(newpost, editpost, deletepost, back)
    bot.send_message(message.from_user.id, allmessage.post, reply_markup=markup)
#
def addname(message):
    if message.text == allmessage.button_cancel:
        adminpanel(message)
        return
    elif message.text == message.text:
        allmessage.head = message.text
        bot.send_message(message.from_user.id, allmessage.add_discription)
        bot.register_next_step_handler(message, adddiscription)
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return
#
def adddiscription(message):
    if message.text == allmessage.button_cancel:
        adminpanel(message)
        return
    elif message.text == message.text:
        allmessage.description = message.text
        bot.send_message(message.from_user.id, allmessage.add_link)
        bot.register_next_step_handler(message, addlink)
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return
#
def addlink(message):
    if message.text == allmessage.button_cancel:
        adminpanel(message)
        return
    elif message.text == message.text:
        allmessage.link = message.text
        newpost(message)
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return

#
def newpost(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    question = allmessage.new_post_message + ""
    question += allmessage.head + "\n" + allmessage.description + "\n" + allmessage.link
    bot.send_message(message.from_user.id, question)
    try:
        i = len(questions)
    except:
        i = 0
    questions[i] = {"text":allmessage.head, 'discription': allmessage.description, 'link': allmessage.link}
    newpost = questions
    with open('database.pickle', 'wb') as f:
        pickle.dump(newpost, f)
    adminpanel(message)
#
def delpost(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    try:
        allmessage.numberpost = int(message.text)
    except:
        bot.send_message(message.from_user.id, allmessage.Error)
        return
    i = len(questions)
    if 0 < allmessage.numberpost <= i:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        yes = types.KeyboardButton(text=allmessage.delete_post_yes)
        no = types.KeyboardButton(text=allmessage.delete_post_no)
        cancel = types.KeyboardButton(text=allmessage.button_cancel)
        markup.add(yes, no, cancel)
        question = questions[allmessage.numberpost-1]['text'] + "\n" + questions[allmessage.numberpost-1]['discription'] + "\n" + questions[allmessage.numberpost-1]['link'] + "\n" + "\n" + allmessage.delete_post
        bot.send_message(message.from_user.id, question, reply_markup=markup)
        bot.register_next_step_handler(message, deletepost)
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return
#
def deletepost(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    if message.text == allmessage.delete_post_yes:
        for i in setting.admins:
            if i == message.from_user.id:
                i = len(questions)
                questions[allmessage.numberpost - 1] = questions[i - 1]
                del questions[i - 1]
                newpost = questions
                with open('database.pickle', 'wb') as f:
                    pickle.dump(newpost, f)
                adminpanel(message)
    elif message.text == allmessage.delete_post_no:
        onemoredelpost(message)
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return

def onemoredelpost(message):
    bot.send_message(message.from_user.id, allmessage.number_delete_post)
    bot.register_next_step_handler(message, delpost)
#
def editpost(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    try:
        allmessage.numberpost = int(message.text)
        i = len(questions)
    except:
        bot.send_message(message.from_user.id, allmessage.Error)
        return
    if 0 < allmessage.numberpost <= i:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        yes = types.KeyboardButton(text=allmessage.delete_post_yes)
        no = types.KeyboardButton(text=allmessage.delete_post_no)
        cancel = types.KeyboardButton(text=allmessage.button_cancel)
        markup.add(yes, no, cancel)
        question = questions[allmessage.numberpost - 1]['text'] + "\n" + questions[allmessage.numberpost - 1][
            'discription'] + "\n" + questions[allmessage.numberpost - 1]['link'] + "\n" + "\n" + allmessage.edit_number_post
        bot.send_message(message.from_user.id, question, reply_markup=markup)
        bot.register_next_step_handler(message, select_edit_post)
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return

def onemoreeditpost(message):
    bot.send_message(message.from_user.id, allmessage.edit_post)
    bot.register_next_step_handler(message, editpost)

#
def select_edit_post(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    if message.text == allmessage.delete_post_yes:
        for i in setting.admins:
            if i == message.from_user.id:
                i = len(questions)
                markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=False)
                editname = types.KeyboardButton(text=allmessage.edit_name)
                editdiscription = types.KeyboardButton(text=allmessage.edit_discription)
                editlink = types.KeyboardButton(text=allmessage.edit_link)
                cancel = types.KeyboardButton(text=allmessage.button_cancel)
                markup.add(editname, editdiscription, editlink, cancel)
                bot.send_message(message.from_user.id, allmessage.edit_select, reply_markup=markup)
                bot.register_next_step_handler(message, edit_post)
    elif message.text == allmessage.delete_post_no:
        onemoreeditpost(message)
        return

    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        return
#
def edit_post(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    if message.text == allmessage.edit_name:
        bot.send_message(message.from_user.id, allmessage.add_name)
        bot.register_next_step_handler(message, editname)
    elif message.text == allmessage.edit_discription:
        bot.send_message(message.from_user.id, allmessage.add_discription)
        bot.register_next_step_handler(message, editdiscription)
    elif message.text == allmessage.edit_link:
        bot.send_message(message.from_user.id, allmessage.add_link)
        bot.register_next_step_handler(message, editlink)
    elif message.text == allmessage.button_cancel:
        bot.send_message(message.from_user.id, allmessage.button_cancel)
        adminpanel(message)
        return
    else:
        bot.send_message(message.from_user.id, allmessage.Error)
        editnextpost(message)
#
def editname(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    if message.text == allmessage.button_cancel:
        bot.send_message(message.from_user.id, allmessage.button_cancel)
        adminpanel(message)
        return
    else:
        editname = message.text
        questions[allmessage.numberpost - 1]["text"] = editname
        editpost = questions
        with open('database.pickle', 'wb') as f:
            pickle.dump(editpost, f)
        with open('database.pickle', 'rb') as f:
            questions = pickle.load(f)
        question = questions[allmessage.numberpost - 1]['text'] + "\n" + questions[allmessage.numberpost - 1]['discription'] + "\n" + questions[allmessage.numberpost - 1]['link']
        sendmessage = allmessage.new_post_message + question
        bot.send_message(message.from_user.id, sendmessage)
        editnextpost(message)
#
def editdiscription(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    if message.text == allmessage.button_cancel:
        bot.send_message(message.from_user.id, allmessage.button_cancel)
        adminpanel(message)
        return
    else:
        editdiscription = message.text
        questions[allmessage.numberpost - 1]["discription"] = editdiscription
        editpost = questions
        with open('database.pickle', 'wb') as f:
            pickle.dump(editpost, f)
        with open('database.pickle', 'rb') as f:
            questions = pickle.load(f)
        question = questions[allmessage.numberpost - 1]['text'] + "\n" + questions[allmessage.numberpost - 1]['discription'] + "\n" + questions[allmessage.numberpost - 1]['link']
        sendmessage = allmessage.new_post_message + question
        bot.send_message(message.from_user.id, sendmessage)
        editnextpost(message)
#
def editlink(message):
    with open('database.pickle', 'rb') as f:
        questions = pickle.load(f)
    if message.text == allmessage.button_cancel:
        bot.send_message(message.from_user.id, allmessage.button_cancel)
        adminpanel(message)
        return
    else:
        editlink = message.text
        questions[allmessage.numberpost - 1]["link"] = editlink
        editpost = questions
        with open('database.pickle', 'wb') as f:
            pickle.dump(editpost, f)
        with open('database.pickle', 'rb') as f:
            questions = pickle.load(f)
        question = questions[allmessage.numberpost - 1]['text'] + "\n" + questions[allmessage.numberpost - 1]['discription'] + "\n" + questions[allmessage.numberpost - 1]['link']
        sendmessage = allmessage.new_post_message + question
        bot.send_message(message.from_user.id, sendmessage)
        editnextpost(message)

def editnextpost(message):
    for i in setting.admins:
        if i == message.from_user.id:
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=False)
            editname = types.KeyboardButton(text=allmessage.edit_name)
            editdiscription = types.KeyboardButton(text=allmessage.edit_discription)
            editlink = types.KeyboardButton(text=allmessage.edit_link)
            cancel = types.KeyboardButton(text=allmessage.button_cancel)
            markup.add(editname, editdiscription, editlink, cancel)
            bot.send_message(message.from_user.id, allmessage.edit_select, reply_markup=markup)
            bot.register_next_step_handler(message, edit_post)

#
bot.remove_webhook()
bot.polling(none_stop=True, interval=0)