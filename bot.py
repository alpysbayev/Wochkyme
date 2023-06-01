import telebot
import requests
import shutil

TOKEN = '5787535765:AAFldNYVtNNMJJl6sIu9PTNcxUyGwx-YAGY'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "<b>Hello</b>, send me your voice message:", parse_mode='html')

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path), stream=True)

    if file.status_code == 200:
        with open('voice.mp3', 'wb') as f:
            file.raw.decode_content = True
            shutil.copyfileobj(file.raw, f)  
    else:
        bot.reply_to(message, 'Unable to download file.')

bot.polling()

bot.polling(none_stop=True)
