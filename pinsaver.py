import requests
from bs4 import BeautifulSoup

import os
import datetime
import telebot
from config import TOKEN

pinsaver = telebot.TeleBot(TOKEN)
pinsaver_url = 'https://pinterestvideodownloader.com/'


def save(url_message):

    data = {
        'url': url_message
    }

    response = requests.post(
        url=pinsaver_url, 
        data=data
    )    
    
    try:
        soup = BeautifulSoup(response.text, 'lxml')

        video = soup.find('video')
        video_src = video['src']
        video_response = requests.get(video_src)

        with open('output.mp4', 'wb') as file:
            file.write(video_response.content)
    except Exception as e:
        print(f'{datetime.datetime.now()} Что-то пошло не так: {e}')   

@pinsaver.message_handler(commands=['start'])
def start(message):
    pinsaver.send_message(message.chat.id, 
f'''*:･ﾟ✧Pinsaver успешно запущен!*:･ﾟ✧

Для начала работы просто отправьте ссылку из Pinterest'''
)

@pinsaver.message_handler()
def activity(message):

    if message.text:
        try:
            save(message.text) 

            with open('output.mp4', 'rb') as file:
                pinsaver.send_document(message.chat.id, file)
                
            pinsaver.send_message(message.chat.id, f'Готово!')
            os.remove('output.mp4')

        except Exception as e:
            print(f'{datetime.datetime.now()} Что-то пошло не так: {e}')
        
pinsaver.infinity_polling()
