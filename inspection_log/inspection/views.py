from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms
import datetime, os, json


def home(request):
    return render(request, 'inspection/index.html', {})


def inspection_log(request):
    '''
    Журнал осмотра
    '''
    log = models.Inspection_log.objects.all()
    return render(request, 'inspection/inspection_log.html', {'logs': log[::-1]})


def handle_uploaded_file(f, name):
    '''
    загрузка картинки в static
    '''
    id_log = models.Inspection_log.objects.all().last().id + 1
    with open(f"inspection/static/downloadimages/{id_log}/{name}.jpg", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



def log_form(request):
    '''
    Форма здля записи в журнал
    '''
    if request.method == 'POST':
        form = forms.LogForms(request.POST, request.FILES)
        id_log = models.Inspection_log.objects.all().last().id + 1
        count_img = 0
        image_dict = {}
        images_name = []
        if form.is_valid():
            if not os.path.isdir(f"inspection/static/downloadimages/{id_log}"): # если папки нету, создаёт новую
                os.mkdir(f"inspection/static/downloadimages/{id_log}")          # с именем id записи
                new_path = f"inspection/static/downloadimages/{id_log}"
            else:
                new_path = f"inspection/static/downloadimages/{id_log}"

            for i in request.FILES.getlist('myFile'):                           # итерация по добавленным файлам и получение байт кода
                count_img += 1                                                  # кол-во фото
                images_name.append(str(i.name))                                    # имена файлов                        
                with open(f"inspection/static/downloadimages/{id_log}/{i.name}", 'wb+') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
            image_dict = {id_log: images_name}
            with open("inspection/static/json/images_name.json", 'w+') as f:
                json.dump(image_dict, f)
            new_log = form.save(commit=False)
            new_log.user_name_id = request.user                                  # сохранение в журнале залогиниившегося юзера
            new_log.responsible_user_id =request.user
            new_log.save()
            return redirect('inspection:inspection_log')
        else:
            return render(request, 'inspection/log_form.html', {'form': form, })
    else:
        form = forms.LogForms()
        return render(request, 'inspection/log_form.html', {'form': form})



def log_details(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    with open("inspection/static/json/images_name.json", 'r') as f:
        image_dict = json.load(f)
    image_list = image_dict[f'{log.id}']

    if not log:
        raise Exception('No such log')
    else:
        return render(request, 'inspection/log_details.html', {'log': log, 'log_id': log_id, 'image_list': image_list})


def update_log(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    form = forms.LogForms(request.POST or None, request.FILES or None, instance=log)
    if form.is_valid():
        new_log = form.save(commit=False)
        new_log.user_name_id = request.user
        new_log.save()
        return redirect('inspection:log_details', log.id)
    return render(request, 'inspection/log_form.html', {'form': form})


def delete_log(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    log.delete()
    logs = models.Inspection_log.objects.all()
    return redirect('inspection:inspection_log')


def substations_all(request):
    substations = models.Inspection_log.objects.filter(substation_name='somebody')
