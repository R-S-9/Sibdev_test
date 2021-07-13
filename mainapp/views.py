from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect

# from .forms import FileForm


@csrf_exempt
def index(request):
    if request.method == 'POST':
        # Если в запросе есть файл - рендерит страницу с таблицей и ссылкой на скачивание файла
        if request.FILES:
            # form = FileForm(request.POST, request.FILES)
            # if form.is_valid():
            #
            #     # handle_uploaded_file(request.FILES['file'])
            #     return HttpResponseRedirect('/success/url/')
            #
            # print(request.FILES)
            # print('YES')

            # frame = get_frame(file_path=request.session['file_path'])
            # request.session['frame'] = frame.to_json()
            # return render(request, 'elements.html', {
            #     'headTable': get_head_table(frame),
            #     'describeTable': get_describe_table(frame),
            #     'link': request.session['file_path'],
            # })
            ...
        return JsonResponse(data={})

    else:
        return render(request, 'main.html', context={})
