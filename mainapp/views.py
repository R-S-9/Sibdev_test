import csv

from django.core.files.storage import FileSystemStorage

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
                data = 'Произошла ошибка.\nВ отправленом вами файле нет ' \
                       'данных. Проверте файл и отправьте файл повторно.'
            else:
                data = data[:10]

            return render(request, 'csv_output.html', {
                'csv_file': data
            })

    return render(request, 'main.html', context={'err': err})


def handle_uploaded_file(file):
    """Фун-ия для чтения и записи в переменную полученых данных"""

    data = []

    with open('media/' + file, mode="r", encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=",", lineterminator="\r")
        for content in read:
            data.append({
                'customer': content['customer'],
                'item': content['item'],
                'total': content['total'],
                'quantity': content['quantity'],
                'date_time': content['date'][:16],
            })

            post_form = CustomerLog.objects.create(
                customer=content['customer'],
                date=content['date']
            )
            post_form.save()

            PurchasedItems.objects.create(
                customer_item_id=post_form.id,
                item=content['item'],
                total=content['total'],
                quantity=content['quantity'],
            )

    return data


def del_all_db(request):
    CustomerLog.objects.all().delete()

    return index(request)


def top_clients(request):
    ...
