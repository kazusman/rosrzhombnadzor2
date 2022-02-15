# РосРжомбНадзор 2

### Вы спросите: "Если это второй, то где первый?"

### "Ты ебало-то завали", - ловко парирую я

![alt text](https://bestmemes.ucoz.net/_nw/2/59797818.jpg)

## Бот для весёлого времяпрепровождения в локальном чатике с мемами

### Тут есть два приложения:

* bot
* google_vision

Первое отвечает за всю коммуникацию с пользователями. Команды, сообщения, коллбэки и прочее

Второе - за API Google Vision, а именно распознование текста на фотографиях

В качестве веб-фреймворка юзается Django, бд - любая реляционная, в моём случае Postgres

Отложенные задачи пинаются воркером Celery в связке с Rabbit, который пинается через исполнение внутри контейнера 
файлика rabbit.sh. Список задач можно посмотреть в `bot/tasks.py`

Крутится всё в докере, сертификат (нужен для вебхуков телеги) берётся через запуск 
init-letsencrypt.sh. Запускается так: в nginx/nginx.conf ставим listen на 80 порт (пока без 443). Поднимаем 
контейнеры. Далее внутри сервиса веб запускаем файл ./init-letsencrypt.sh через команду 

`docker-compose exec web ./init-letsencrpt.sh`

После того, как скрипт отработает, нужно в nginx/nginx.conf описать listening для 443 порта и перезапустить контейнеры. 
Если тестите, то не забудьте в init-letsencrypt поставить значение переменной staging на 1, чтобы не словить флуд-бан на 
несколько часов, если будут ошибки

В качестве веб-сервера юзаем nginx, он роутит всю статику админки и запросы к http/https в т.ч. и проверку сертификатов

Прокси - gunicorn. Фактически веб стартует через гуникорновский WSGI (команда запуска есть в docker-compose и выглядит так: 
gunicorn app.wsgi:application --bind 0.0.0.0:8000)

Морда админки - Django Jazzmin, в принципе симпатичная и дизайн с настройками устанавливается в переменных 
`JAZZMIN_SETTINGS` и `JAZZMIN_UI_TWEAKS` в app/settings.py

## Модели

### bot:

* User - вся инфа о юзерах (telegram_id, username и прочее)
* Status - статусы пользователя. Нужны по факту для определения, что сейчас делает пользователь. Например, если прислал команду
/search - ставим статус meme_searching и когда он пришлёт любой текст с таким статусом, то я 
сразу пойму, что этот текст с картинки, а не просто пердёж в лужу в виде очередного анекдота
* StartAnswer - список ответов на команду /start
* Message - тут сохраняем все сообщения юзеров (кроме тех случаев, когда присылаются команды и когда идёт запрос на поиск мема)
* NotFoundAnswer - список ответов на случаи, когда мем не найден
* FunnyAction - правила ответа на те или иные сообщения
* Bet - информация о ставках. Кто поставил, кому, какая сумма, какое сообщение, какой результат

Вся логика работы с моделями разбита на несколько классов и бОльшая часть описана в bot/service. В тех классах 
инициализируются юзеры, статусы, методы для их управления и различные необходимые атрибуты. Далее, в зависимости 
от типа присланного контента (текст, фото, видео, войс и т.д.) дёргаются наследованные от ActionProcessor класса методы,
которые описаны в своих директориях в bot/communication/ТИП_СООБЩЕНИЯ/service.py. Сами же "роуты" событий так 
же описаны в соответсвующих типам сообщений директориям в bot/communication/ТИП_СООБЩЕНИЯ/__init__.py

## .env

Сами переменные не дам, придумывайте свои. Пример есть в .env.example, а здесь просто описание

SECRET_KEY= секретный ключ Django из settings.py
DEBUG= Режим разработки, булево значение
ALLOWED_HOSTS= Список (или кортеж) дозволенных хостов. Если несколько, указываются через ПРОБЕЛ. Если не боитесь, можно просто поставить *

DATABASE= Имя БД
USER= Имя пользователя
PASSWORD= Пароль пользователя
HOST= Хост
PORT= Порт

RABBITMQ_ERLANG_COOKIE= Куки (коки)
RABBITMQ_DEFAULT_USER= Дефолтное имя пользователя рэббита
RABBITMQ_DEFAULT_PASS= Дефолтный пароль пользователя

CHAT_ID= ID чата, в котором происходит всё действо
CHAT_URL= Ссылка на этот чат
BOT_URL= Ссылка на бота
TELEGRAM_BOT_TOKEN= Токен телеграм-бота
PROJECT_URL= Основная url проекта в формате https://example.com (обязательно https, а то не поставишь вебхук. И никаких слэшей в конце)
CELERY_BROKER_URL= url брокера задач

GOOGLE_APPLICATION_CREDENTIALS= название файла с кредами от гуглоаккаунта


Всё, что ниже, расписывать не буду. это просто данные из файлика кредов от гугла, которые перенесены в переменные, чтоб не хранить файл где-то в гитхабе. 
В settings.py есть функция, которая вытаскивает эти переменные, засовывает их в файл creds.json и подсовывает этот файл гугловскому апи

TYPE=

PROJECT_ID=

PRIVATE_KEY_ID=

PRIVATE_KEY=

CLIENT_EMAIL=

CLIENT_ID=

AUTH_URI=

TOKEN_URI=

AUTH_PROVIDER_X509_CERT_URL=

CLIENT_X509_CERT_URL=