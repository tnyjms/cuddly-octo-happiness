# -*- coding: UTF-8 -*-
''' 
Parses CoinMarketdatacap site for growing coins
'''

import json
from math import isnan
from operator import itemgetter

import requests
from bs4 import BeautifulSoup, element

FIELDS = '''#	Name	Symbol	Market Cap	Price	Circulating Supply	Volume (24h)	% 1h	% 24h	% 7d'''.decode(
    'utf-8')


class Coin(object):
    ''' Coin operations'''

    def __init__(self, fetch=False):
        self.coins = []
        self.fetch = fetch
        self._getCoinMarketDetails()

    def _getCoinMarketDetails(self):
        if not self.fetch:
            with open('data.json', 'r') as f:
                self.coins = json.load(f)
        else:
            page = requests.get('https://coinmarketcap.com/all/views/all/')
            page.raise_for_status()
            soup = BeautifulSoup(page.content, 'html.parser').find_all('tr')
            data, data_btc = {}, {}
            # FIELDS = [i for i in soup[0].text.strip().split('\n')]
            for coin in soup[1:]:
                if isinstance(coin, element.Tag) and coin.has_attr('class'):
                    _, No, _, Name, _, Symbol, _, Market_Cap, _, Price, _, Circulating_Supply, _, Volume_24h, _, hour, _, day, _, week, _, _, _ = coin
                    data['#'] = No.get_text().replace(' ', '').strip()
                    data['Name'] = Name.find(
                        class_='currency-name-container').get_text()
                    data['Symbol'] = Symbol.get_text()
                    try:
                        data['Market Cap'] = float(
                            Market_Cap.attrs['data-usd'])
                        data_btc['Market Cap'] = float(
                            Market_Cap.attrs['data-btc'])
                    except ValueError:
                        data['Market Cap'] = data_btc['Market_Cap'] = 0
                    try:
                        data['Price'] = float(Price.find(
                            class_='price').attrs['data-usd'])
                        data_btc['Price'] = float(Price.find(
                            class_='price').attrs['data-btc'])
                    except ValueError:
                        data['Price'] = data_btc['Price'] = 0
                    try:
                        data['Circulating Supply'] = float(
                            Circulating_Supply.find(['a', 'span']).attrs['data-supply'])
                    except ValueError:
                        data['Circulating Supply'] = float(0)
                    try:
                        data['Volume (24h)'] = float(
                            Volume_24h.find(class_='volume').attrs['data-usd'])
                        data_btc['Volume (24h)'] = float(
                            Volume_24h.find(class_='volume').attrs['data-btc'])
                    except ValueError:
                        data['Volume (24h)'] = data_btc['Volume (24h)'] = 0
                    try:
                        data['% 1h'] = float(hour.attrs['data-percentusd'])
                    except KeyError:
                        data['% 1h'] = float('nan')
                    try:
                        data['% 24h'] = float(day.attrs['data-percentusd'])
                    except KeyError:
                        data['% 24h'] = float('nan')
                    try:
                        data['% 7d'] = float(week.attrs['data-percentusd'])
                    except KeyError:
                        data['% 7d'] = float('nan')
                    except ValueError:
                        if week.attrs['data-percentusd'] == '> 9999':
                            data['% 7d'] = float(10000)
                    self.coins.append(data.copy())
            with open('data.json', 'w') as f:
                json.dump(self.coins, f)

    @staticmethod
    def print_table(coin_list=None, desc=None):
        ''' Print the coins table'''
        if desc:
            print '-' * 80 + '\n' + '{:^80}'.format(desc) + '\n' + '-' * 80
        print '-' * 80 + '\n' + \
            '\t'.join(sorted(FIELDS.split('\t'))) + '\n' + '-' * 80
        output = []
        if coin_list is not None and coin_list != []:
            for coin in coin_list:
                output.append('\t'.join([str(coin[key])
                                         for key in sorted(coin.keys())]))
        print '\n'.join(output)

    def growing_coins(self, weekly_growth=30):
        negative_coins, positive_coins = [], []
        for i in self.coins:
            h, d, w = i['% 1h'], i['% 24h'], i['% 7d']
            if not isnan(h) and not isnan(d):
                if w > weekly_growth and h > d:
                    if d < 0:
                        negative_coins.append(i)
                    else:
                        positive_coins.append(i)
        return (negative_coins, positive_coins)

    def sort_coins(self, field=None, limit=None, growth=30):
        ''' Limit : Removes the coins below a certain market cap no.'''
        neg, pos = self.growing_coins(growth)
        if not field:
            field = '% 7d'
        neg = sorted(neg, key=itemgetter(field), reverse=True)
        pos = sorted(pos, key=itemgetter(field), reverse=True)
        if limit:
            negative, positive = [], []
            positive = [i for i in pos if int(i['#']) < limit]
            negative = [i for i in neg if int(i['#']) < limit]
        else:
            negative, positive = neg, pos
        self.print_table(negative, '-VE Growth Last Day')
        self.print_table(positive, '+VE Growth Last Day')


if __name__ == '__main__':
    today = Coin(True)
    today.sort_coins(growth=10)
