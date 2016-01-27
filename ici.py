#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import re
from xml.dom import minidom
from collections import namedtuple

import requests
import webbrowser
from wox import Wox,WoxAPI

KEY = 'E0F0D336AF47D3797C68372A869BDBC5'
URL = 'http://dict-co.iciba.com/api/dictionary.php'


class Main(Wox):

    ex_count = 0

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
                }

    def query(self, args):
        response = self.request([i.lower() for i in args.split(' ')])
        if not response:
            return
        return [i for i in self.parse(response.json())]
        for i in self.parse(root):
            title = i[0]
            url = None
            results.append({
                "Title": repr(title),
                "SubTitle": i[-1].decode('utf-8'),
                # "IcoPath": "Images/app.ico",
                "JsonRPCAction": {
                    # See https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs
                    "method": "openUrl",
                    #参数必须以数组的形式传过去
                    "parameters": [url],
                    #是否隐藏窗口
                    "dontHideAfterAction": True
                }
            })

        return results

if __name__ == '__main__':
    Main()
