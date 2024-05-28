import logging
import random
from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler,
)

ONE, TWO, THREE, FOUR = range(4)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from baza.models import Word, User

GAME = "🎮 So'z o'yini"
MY_LIST = "📕 Mening lug'atim"

MAIN = [[GAME, MY_LIST]]
FIRST, CREATE_WORD, CREATE_DEF = range(3)


def start(update: Update, context: CallbackContext):
    """Inform user about what this bot can do"""
    user = update.message.from_user.id

    # users = list(User.objects.values("user_id").values())

    user = update.message.from_user.first_name
    update.message.reply_text(
        f"Assalamu alaykum {user}, botga xush kelibsiz",
        reply_markup=ReplyKeyboardMarkup(
            MAIN,
            resize_keyboard=True
        ),

    )

    if {"user_id": user} not in User.objects.values("user_id"):
        User.objects.create(user_id=user)


def my_list(update: Update, context: CallbackContext):
    keyboard = [
                [
                    InlineKeyboardButton("➕ Qo'shish", callback_data=str(add)),

                ],
                [
                    InlineKeyboardButton("👀 Ko'rish", callback_data=str(see)),
                ],
            ]

    update.message.reply_html(
        "📕 Mening lug'atim\n"
        "✅ Shaxsiy lug'atlaringiz ustida amallar bajarishingiz mumkin!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return FIRST
    # pass


def add(update: Updater, content: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="⏳Inglizcha so'z kiriting: Kiritilayotgan so'z:\n"
                                 "book--definition--kitob "
                                 "ko'rinishida kiriting")

    return CREATE_WORD


def get_current_user(id):
    user = User.objects.filter(user_id=id).first()
    return user


def create_word(update: Updater, context: CallbackContext):
    message = update.message.text
    text = message.split("\n")
    line = len(text)
    user = update.message.from_user.id

    s = f"✅{line} ta lug'at qo'shildi!✅\n"

    n = 1
    for tex in text:
        t = tex.split("—")
        Word.objects.create(user=get_current_user(user), word=t[0], definition=t[1], tarjima=t[2])

        s += f"{n})New word \n 🔹{t[0]} --- {t[2]}\n 🔸definition: {t[1]} \n\n"
        n +=1
    update.message.reply_text(s)
    return ConversationHandler.END


selected_options = {}


def see(update: Updater, content: CallbackContext):
    words = Word.objects.all()

    text = ""
    for x in words:
        text += " ⚡️ " + x.word + " " + x.tarjima + "\n"

    query = update.callback_query
    query.answer()
    query.edit_message_text(text)

    return ConversationHandler.END


def menu(update: Updater, content: CallbackContext):
    query = update.callback_query
    query.answer()
    return start(update, content)


words = {}


def quiz(update: Update, context: CallbackContext):

    text = Word.objects.all()
    for x in text:
        words[f"{x.word}"] =x.tarjima

    if not words:
        update.message.reply_text('No words available for quiz.')
        return

    # Randomly select a word
    word, correct_definition = random.choice(list(words.items()))

    # Generate wrong definitions
    all_definitions = list(words.values())
    all_definitions.remove(correct_definition)
    wrong_definitions = random.sample(all_definitions, 3)

    # Create a list of options and shuffle them
    options = wrong_definitions + [correct_definition]
    random.shuffle(options)

    # Store the correct answer in context.user_data
    context.user_data['quiz_word'] = word
    context.user_data['correct_answer'] = correct_definition

    # Create inline keyboard for options
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f'What is the definition of: {word}?', reply_markup=reply_markup)

def help(update:Updater, content: CallbackContext):
    update.message.reply_text("/start botni ishga tushirish uchun , /quiz quiz dan takrorlash uchun, "
                              "/stats statistikani ko'rish uchun")

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    selected_option = query.data
    correct_answer = context.user_data.get('correct_answer')

    if 'correct_count' not in context.user_data:
        context.user_data['correct_count'] = 0
    if 'incorrect_count' not in context.user_data:
        context.user_data['incorrect_count'] = 0

    if selected_option == correct_answer:
        context.user_data['correct_count'] += 1
        query.edit_message_text(
            text=f'Correct! The definition of {context.user_data["quiz_word"]} is "{correct_answer}".')
    else:
        context.user_data['incorrect_count'] += 1
        query.edit_message_text(
            text=f'Incorrect. The correct definition of {context.user_data["quiz_word"]} is "{correct_answer}".')

    # Clear the stored data
    context.user_data['quiz_word'] = None
    context.user_data['correct_answer'] = None


def stats(update: Update, context: CallbackContext) -> None:
    correct_count = context.user_data.get('correct_count', 0)
    incorrect_count = context.user_data.get('incorrect_count', 0)
    update.message.reply_text(f'Statistics:\nCorrect answers: {correct_count}\nIncorrect answers: {incorrect_count}')


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("7134965785:AAFv-6tRKlRbH9_nJSuamN8ACm3V4m2brb8", workers=5, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
                entry_points=[
                    CommandHandler('start', start),
                    MessageHandler(Filters.text(MY_LIST), my_list),
                    MessageHandler(Filters.text(GAME), quiz),
                    CommandHandler("quiz", quiz),
                    CommandHandler("stats", stats),
                    CommandHandler("help", help),
                    CallbackQueryHandler(button)
                ],
                states={
                    FIRST: [
                        CallbackQueryHandler(add, pattern='^' + str(add) + '$'),
                        CallbackQueryHandler(see, pattern='^' + str(see) + '$'),
                    ],

                    CREATE_WORD: [
                        MessageHandler(Filters.text & ~Filters.command, create_word),
                    ],


                },
                fallbacks=[CommandHandler('start', start)],
            )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()


