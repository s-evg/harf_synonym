from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from synonym.models import Word
import requests
import os


ya_token = os.environ.get('ya_token')
URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*',
             }


def get_synonym_view(request):
    """
    :param request: слово
    :return: снисок синонимов
    """

    word = request.GET.get("word")
    print(f'REQUEST ------>>>>> {word}')
    template_name = 'synonym/index.html'

    if word is None:
        return render(request, template_name)

    else:

        try:
            queryset = Word.objects.get(text=word)
            syn = Word.objects.filter(syn=word)
            context = {
                'syn': syn,
                'word': word
            }
            print('Попали сюда')
            return render(request, template_name, context)

        except ObjectDoesNotExist:
            # print('Слова нет')

            url = URL + ya_token + '&lang=ru-ru&text=' + word

            print(url)
            req_ya = requests.get(url=url, headers=HEADERS).json()

            syn_list = []

            # pprint(req_ya)
            print(f"GET =========>>>>>>>>>> {req_ya.get('def')}")

            if req_ya.get('def') is None:
                print('Некорректное слово')
                context = {
                    'syn_list': [{'syn': [{'text': 'Некорректное слово, или пустой запрос.'}]}],
                    'word': word

                }
                return render(request, template_name, context)

            else:
                text = req_ya['def'][0]['text'] # запрашиваемое слово / фраза
                pos = req_ya['def'][0]['pos'] # часть речи

                for i in req_ya['def']:

                    for q in i['tr']:
                        tr = q.get('text')
                        syn = q.get('syn')

                        syn_list.append({
                            'tr': tr,
                            'syn': syn,
                        })

                context = {
                    'text': text,
                    'syn_list': syn_list
                }

                pprint(syn_list)

                return render(request, template_name, context)
