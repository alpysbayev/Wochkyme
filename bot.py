import telebot
import requests
import shutil
from pydub import AudioSegment
import speech_recognition as sr
import openai

API_KEY = "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"
BOT_TOKEN = '5787535765:AAFldNYVtNNMJJl6sIu9PTNcxUyGwx-YAGY'

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = API_KEY


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "<b>Research Oriented Study</b> \nOur team: Adilet | Beknar | Yerulan | Timur | Adilkhan \nOur bot can convert your voice message to text and send it to you. \nAlso, we can chat with you using GPT-3.",
        parse_mode='html'
    )


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(
        f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}',
        stream=True
    )

    username = str(message.from_user.username)
    if file.status_code == 200:
        with open(f'{username}.ogg', 'wb') as f:
            file.raw.decode_content = True
            shutil.copyfileobj(file.raw, f)

            # Convert ogg file to wav
        ogg_version = AudioSegment.from_ogg(f'{username}.ogg')
        ogg_version.export(f'{username}.wav', format="wav")

        # Initialize recognizer class (for recognizing the speech)
        r = sr.Recognizer()

        # Reading Audio file as source
        # listening the audio file and store in audio_text variable
        with sr.AudioFile(f'{username}.wav') as source:
            audio_text = r.listen(source)

        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            print('Converting audio transcripts into text...')
            text = r.recognize_google(audio_text)
            print(text)
            bot.send_message(message.chat.id, f"Your VM: {text}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"{text}"}
                ]
            )
            chatgpt_response = response['choices'][0]['message']['content']
            bot.send_message(message.chat.id, f"<b>ChatGPT:</b  > {chatgpt_response}", parse_mode='html')


        except Exception as e:
            print('Failed to recognize speech from audio. Error:', str(e))


    else:
        bot.reply_to(message, 'Unable to download file.')


bot.polling(none_stop=True)
