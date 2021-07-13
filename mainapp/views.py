import csv

from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        csv_file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)

        return render(request, 'csv_output.html', {
            'csv_file': handle_uploaded_file(filename, request)
        })
    else:
        return render(request, 'main.html')


def handle_uploaded_file(file, request):

    with open('media/' + file, mode="r", encoding='utf-8') as file:
        read = csv.DictReader(file, delimiter=",", lineterminator="\r")
        for i in read:
            print(i)
