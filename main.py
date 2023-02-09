from aiotg import Bot, Chat, CallbackQuery
import re
import os

if __name__ == '__main__':

    # @todo переделать под параметры

    bot = Bot(api_token=os.getenv('ITIL_BOT_TOKEN'))#взяли токен из параметров запуска
    admins = [213199160, 1722583749] #список админов


    @bot.command("/start")
    @bot.command("/?help")
    async def start_poker(chat: Chat, match):
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
        print(message)
        # channel.forward_message(chat.id, message['message_id'] )

        # проверим, не ответ ли это
        if ((message["from"]["id"] in admins) and ("reply_to_message" in message)):
            # @todo возможно надо добавить проверку, что переслано сообщение от 6206108722
            rep = "исходное сообщение:" + "\nот " + str(message["reply_to_message"]["forward_from"]["id"]) + "\n" + \
                  message["reply_to_message"]["forward_from"]["first_name"] + " "
            if ("last_name" in message["reply_to_message"]["forward_from"]):
                rep += message["reply_to_message"]["forward_from"]["last_name"]
            rep +=  "\n" + message["reply_to_message"]["text"]
            print(rep)
            reply = bot.channel(message["reply_to_message"]["forward_from"]["id"])
            await reply.send_text(message["text"])

            return await chat.reply("передано\n"+rep)

        if (re.fullmatch(r"(\d{3})", message['text'])):
            print(message['text'])
            #await channel.forward_message(chat.id, message['message_id'])
            for ch in channels:
                await ch.forward_message(chat.id, message['message_id'])
            return await chat.reply("Информацию принял, передаю. Ждите ответа")

        return chat.reply("Введите только цифры кода")


    channels = []
    #создадим соединения с админами
    for a in admins:
        channels.append(  bot.channel(a))
    bot.run()
