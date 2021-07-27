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


def log_form(request):
    '''
    Форма для записи в журнал
    '''
    if request.method == 'POST':
        form = forms.LogForms(request.POST, request.FILES)
        id_log = models.Inspection_log.objects.all().last().id + 1              # id для название папки новой формы
        images_name = []                                                        # список для названия фото
        img_path = f"inspection/static/downloadimages/{id_log}"
        if form.is_valid():
            if not os.path.isdir(img_path):                                     # если папки нету, создаёт новую
                os.mkdir(img_path)                                              # с именем id записи

            for i in request.FILES.getlist('myFile'): # итерация по добавленным файлам через input и получение байт кода
                images_name.append(str(i.name))                                 # имена фото
                with open(f"{img_path}/{i.name}", 'wb+') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
            image_dict = {id_log: images_name}
            if not os.path.exists("inspection/static/json/images_name.json"):
                with open("inspection/static/json/images_name.json", 'w') as f:   # в json хранятся значения id записи
                    json.dump(image_dict, f)                                      # и списка имени файлов
            else:
                with open("inspection/static/json/images_name.json", 'r') as f:
                    img_dict = json.load(f)
                    new_dict = {**image_dict, **img_dict}                          # объединение словарей
                    with open("inspection/static/json/images_name.json", 'w') as f:
                        json.dump(new_dict, f)
            new_log = form.save(commit=False)
            new_log.user_name_id = request.user
            new_log.responsible_user_id =request.user
            new_log.save()
            return redirect('inspection:inspection_log')
        else:
            return render(request, 'inspection/log_form.html', {'form': form})
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
