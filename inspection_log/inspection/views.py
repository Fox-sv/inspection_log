from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from . import models, forms
import datetime, os, json
from django.contrib.auth.models import User

def home(request):
    return render(request, 'index.html', {})


def inspection_log(request):
    '''
    Журнал осмотра и фильтром
    '''
    log = models.Inspection_log.objects.all()
    if request.method == 'POST':
        form = forms.InspectionLogForm(request.POST)                            # форма фильтра
        if form.is_valid():
            clean_data = form.cleaned_data
            substation_name = clean_data['substation_name']
            date_time_start = clean_data['date_time_start']
            date_time_last = clean_data['date_time_last']
            developer = clean_data['developer']
            if date_time_start == None:                                         # если дата не заполнена, автоматически вносится
                date_time_start = datetime.date(2010, 1, 1)
            if date_time_last == None:
                date_time_last = datetime.date(2050, 1, 1)
            if developer != '0':
                find_user_id = User.objects.filter(username=developer)[0].id    # получение id пользователя по логину
                find_user_id_last = find_user_id
            else:
                find_user_id = 1
                find_user_id_last = len(User.objects.all())                     
            if len(substation_name) != 0:                                       # если ведено название подстанции           
                log = models.Inspection_log.objects.filter(substation_name=substation_name, date_record__lte=date_time_last, 
                    date_record__gte=date_time_start, user_name_id__gte=find_user_id, user_name_id__lte=find_user_id_last)
            else:
                log = models.Inspection_log.objects.filter(date_record__lte=date_time_last, 
                    date_record__gte=date_time_start, user_name_id__gte=find_user_id, user_name_id__lte=find_user_id_last)
            return render(request, 'inspection/inspection_log.html', {'logs': log[::-1], 'form': form})
        else:
            return redirect('inspection:inspection_log')
    else:
        form = forms.InspectionLogForm()
        return render(request, 'inspection/inspection_log.html', {'logs': log[::-1], 'form': form})


def log_form(request):
    '''
    Форма для записи в журнал
    '''
    if request.method == 'POST':
        form = forms.LogForms(request.POST, request.FILES)
        images_name = []                                                        # список для названия фото
        if form.is_valid() :
            new_log = form.save(commit=False)
            new_log.user_name_id = request.user
            new_log.responsible_user_id =request.user
            new_log.save()
            id_log = new_log.id
            img_path = f"inspection/static/downloadimages/{id_log}"
            if not os.path.isdir(img_path):                                     # если папки нету, создаёт новую
                os.mkdir(img_path)                                              # с именем id записи
            for i in request.FILES.getlist('myFile'):                   # итерация по добавленным файлам через input и получение байт кода
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
            return redirect('inspection:inspection_log')
        else:
            return render(request, 'inspection/log_form.html', {'form': form,})
    else:
        form = forms.LogForms()
        return render(request, 'inspection/log_form.html', {'form': form, })


def log_details(request, log_id: int):    
    log = models.Inspection_log.objects.get(id=log_id)
    time_ = datetime.datetime.today()
    with open("inspection/static/json/images_name.json", 'r') as f:
        image_dict = json.load(f)
    try:
        image_list = image_dict[f'{log.id}']
    except KeyError:
        image_list = []
    if not log:
        raise Exception('No such log')
    else:
        return render(request, 'inspection/log_details.html', {'log': log, 'log_id': log_id, 'image_list': image_list, 'time1': time_.time()})


def update_log(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    img_path = f"inspection/static/downloadimages/{log_id}"
    form = forms.LogForms(request.POST or None, request.FILES or None, instance=log)
    if form.is_valid():
        with open("inspection/static/json/images_name.json", 'r') as f:
                images_dict = json.load(f)
        try:
            flag = True
            images_name = images_dict[f'{log_id}'] 
        except KeyError:
            flag = False
            images_name = []
        for i in request.FILES.getlist('myFile'):
            images_name.append(f"{i.name}")
            with open(f"{img_path}/{i.name}", 'wb+') as f:
                for chunk in i.chunks():
                    f.write(chunk)
        images_dict[f"{log_id}"] = images_name if flag else images_name
        with open("inspection/static/json/images_name.json", 'w') as f:
            json.dump(images_dict, f)
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


def delete_img(request, log_id: int, name_img: str):
    '''
    Удаление изображения в log_details
    '''
    log = models.Inspection_log.objects.get(id=log_id)
    with open("inspection/static/json/images_name.json", 'r') as f:
        images_dict = json.load(f)
    images_list = images_dict[f"{log_id}"]
    print(images_list)
    images_list.remove(f'{name_img}')
    print(images_list)
    with open("inspection/static/json/images_name.json", 'r') as f:
        new_dict = json.load(f)
        new_dict[f"{log_id}"] = images_list
        with open("inspection/static/json/images_name.json", 'w') as file:
            json.dump(new_dict, file)
    return redirect('inspection:log_details', log.id)


def substations_all(request):
    substations = models.Inspection_log.objects.filter(substation_name='somebody')
