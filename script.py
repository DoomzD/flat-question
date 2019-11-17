import requests
import time
import telepot
import difflib
import json

from bs4 import BeautifulSoup


TOKEN = 'xxx'

URLs = {
    'yandex': 'https://realty.yandex.ru/moskva/snyat/kvartira/studiya,1-komnatnie/?priceMax=32000&metroTransport=ON_FOOT&timeToMetro=15&priceMin=20000&sort=DATE_DESC',
    'avito': 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok?f=550_5702-5703&pmax=32000&pmin=25000&s=104&s_trg=4',
    # 'cian': 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&foot_min=15&maxprice=32000&minprice=20000&offer_type=flat&only_foot=2&region=1&room1=1&room9=1&type=4',
    # 'domofond': 'https://www.domofond.ru/arenda-kvartiry-moskva-c3584?PriceFrom=20000&PriceTo=32000&RentalRate=Month&Rooms=One%2CStudio&SortOrder=Newest&DistanceFromMetro=UpTo1000m',
}
IDs = {
    'Alex': 'xxx',
    'Ksusha': 'xxx',
}

HEADERS = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 YaBrowser/18.11.1.716 Yowser/2.5 Safari/537.36',
    'X-Ya-Front-Host': 'yandex.ru',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9',
    # 'Cookie': 'yandexuid=7699359971544005373; _ym_uid=1544008773812746315; mda=0; yandex_gid=213; my=YwA=; fuid01=5c11408f7cad109c.dTDWJJ8Zzh8-xjd6xpfRQMy3QgR1udtwRrUVMOmP8cWLEXXFobGYUG1istqrQPYo0QXVZ4IejVkiZ5ChTfO4fmZflk6vrFYJ9Qtvu5Cx6j_5mrgeICvuO9clgCSe5Axi; suid=738bfc48dcae921e9e1a580a915eb395.2f980f60b2763a2e65f097667556edeb; blcrm=1; offer_map_transport=auto; _ym_d=1545559905; zm=m-white_bender.webp.css-https%3Awww_JCLZKhmgme1dTevqhMpu3q3ZVLI%3Al; yc=1545819107.zen.cach%3A1545563504; cto_lwid=9b09fd1a-12c7-4af7-ad45-ddc84fcc72ba; __utma=190882677.1645957643.1545729024.1545729024.1545729024.1; __utmz=190882677.1545729024.1.1.utmcsr=game_pinata|utmccn=(not%20set)|utmcmd=pr; __utmv=190882677.|2=Account=Yes=1^3=Login=Yes=1; _ga=GA1.2.1645957643.1545729024; L=XmBhflNFBWpqBEV1WXkFbmloUE9WcXF4BhodNzs3EA==.1545839254.13726.398326.37aad83a35853b5298fa829b1301bc8f; yandex_login=DoomzzD; i=gMY5tPeKQ/gHKwwOLsdKOkTY0v/InfcPlV7Ofa7B6sa8UmKTAL2G1zMkaAUg2AY1NvqHsLnpN+Vxul5GJVj0EKKnxF8=; yabs-frequency=/4/1W0205Ro95mWNXbS/t5MmS4WpGG00/; offer_map_zoom=10; ys=mailchrome.8-22-3-1#ybzcc.ru#svt.1#def_bro.1#musicchrome.0-0-472-1; from=direct; _csrf=vOue29uQJeSdZz0wPxlLxq6u; device_id="ae1a47de9ba559b6cbf516d0749709be69f7370b7"; subscription_popup_count=0; subscription_popup_shown=1; rheftjdd=rheftjddVal; Session_id=3:1546359794.5.0.1545839254776:gnc_Q_pUswgMRgAAuAYCKg:50.1|531295415.0.302.0:3|192796.207092.hc3gULKoSw55TgQX5uwZXmCQhTU; sessionid2=3:1546359794.5.0.1545839254776:gnc_Q_pUswgMRgAAuAYCKg:50.1|531295415.0.302.0:3|192796.620774.5zngRyEDfagoKI-SYHs5nRxfRb4; X-Vertis-DC=sas; bltsr=1; _ym_visorc_2119876=w; _ym_isad=1; tmr_detect=1%7C1546422588060; _fbp=fb.1.1546422588113.681205772; from_lifetime=1546422593286; yp=1575541373.cld.1955450#2145906000.yb.18_10_2_172:0:1544014822:1545391540:244:0#1548527850.shlos.1#1562135739.szm.2:1440x900:1440x828#1547226510.ygu.1#1546769509.ysl.1#1860315590.multib.1#1861199254.udn.cDrQkNC70LXQutGB0LXQuSDQmtC%2B0YDRj9C60L7Qsg%3D%3D#1546430012.gpauto.53_931049:30_356724:140:1:1546422812#1577219896.as.1',
}


def get_diff(a, b):
    for i, s in enumerate(difflib.ndiff(a, b)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            print(u'Delete "{}" from position {}'.format(s[-1], i))
        elif s[0] == '+':
            print(u'Add "{}" to position {}'.format(s[-1], i))
    print()


def pretty_json(json_string):
    return json.dumps(json_string, indent=4, ensure_ascii=False)


def parse_yandex(cur_soups, fl=False):
    '''
        takes <div class='i-react-state i-bem' data-bem=...>, where data-bem contains all info
        flats are taken from 'data-bem -> i-react-state -> state -> search -> offers -> entities'
        :return list:
    '''
    soup = cur_soups['yandex']

    flats_block = str(soup.find('div', {'class': 'i-react-state i-bem'})['data-bem'])
    json_string = json.loads(flats_block)

    flats = json_string['i-react-state']['state']['search']['offers']['entities']

    # print(pretty_json(flats))

    if fl:
        for flat in flats:
            print('https:' + flat['unsignedInternalUrl'])
            print(flat['predictions']['predictedPrice']['min'] + ' to ' + flat['predictions']['predictedPrice']['max'])
            print()

    descs = []
    for flat in flats:
        if 'description' in flat:
            descs.append(flat['description'])

    return descs


def parse_avito(cur_soups):
    soup = cur_soups['avito']

    flats = soup.find_all('div', {'class': 'about', 'itemprop': 'offers'})
    return flats


# TODO: make this shit work
def parse_cian(cur_soups):
    soup = cur_soups['cian']

    flats = soup.find_all('div', {'class': 'c6e8ba5398-term--39cia'})
    return flats


def parse_domofond(cur_soups):
    soup = cur_soups['domofond']

    flats = soup.find_all('div', {'class': 'e-description-text', 'itemprop': 'description'})
    return flats


def get_unique_info(cur_soups):
    return [
        parse_yandex(cur_soups),
        parse_avito(cur_soups),
        # parse_cian(cur_soups),
        # parse_domofond(cur_soups)
    ]


telebot = telepot.Bot(token=TOKEN)

start_states = {name: requests.get(url, headers=HEADERS) for name, url in URLs.items()}
soups = {name: BeautifulSoup(start_state.text.encode(start_state.encoding).decode('utf-8'), 'html.parser') for name, start_state in start_states.items()}

serps = get_unique_info(soups)

for person, id in IDs.items():
    telebot.sendMessage(id, 'I\'m alive!')

cnt = 0
while True:
    try:
        new_states = {name: requests.get(url, headers=HEADERS) for name, url in URLs.items()}
        new_soups = {name: BeautifulSoup(new_state.text.encode(new_state.encoding).decode('utf-8'), 'html.parser') for name, new_state in new_states.items()}
        new_serps = get_unique_info(new_soups)

        for url, serp, old_serp, i in zip(URLs, new_serps, serps, range(len(serps))):
            if url == 'yandex' and serp != old_serp:
                for person, id in IDs.items():
                    telebot.sendMessage(id, '{}: Hey {}, smth happend on {}'.format(url, person, URLs[url]))
                serps[i] = serp
            elif url == 'avito' and (serp[1] != old_serp[1] or serp[2] != old_serp[2]):
                for person, id in IDs.items():
                    telebot.sendMessage(id, '{}: Hey {}, smth happend on {}'.format(url, person, URLs[url]))
                serps[i] = serp

        print('Iteration #{} done'.format(cnt))
        cnt += 1
        time.sleep(15)
    except:
        time.sleep(10)
        continue

