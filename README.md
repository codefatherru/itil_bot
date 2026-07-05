# Bot for Telegram для техподдержки
Этот бот собирает присланные коды, пересылает их админам бота и дает возожность отвечать на эти запросы.
Админы получают пересланное сообщение клиента и для отправки ответа, должны ответить (reply) на конкретное сообщение клиента. 
Если Клиент не дает разрешение на цитирование своих сообщений, отвечать надо на Техническое Сообщение начинающееся с технического номера Клиента
# Usage

##запуск для разработкии:
```
python -m venv venv  
venv\Scripts\activate 

python .\main.py 7 749923226:ХХХХ
```
##запуск на хостинге:
### bothost
для запуска на bothost была добавлена поддержка dotenv и значения `BOT_TOKEN`

как настроить деплой с GitHub:
https://github.com/codefatherru/itil_bot/settings делаем репозиторий публичным
https://github.com/settings/personal-access-tokens генерируем гранулированный токен для https://github.com/codefatherru/itil_bot.git
https://bothost.ru/admin-repos.php заводим новый токен (ветка itil_bot + https токен), старые удаляем

##запуск в контейнере:
###windows
```
run.bat 6206108722:some-token
```
для удобства можно создать Ярлык с указанием токена. внимание. параметр задаётся без "ITIL_BOT_TOKEN=" : сразу значение

наблюдать через вкладку logs контейнера itilbot 
###unix
 
```
ITIL_BOT_TOKEN=6206108722:some-token ./run.sh
```
```
 bash ./run.sh -ITIL_BOT_TOKEN "6206108722:some-token" 
```
будут созданы и запушены образ и контейнер `itilbot`. 
параметром вызова является токен бота (должен попасть в переменную окружения ITIL_BOT_TOKEN)

для чтения логов докера можно использовать консольную команду ``docker logs itilbot
``

#Errors

```
ERROR:aiotg:Not Found
```
pip install aiotg  
```
aiotg.bot.BotApiError: Not Found
```
При вызове не был передан ITIL_BOT_TOKEN

``
error during connect: this error may indicate that the docker daemon is not running
``
означает, что не запущен docker daemon

>   File "/usr/local/lib/python3.11/site-packages/urllib3/connection.py", line 213, in _new_conn
    raise ConnectTimeoutError(
urllib3.exceptions.ConnectTimeoutError: (<HTTPSConnection(host='moscow.megafon.ru', 


> raise ConnectTimeout(e, request=request)
requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='moscow.megafon.ru'
