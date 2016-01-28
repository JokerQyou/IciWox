#!/usr/bin/env python
# encoding:utf-8
from __future__ import unicode_literals

import requests
import webbrowser
from wox import Wox, WoxAPI

KEY = 'E0F0D336AF47D3797C68372A869BDBC5'
URL = 'http://dict-co.iciba.com/api/dictionary.php'


class Main(Wox):

    def request(self, words):
        words = "_".join(words)
        return requests.get(
            URL,
            params={'key': KEY, 'w': words, 'type': 'json'}
        )

    def parse(self, jsonobj):
        for symbol in jsonobj.get('symbols', []):
            for part in symbol.get('parts', []):
                yield {
                    'Title': '{} ({} / {})'.format(
                        jsonobj.get('word_name'),
                        symbol.get('ph_am', ''),
                        symbol.get('ph_en', ''),
                    ),
                    'SubTitle': '{}\t{}'.format(
                        part.get('part', '?'),
                        '\n\t'.join(part.get('means'))
                    ),
                    # "IcoPath": "Images/app.ico",
                    "JsonRPCAction": {
                        # See https://git.io/vz74N
                        "method": "open_url",
                        "parameters": [
                            'http://iciba.com/{}'.format(
                                jsonobj.get('word_name')
                            ),
                        ],
                        # 是否隐藏窗口
                        "dontHideAfterAction": False,
                    },
                }

    def open_url(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

    def query(self, args):
        response = self.request([i.lower() for i in args.split(' ')])
        if not response:
            return
        return [i for i in self.parse(response.json())]

if __name__ == '__main__':
    Main()
