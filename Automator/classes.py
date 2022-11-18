from FileGenerator.classes import TextFileGenerator
import os
import requests

from random import randint
import time
import datetime


class VJudge:
    def __init__(self, data):
        self.__data = data

        self.__handle_non_required_properties()

        self.__session = requests.Session()
        self.__session.cookies.set(
            "Jax.Q", self.__data['cookies']['Jax.Q'], domain=".vjudge.net")
        self.__session.post('https://vjudge.net/user/checkLogInStatus')

    def automate(self):
        print('get data from Vjudge...')
        submissions = self.__get_contest_status()

        if len(submissions) == 0:
            print(
                'can NOT get data from vjudge :(, please make sure you set correct contestId and cookies OR maybe there is no submission after the entered date and time')
            return

        print('clean data...')
        submissions = list(filter(
            lambda sub: sub['time'] >= self.__data['dateAndTime'], submissions))

        print('get sharable problem links...')
        shareable_submissions = self.__make_sharable(submissions)

        print('sort data...')
        sorted_shareable_submissions = sorted(shareable_submissions, key=lambda d: (
            d['contestNum'], d['languageCanonical'], -d['time']))

        print('re-formatting data...')
        prime_keys = ['contestNum', 'languageCanonical', 'link']
        grouped_data = self.__group_list_by(
            sorted_shareable_submissions, prime_keys)

        print('generating file...')
        TextFileGenerator().generate(grouped_data, os.getcwd(),
                                     self.__data.get('generatedFileName', ''))
        print(f'generated file name: {self.__data["generatedFileName"]}')
        print('DONE! :)')

    def __get_contest_status(self):
        url = 'https://vjudge.net/status/data'
        params = {
            'contestId': self.__data['contestId'],
            'draw': '1',
            'start': '0',
            'length': '20',
            'res': '1',
            'num': '-',
            'inContest': 'true',
            'un': self.__data['username']
        }

        final_data = []
        while True:
            params['start'] = str(len(final_data))
            response = self.__session.get(url=url, params=params)
            data = response.json()['data']
            if len(data):
                final_data.extend(data)
            else:
                break

        return final_data

    def __make_sharable(self, submissions):
        for d in submissions:
            response = self.__session.post(
                f'https://vjudge.net/solution/shareText/{d["runId"]}')
            shareable_link = f'https://vjudge.net/solution/{d["runId"]}/{response.text}'
            d['link'] = shareable_link
        return submissions

    def __group_list_by(self, list, prime_keys):
        res = {}

        def insert(res, el, prime_keys, index):
            key = prime_keys[index]
            if index + 1 == len(prime_keys):
                res.append(el[key])
                return

            if index + 2 == len(prime_keys):
                if not el[key] in res:
                    res[el[key]] = []
                insert(res[el[key]], el, prime_keys, index + 1)
                return

            if not el[key] in res:
                res[el[key]] = {}

            insert(res[el[key]], el, prime_keys, index + 1)

        for d in list:
            insert(res, d, prime_keys, 0)

        return res

    def __handle_non_required_properties(self):
        if len(self.__data.get('dateAndTime', '')) == 0:
            self.__data['dateAndTime'] = -999999
        else:
            self.__data['dateAndTime'] = int(time.mktime(
                datetime.datetime.strptime(self.__data['dateAndTime'], '%Y-%m-%d %H:%M').timetuple())) * 1000

        self.__data['username'] = self.__data['cookies']['Jax.Q'].split('|')[0]

        if len(self.__data.get('generatedFileName', '')) == 0:
            self.__data['generatedFileName'] = self.__data['username'] + "_" + \
                self.__data['contestId'] + "_" + str(randint(10000, 99999))
