import csv
import decimal
import json
import os
from operator import itemgetter
from collections import OrderedDict
import pandas as pd

from django.core.exceptions import ValidationError

from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from .models import CustomerLog, PurchasedItems


@csrf_exempt
def index(request):
    err = ''

    if request.method == 'POST':
        try:
            file = request.FILES['myfile']

        except MultiValueDictKeyError:
            file = None
            err = 'Выберите файл для обработки, и отправиьте его.'

        if file:
            csv_file = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)

            data = handle_uploaded_file(filename)

            if not data:
                err = 'Произошла ошибка.\nВ отправленом вами файле нет ' \
                      'данных. Проверте файл и отправьте файл повторно.'

            elif type(data) is str:
                err = data

            try:
                df = pd.read_csv('media/' + filename)
                json_records = df.reset_index().to_json(orient='records')
                geeks_object = json.loads(json_records)
            except UnicodeDecodeError:
                err = 'Ошибка в кодировании или файле.'
                geeks_object = False

            except pd.errors.ParserError:
                err = 'Ошибка файла.'
                geeks_object = False

            finally:
                os.remove('media/' + filename)

                if type(data) is list:
                    data = len(data)
                else:
                    data = ''

            return render(request, 'csv_output.html', {
                'csv_error': err,
                'd': geeks_object,
                'data_len': data
            })

    return render(request, 'main.html', context={'err': err})


def is_adv_digit(digit):
    digit_list = list(str(digit))

    if digit_list[0] == '-':
        return ValidationError

    for inter in digit_list:
        if not inter.isdigit():
            return False

    return digit


def handle_uploaded_file(media_file):
    """Фун-ия для чтения и записи в bd полученых данных"""

    data = []
    error = False

    with open('media/' + media_file, mode="r", encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=",", lineterminator="\r")

        try:
            for content in read:
                try:
                    if content['customer'] == '':
                        return 'Ошибка логина.'

                    if content['item'] == '':
                        return 'Ошибка имени предмета.'

                    if is_adv_digit(content['total']) is False:
                        return 'Ошибка чека - Не число.'

                    elif is_adv_digit(content['total']) is ValidationError:
                        return 'Ошибка чека - Итог не может быть ' \
                               'отрицательным.'

                    if is_adv_digit(content['quantity']) is False:
                        return 'Ошибка в кол-ве предметов - не число.'

                    elif is_adv_digit(content['quantity']) is ValidationError:
                        return 'Ошибка в данных. Кол-во не может быть ' \
                               'отрицательным.'

                except KeyError:
                    error = True
                    break

                data.append({
                    'customer': content['customer'],
                    'item': content['item'],
                    'total': content['total'],
                    'quantity': content['quantity'],
                    'date_time': content['date'][:16],
                })

                try:
                    post_form = CustomerLog.objects.create(
                        customer=content['customer'],
                        date=content['date']
                    )

                except ValidationError:
                    return 'Ошибка в дате. Значение должно быть в формате ' \
                           'YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ].'

                post_form.save()

                try:
                    pur_item = PurchasedItems.objects.create(
                        customer_item_id=post_form.id,
                        item=content['item'],
                        total=content['total'],
                        quantity=content['quantity'],
                    )

                except decimal.InvalidOperation:
                    return 'Ваше число намного больше чем это прописано в ' \
                           'модели. Пожалуйста, проверьте точность данных ' \
                           'или измените модель total/max_digits=(на то ' \
                           'число, которое подходит для вас)'

                except ValidationError:
                    return 'Произошла ошибка. Значение чек/total должно быть' \
                           'десятичным числом.'

                except ValueError:
                    return 'Произошла ошибка в кол-ве купленных преметов.'

                post_form.save()
                pur_item.save()

        except UnicodeDecodeError:
            data = 'Проверьте файл и кодировку.'

    if error:
        data = 'Ошибка в файле или в данных в нем. Возможно вы отправили ' \
               'не csv файл. Проверте файл и попытайтесь снова.'

    return data


def del_all_db(request):
    CustomerLog.objects.all().delete()

    return index(request)


def user_gems(data):
    list_of_gems = []

    for v in data:
        cus = CustomerLog.objects.filter(
            customer=v.get('username')
        ).values_list('pur_item__item', flat=True)

        no_duplicates_gems = list(OrderedDict.fromkeys(cus))

        list_of_gems.append({
            'username': v.get('username'),
            'gems': no_duplicates_gems
        })

    gems = [
        list_of_gems[inter].get('gems') for inter in range(len(list_of_gems))
    ]

    return gems


def top_clients(request):
    last_value = ''
    customers = CustomerLog.objects.all().order_by('customer')
    customers_names = []

    for name in customers:
        if name.customer not in last_value:
            customers_names.append(name)

        last_value = name.customer

    data = []  # Список для хранения топ 5 клиентов.

    for i in customers_names:
        list_of_customer = CustomerLog.objects.filter(
            customer=i.customer
        )

        sum_total = list_of_customer.aggregate(
            spent_money=Sum('pur_item__total')
        )

        data.append({
            'username': i.customer,
            'spent_money': sum_total['spent_money']
        })

    data.sort(key=itemgetter('spent_money'), reverse=True)

    # Топ 5 клиентов (Логины, потраченые средства)
    data = data[:5]

    gems_customer = user_gems(data)

    lol = [item.get('username') for item in data]

    gems_of_customer = []  # Список для хранения предметов топ 5 клиентов.
    output_data = []

    for j in range(len(gems_customer)):
        for i in gems_customer[j]:
            list_of_customer = CustomerLog.objects.filter(
                pur_item__item=i,
                pur_item__quantity__gt=2,
            ).values_list('customer', flat=True)

            list_of_customer = list(OrderedDict.fromkeys(list_of_customer))

            gems_of_customer.append({
                'customer': list_of_customer,
                'gems': i
            })

        customer_log = data[j].get('username')
        customer_top_spent_money = data[j].get('spent_money')

        gems_name = gems_of_customer[j].get('gems')

        identical_gems = [
            j for item in gems_of_customer for j in item.get('customer')
            if j in lol
        ]

        output_data.append(
            {
                'customer_log': customer_log,
                'customer_top_spent_money': customer_top_spent_money,
                'gems_name': gems_name,
                'identical_gems': identical_gems,
            }
        )

    '''
        Сделать отдельный список gems в котором будет отдельные предметы и 
        рядом список тех, кто купил его больше 2х раз.
    '''

    # CustomerLog.objects.all().delete()

    if not output_data:
        output_data = 'Ошибка в файле. Повторите попытку загрузив данные с ' \
                      'файла снова'

    return render(request, 'csv_output.html', context={
        'output_data': output_data
    })
