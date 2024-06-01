# Pinsaver
### Даввно хотел скачивать видосики из Pinterest? Выход есть!

### Значит смотри. Я тут тебе телегерамм бота, склепал. Сейчас всё поясню.

### Первым делом, первым делом что? Самолёты? Нифига! Первым делом иди к BotFather за токеном. Я подожду...

### Сходил? Отлично, теперь копируй репозиторий к себе 

```
$ git clone 
```

### Вставляй токен вот сюда:

```
pinsaver = telebot.TeleBot(TOKEN)
```

### Собственно на этом всё, можешь пользоваться. Но если тебе интересно как же там всё работает, сейчас всё объясню.


### В идеале, парсить видосики прямо с сайта, но злые дяди поставили тип данных blob и это печально. Поэтому будем парсить с https://pinterestvideodownloader.com/ 


```
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
```


### Теперь просто подвяжем это к боту, чтобы ты дал ему ссылку, а он тебе видосик

```
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
```

### А на этом всё. Ииииииииииииииииииииии помните, боты - это круто.