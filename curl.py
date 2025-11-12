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
    'minute': 5000,
    'internet': 999999999,
    'price': 300,
}

response = requests.post('https://moscow.megafon.ru/api/lk/clone', cookies=cookies, headers=headers, json=json_data)

print(response)
print(response.status_code)
json_data = response.json()
print(json_data)