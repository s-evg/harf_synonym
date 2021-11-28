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

INFO_1 = 'Для того чтобы найти синонимы'
INFO_2 = 'введите слово в поле для ввода.'


def get_synonym_view(request):
    """
    :param request: слово
    :return: снисок синонимов
    """

    word = request.GET.get("word")
    template_name = 'synonym/index.html'
    if word is None:
        context = {
            'info_1': INFO_1,
            'info_2': INFO_2,
            'syn_list': [{'syn': [{'text': 'Введите слово!'}]}],
            'word': ''
        }
        return render(request, template_name, context)

    else:

        try:
            queryset = Word.objects.get(text=word)
            syn = Word.objects.filter(syn=word)
            context = {
                'syn': syn,
                'word': word
            }
            return render(request, template_name, context)

        except ObjectDoesNotExist:

            url = URL + ya_token + '&lang=ru-ru&text=' + word

            req_ya = requests.get(url=url, headers=HEADERS).json()

            syn_list = []

            if req_ya.get('def') == []:
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
                    'word': word,
                    'syn_list': syn_list
                }

                return render(request, template_name, context)
