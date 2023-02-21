# coding: utf-8
"""
Telegram Бот для обработки входящий сообщений.
Бот принимает входящие личные сообщения строго определенного формата (Код из 3х символов) от Клиентов
и передает их Админам (фиксированный список пользователей) в виде пересланого сообщения (Обращения).
Если Админ ответит (строго при помощи функции "Reply" на конкретное Обращение),
текст Ответа будет передан Клиенту в качестве нового личного сообщения.
"""
from aiotg import Bot, Chat, CallbackQuery
import re
import os

if __name__ == '__main__':

    # @todo переделать под параметры

    bot = Bot(api_token=os.getenv('ITIL_BOT_TOKEN'))#взяли токен из параметров запуска
    admins = [213199160, 1722583749] #список админов


    @bot.command("/start")
    @bot.command("/?help")
    async def start_chat(chat: Chat, match):
        """
        обработчик начала работы Клиента с Ботом.
        """
        await chat.send_text("Здравствуйте, для запроса пароля введите код из ЛИСа и дождитесь ответа"
                             "\nНапоминаю, что ввод пароля нужен только при первом запуске приложения после установки или переустановки приложения"
                             "\nВаши данные никуда не передаются и не сохраняются"
                             "\nСпасибо, что пользуетесь приложением")


    """ @bot.command(r"(\d{4})")
    async def code(chat: Chat, message, match):
        print(match.group(1))
        await channel.forward_message(chat.id, message['message_id'])
        return await chat.reply("Информацию принял, передаю. Ждите ответа")"""

    """    @bot.command(r"(.+)")
    async def again(chat: Chat, match):
        print(chat.id)
        #print(chat.get_chat())
        #print(match)
        #print(Chat.get_chat(chat))
        print(chat.sender.keys())
        print(chat.sender['id'])
        # леонов 213199160
        #match.group(1)
        #chat.forward_message(213199160,)
        return chat.reply(" заявку принял ")"""


    @bot.default
    async def echo(chat, message):
        """
        Обработчик всех входящих сообщений. Собержит основную логику принятия решений о пересылке сообщений
        """
        print(message)
        #@todo сделать нормальное логирование
        # channel.forward_message(chat.id, message['message_id'] )

        # проверим, не Ответ ли это от Админов
        if ((message["from"]["id"] in admins) and ("reply_to_message" in message)):
            # @todo возможно надо добавить проверку, что переслано сообщение от 6206108722 т.е. от самого бота
            if(("reply_to_message" in message) and ("*INBOX from*" in message["reply_to_message"]["text"])):
                #поймали ответ на техническое сообщение
                data = message["reply_to_message"]["text"].split("*")
                print(data)
                rep = "исходное сообщение:" + "\nот " + data[2] + "\n" +data[3]
                # соединяемся с персональным чатом автора исходного сообщения(Клиент, отправивший обращение с кодом)
                reply = bot.channel(data[2])
                await reply.send_text(message["text"])
                return await chat.reply("передано\n" + rep)
            elif ("forward_from" in message["reply_to_message"]):#это ответ на обычное пересланное Обращение
                #формируем текст отчета об Ответе
                rep = "исходное сообщение:" + "\nот " + str(message["reply_to_message"]["forward_from"]["id"]) + "\n" + \
                      message["reply_to_message"]["forward_from"]["first_name"] + " "
                # фамилия может быть не заполнена
                if ("last_name" in message["reply_to_message"]["forward_from"]):
                    rep += message["reply_to_message"]["forward_from"]["last_name"]
                rep +=  "\n" + message["reply_to_message"]["text"]
                print(rep)
                #соединяемся с персональным чатом автора исходного сообщения(Клиент, отправивший обращение с кодом)
                reply = bot.channel(message["reply_to_message"]["forward_from"]["id"])
                #отправляем Клиенту текст из сообщения-Ответа Админа
                await reply.send_text(message["text"])
                #отправляем отчет Админу
                return await chat.reply("передано\n"+rep)
            elif ("forward_sender_name" in message["reply_to_message"]):#это ответ на непересылаемое сообщение
                return await chat.reply("Клиент не разрешил пересылать свои Обращения, используйте техническое сообщение")


        #если текст входящего сообщение подходит под формат Кода (3 числа)
        if (re.fullmatch(r"(\d{3})", message['text'])):
            print(message['text'])
            #await channel.forward_message(chat.id, message['message_id'])
            #пересылаем Обращение Админам
            for ch in channels:
                #Пересылаем исхожное Обращение
                await ch.forward_message(chat.id, message['message_id'])
                #отправляем техническое сообщение
                await ch.send_text("*INBOX from*" + str(message["from"]['id']) +"*" + message["text"], markup="MarkdownV2")
            return await chat.reply("Информацию принял, передаю. Ждите ответа")
        #отвечаем на все остальные неопознанные сообщения
        return chat.reply("Введите только цифры кода")


    channels = []
    #создадим соединения с админами
    for a in admins:
        channels.append(  bot.channel(a))
    #@todo убрать временный костыль. отправка сообщения о старте первому из Админов
    channels[0].send_text("Стартую")
    bot.run()
