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
import requests
import sys
from dotenv import load_dotenv

import logging

## Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG)

import http.client

httpclient_logger = logging.getLogger("http.client")

def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework."""
    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    http.client.print = httpclient_log
    http.client.HTTPConnection.debuglevel = 1

httpclient_logging_patch()


if __name__ == '__main__':

    load_dotenv()

    if os.getenv('BOT_TOKEN'):
        token = os.getenv('BOT_TOKEN')#требование bothost
    elif len(sys.argv) == 2 and sys.argv[1] != '-u':
        token = sys.argv[1]
    elif os.getenv('ITIL_BOT_TOKEN'):
        token = os.getenv('ITIL_BOT_TOKEN')
    else:
        sys.exit('не передан токен')
    print('параметр ', token)

    bot = Bot(api_token=token)#взяли токен из параметров запуска
    admins = [224671539 , 213199160] #список админов
    mid = None


    @bot.command("/start")
    @bot.command("/?help")
    async def start_chat(chat: Chat, match):
        """
        обработчик начала работы Клиента с Ботом.
        """
        await chat.send_text("Здравствуйте, введите телефонный номер")





    @bot.default
    async def echo(chat, message):
        """
        Обработчик всех входящих сообщений. Собержит основную логику принятия решений о пересылке сообщений
        """
        global tel, mid
        print('tel', tel, 'mid', mid)
        print(message)
        #@todo сделать нормальное логирование
        # channel.forward_message(chat.id, message['message_id'] )


        #если текст входящего сообщение подходит под формат телефона (10 чисел)
        if (re.fullmatch(r"(\d{10})", message['text'])):
            print(message['text'])
            #await channel.forward_message(chat.id, message['message_id'])

            tel = message['text']

            cookies = {
                'tmr_lvid': '9ff438b1c18f8a9bdd32253a89d02ac2',
                'tmr_lvidTS': '1762886458466',
                '_ym_uid': '176288645985168560',
                '_ym_d': '1762886459',
                '_ym_visorc': 'b',
                '_ym_isad': '2',
                'mindboxDeviceUUID': '2b88142a-e896-4f78-9042-d7d8f806b546',
                'directCrm-session': '%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D',
                '_ymab_param': '3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ',
                'domain_sid': 'DvNXmLUQfGJfC0wReUU1Z%3A1762886460394',
                'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
                'mid': mid,
                'tmr_detect': '0%7C1762886465762',
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://moscow.megafon.ru/perenos_tarifa/drugoy_operator/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'X-API-Scope': 'browser',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                # 'Cookie': 'tmr_lvid=9ff438b1c18f8a9bdd32253a89d02ac2; tmr_lvidTS=1762886458466; _ym_uid=176288645985168560; _ym_d=1762886459; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=2b88142a-e896-4f78-9042-d7d8f806b546; directCrm-session=%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D; _ymab_param=3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ; domain_sid=DvNXmLUQfGJfC0wReUU1Z%3A1762886460394; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; mid=28e12f4c-a753-4c10-9c85-25294ef4557c; tmr_detect=0%7C1762886465762',
            }

            response = requests.get('https://moscow.megafon.ru/api/unite/v1/cdss/mid', cookies=cookies, headers=headers)

            if response.status_code == 200:
                json_data = response.json()
                print(json_data)
                mid = json_data['mid']



            cookies = {
                'tmr_lvid': '9ff438b1c18f8a9bdd32253a89d02ac2',
                'tmr_lvidTS': '1762886458466',
                '_ym_uid': '176288645985168560',
                '_ym_d': '1762886459',
                '_ym_visorc': 'b',
                '_ym_isad': '2',
                'mindboxDeviceUUID': '2b88142a-e896-4f78-9042-d7d8f806b546',
                'directCrm-session': '%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D',
                '_ymab_param': '3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ',
                'domain_sid': 'DvNXmLUQfGJfC0wReUU1Z%3A1762886460394',
                'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
                'mid': mid,
                'tmr_detect': '0%7C1762886465762',
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://moscow.megafon.ru',
                'Pragma': 'no-cache',
                'Referer': 'https://moscow.megafon.ru/perenos_tarifa/drugoy_operator/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                # 'Cookie': 'tmr_lvid=9ff438b1c18f8a9bdd32253a89d02ac2; tmr_lvidTS=1762886458466; _ym_uid=176288645985168560; _ym_d=1762886459; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=2b88142a-e896-4f78-9042-d7d8f806b546; directCrm-session=%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D; _ymab_param=3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ; domain_sid=DvNXmLUQfGJfC0wReUU1Z%3A1762886460394; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; mid=28e12f4c-a753-4c10-9c85-25294ef4557c; tmr_detect=0%7C1762886465762',
            }

            json_data = {
                'msisdn': tel,
            }

            response = requests.post('https://moscow.megafon.ru/api/lk/clone/info', cookies=cookies, headers=headers,
                                     json=json_data)
            json_data = response.json()
            print(json_data)



            cookies = {
                'tmr_lvid': '9ff438b1c18f8a9bdd32253a89d02ac2',
                'tmr_lvidTS': '1762886458466',
                '_ym_uid': '176288645985168560',
                '_ym_d': '1762886459',
                '_ym_visorc': 'b',
                '_ym_isad': '2',
                'mindboxDeviceUUID': '2b88142a-e896-4f78-9042-d7d8f806b546',
                'directCrm-session': '%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D',
                '_ymab_param': '3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ',
                'domain_sid': 'DvNXmLUQfGJfC0wReUU1Z%3A1762886460394',
                'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
                'mid': mid,
                'tmr_detect': '0%7C1762886465762',
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://moscow.megafon.ru',
                'Pragma': 'no-cache',
                'Referer': 'https://moscow.megafon.ru/perenos_tarifa/drugoy_operator/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                # 'Cookie': 'tmr_lvid=9ff438b1c18f8a9bdd32253a89d02ac2; tmr_lvidTS=1762886458466; _ym_uid=176288645985168560; _ym_d=1762886459; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=2b88142a-e896-4f78-9042-d7d8f806b546; directCrm-session=%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D; _ymab_param=3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ; domain_sid=DvNXmLUQfGJfC0wReUU1Z%3A1762886460394; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; mid=28e12f4c-a753-4c10-9c85-25294ef4557c; tmr_detect=0%7C1762886465762',
            }

            json_data = {
                'msisdn': tel,
            }


            response = requests.post('https://moscow.megafon.ru/api/lk/clone/otp/request', cookies=cookies, headers=headers, json=json_data)

            json_data = response.json()
            print(json_data)

            if response.status_code == 200:
                return await chat.reply("Информацию принял, передаю. Ждите SMS и введите код")
            else:
                return await chat.reply("Ошибка! " + json_data)

        #отвечаем на все остальные неопознанные сообщения
        #return chat.reply("Введите только 10 цифр номера")

        #если текст входящего сообщение подходит под формат Кода (6 чисел)
        if (re.fullmatch(r"(\d{6})", message['text'])):
            print(message['text'])
            #await channel.forward_message(chat.id, message['message_id'])

            cookies = {
                'tmr_lvid': '9ff438b1c18f8a9bdd32253a89d02ac2',
                'tmr_lvidTS': '1762886458466',
                '_ym_uid': '176288645985168560',
                '_ym_d': '1762886459',
                '_ym_visorc': 'b',
                '_ym_isad': '2',
                'mindboxDeviceUUID': '2b88142a-e896-4f78-9042-d7d8f806b546',
                'directCrm-session': '%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D',
                '_ymab_param': '3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ',
                'domain_sid': 'DvNXmLUQfGJfC0wReUU1Z%3A1762886460394',
                'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
                'tmr_detect': '0%7C1762886465762',
                'mid': mid,
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://moscow.megafon.ru',
                'Pragma': 'no-cache',
                'Referer': 'https://moscow.megafon.ru/perenos_tarifa/drugoy_operator/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'X-API-Scope': 'browser',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                # 'Cookie': 'tmr_lvid=9ff438b1c18f8a9bdd32253a89d02ac2; tmr_lvidTS=1762886458466; _ym_uid=176288645985168560; _ym_d=1762886459; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=2b88142a-e896-4f78-9042-d7d8f806b546; directCrm-session=%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D; _ymab_param=3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ; domain_sid=DvNXmLUQfGJfC0wReUU1Z%3A1762886460394; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; tmr_detect=0%7C1762886465762; mid=926cd472-e11b-45e4-a25b-0302c1debbbb',
            }

            params = {
                'mid': mid,
            }

            data = {
                'msisdn': tel,
                'priority': '2',
            }

            response = requests.post(
                'https://moscow.megafon.ru/api/unite/v1/cdss/set?mid='+mid,
                params=params,
                cookies=cookies,
                headers=headers,
                data=data,
            )
            json_data = response.json()
            print(json_data)

            cookies = {
                'tmr_lvid': '9ff438b1c18f8a9bdd32253a89d02ac2',
                'tmr_lvidTS': '1762886458466',
                '_ym_uid': '176288645985168560',
                '_ym_d': '1762886459',
                '_ym_visorc': 'b',
                '_ym_isad': '2',
                'mindboxDeviceUUID': '2b88142a-e896-4f78-9042-d7d8f806b546',
                'directCrm-session': '%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D',
                '_ymab_param': '3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ',
                'domain_sid': 'DvNXmLUQfGJfC0wReUU1Z%3A1762886460394',
                'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
                'tmr_detect': '0%7C1762886465762',
                'mid': mid,
            }

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://moscow.megafon.ru',
                'Pragma': 'no-cache',
                'Referer': 'https://moscow.megafon.ru/perenos_tarifa/drugoy_operator/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                # 'Cookie': 'tmr_lvid=9ff438b1c18f8a9bdd32253a89d02ac2; tmr_lvidTS=1762886458466; _ym_uid=176288645985168560; _ym_d=1762886459; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=2b88142a-e896-4f78-9042-d7d8f806b546; directCrm-session=%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D; _ymab_param=3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ; domain_sid=DvNXmLUQfGJfC0wReUU1Z%3A1762886460394; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; tmr_detect=0%7C1762886465762; mid=926cd472-e11b-45e4-a25b-0302c1debbbb',
            }

            json_data = {
                'otp': message['text'],
                'msisdn': tel,
            }

            response = requests.post('https://moscow.megafon.ru/api/lk/clone/otp/submit', cookies=cookies, headers=headers, json=json_data)
            print(response)
            print(response.status_code)
            json_data = response.json()
            print(json_data)

            if response.status_code == 200:
                await chat.reply("Код верный")

                cookies = {
                    'tmr_lvid': '9ff438b1c18f8a9bdd32253a89d02ac2',
                    'tmr_lvidTS': '1762886458466',
                    '_ym_uid': '176288645985168560',
                    '_ym_d': '1762886459',
                    '_ym_visorc': 'b',
                    '_ym_isad': '2',
                    'mindboxDeviceUUID': '2b88142a-e896-4f78-9042-d7d8f806b546',
                    'directCrm-session': '%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D',
                    '_ymab_param': '3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ',
                    'domain_sid': 'DvNXmLUQfGJfC0wReUU1Z%3A1762886460394',
                    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
                    'tmr_detect': '0%7C1762886465762',
                    'mid': mid,
                    'cookies-informer': '%7B%22version%22%3A%2215.242%22%2C%22closed%22%3Atrue%7D',
                }

                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    'Origin': 'https://moscow.megafon.ru',
                    'Pragma': 'no-cache',
                    'Referer': 'https://moscow.megafon.ru/perenos_tarifa/drugoy_operator/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    # 'Cookie': 'tmr_lvid=9ff438b1c18f8a9bdd32253a89d02ac2; tmr_lvidTS=1762886458466; _ym_uid=176288645985168560; _ym_d=1762886459; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=2b88142a-e896-4f78-9042-d7d8f806b546; directCrm-session=%7B%22deviceGuid%22%3A%222b88142a-e896-4f78-9042-d7d8f806b546%22%7D; _ymab_param=3Mupkveh2_bgDHFXfCJXbKKgUQdqoWBaRcSSPKb-PTfIbyfiBtJkupw_I7KDf1_N8pnXR-Fj9slwXz2O1pN7jHHBhNQ; domain_sid=DvNXmLUQfGJfC0wReUU1Z%3A1762886460394; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; tmr_detect=0%7C1762886465762; mid=926cd472-e11b-45e4-a25b-0302c1debbbb; cookies-informer=%7B%22version%22%3A%2215.242%22%2C%22closed%22%3Atrue%7D',
                }

                json_data = {
                    'msisdn': tel,
                    'minute': 2000,
                    'internet': 999999999,
                    'price': 390,
                }

                response = requests.post('https://moscow.megafon.ru/api/lk/clone', cookies=cookies, headers=headers,
                                         json=json_data)

                print(response)
                print(response.status_code)
                json_data = response.json()
                print(json_data)


                if response.status_code == 200:
                    return await chat.reply("Ваш Промокод для " + tel + " :\n" + json_data['value'])
                else:
                    return await chat.reply("Ошибка! " + json_data['error']['message'])

            else:
                return await chat.reply("Ошибка! " + json_data['error']['message'])

            #отвечаем на все остальные неопознанные сообщения
        return chat.reply("Введите только 10 цифр номера или 6 цифр SMS кода")

    tel = None
    channels = []
    #создадим соединения с админами
    for a in admins:
        channels.append(  bot.channel(a))
    #@todo убрать временный костыль. отправка сообщения о старте первому из Админов
    channels[0].send_text("Стартую. Введите 10 цифр номера")
    channels[1].send_text("Стартую. Введите 10 цифр номера")
    bot.run()
