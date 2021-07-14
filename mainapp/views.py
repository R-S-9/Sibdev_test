import csv

from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CustomerLog, PurchasedItems


@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        csv_file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)

        data = handle_uploaded_file(filename)
        print(len(data))

        return render(request, 'csv_output.html', {
            'csv_file': data[:10]
        })
    else:
        return render(request, 'main.html')


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
                'date': content['date'],
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


def delet_all_db(request):
    CustomerLog.objects.all().delete()
    return index(request)
