from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from . import models, forms
import datetime, os, json, telebot
from django.contrib.auth.models import User
import yandex_map, all_path
from PIL import Image, ImageOps, ImageFile, UnidentifiedImageError
from django.db.models import Count


bot = telebot.TeleBot(os.getenv('api_token'))
chatId = os.getenv('chatId_my')
ImageFile.LOAD_TRUNCATED_IMAGES = True

def send_message_tg(type_message, name, job_type, substation):
    '''
    Отправка уведомления в телеграмм
    '''
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    message = f'{name} {type_message}.\n{job_type}\n{substation}\n{time_now.strftime("%d.%m.%Y, %H:%M:%S")}'
    bot.send_message(chatId, text=message)

def change_imagesize(name, img_path):
    '''
    уменьшение размера картинок
    '''
    try:
        new_img = Image.open(f'{img_path}/{name}')
        image = ImageOps.exif_transpose(new_img)
        image.save(f'{img_path}/{name}', format='JPEG', quality=50)
        image.close()
    except UnidentifiedImageError:
        pass



def home(request):
    job_count = {}
    all_job = models.Inspection_log.objects.values('job_type').distinct()
    for job in all_job:
        job_count[job['job_type']] = models.Inspection_log.objects.filter(job_type=job['job_type']).count()

    content = {"job_count": job_count}
    return render(request, 'index.html', content)


def inspection_log(request):
    '''
    Журнал осмотра и фильтром
    '''
    if not request.user.has_perm('inspection.view_inspection_log'):
        log = []
    else:
        log = models.Inspection_log.objects.all()
    if request.method == 'POST':
        form = forms.InspectionLogForm(request.POST)                            # форма фильтра
        if form.is_valid():
            clean_data = form.cleaned_data
            substation_name = clean_data['substation_name']
            date_time_start = clean_data['date_time_start']
            date_time_last = clean_data['date_time_last']
            developer = clean_data['developer']
            sort_list = clean_data['sort_list']
            if date_time_start == None:                                         # если дата не заполнена, автоматически вносится
                date_time_start = datetime.date(2010, 1, 1)
            if date_time_last == None:
                date_time_last = datetime.date(2050, 1, 1)
            if developer != '0':
                find_user_id = User.objects.filter(username=developer)[0].id    # получение id пользователя по логину
                find_user_id_last = find_user_id
            else:
                find_user_id = 1
                find_user_id_last = User.objects.all().last().id
            if len(substation_name) != 0:                                       # если ведено название подстанции           
                log = models.Inspection_log.objects.filter(substation_name=substation_name, date_record__lte=date_time_last, 
                    date_record__gte=date_time_start, user_name_id__gte=find_user_id, user_name_id__lte=find_user_id_last)
                bot.send_message(chatId, text=f'начало - {date_time_start}, конец - {date_time_last}, user1 - {find_user_id}, user2 - {find_user_id_last}')
            else:
                log = models.Inspection_log.objects.filter(date_record__lte=date_time_last, 
                    date_record__gte=date_time_start, user_name_id__gte=find_user_id, user_name_id__lte=find_user_id_last)
            if sort_list == 'date':
                log = log.order_by('-date_record')
            elif sort_list == 'occupancy':
                log = log[::-1]
            elif sort_list == 'warning':
                log = log.order_by('-note')
            content = {'logs': log, 'form': form}
            return render(request, 'inspection/inspection_log.html', content if request.user.has_perm('inspection.view_inspection_log') else {})
        else:
            return redirect('inspection:inspection_log')
    else:
        form = forms.InspectionLogForm()
        return render(request, 'inspection/inspection_log.html', {'logs': log[::-1], 'form': form})


def log_form(request):
    '''
    Форма для записи в журнал
    '''
    if not os.path.isdir(all_path.downloadimages):
        os.mkdir(all_path.downloadimages)

    if request.method == 'POST':
        form = forms.LogForms(request.POST, request.FILES)
        images_name = []                                                        # список для названия фото
        if form.is_valid() :
            new_log = form.save(commit=False)
            new_log.user_name_id = request.user
            new_log.responsible_user_id = request.user
            new_log.save()
            send_message_tg('сделал запись', request.user.get_full_name(), new_log.job_type, new_log.substation_name)
            id_log = new_log.id                                                 # id новой записи
            img_path = all_path.downloadimages + f'/{id_log}'
            if not os.path.isdir(img_path):                                     # если папки нету, создаёт новую
                os.mkdir(img_path)                                              # с именем id записи
            for i in request.FILES.getlist('myFile'):                           # итерация по добавленным файлам через input и получение байт кода
                images_name.append(str(i.name))                                 # имена фото
                with open(f"{img_path}/{i.name}", 'wb+') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
                change_imagesize(i.name, img_path)
            image_dict = {id_log: images_name}                                      
            if not os.path.exists(all_path.images_name):
                with open(all_path.images_name, 'w') as f:   # в json хранятся значения id записи
                    json.dump(image_dict, f)                                      # и списка имени файлов
            else:
                with open(all_path.images_name, 'r') as f:
                    img_dict = json.load(f)
                    new_dict = {**image_dict, **img_dict}                          # объединение словарей
                    with open(all_path.images_name, 'w') as f:
                        json.dump(new_dict, f)

            return redirect('inspection:inspection_log')
        else:
            return render(request, 'inspection/log_form.html', {'form': form,})
    else:
        form = forms.LogForms()
        return render(request, 'inspection/log_form.html', {'form': form, })


def log_details(request, log_id: int):  
    log = models.Inspection_log.objects.get(id=log_id)
    try:
        location_of_substation = yandex_map.location[f'{log.substation_name}']
    except KeyError:
        location_of_substation = 0
    time_ = datetime.datetime.today()
    with open(all_path.images_name, 'r') as f:
        image_dict = json.load(f)
    try:
        image_list = image_dict[f'{log.id}']
    except KeyError:
        image_list = []
    if not log:
        raise Exception('No such log')
    else:
        content = {'log': log, 'log_id': log_id, 'image_list': image_list, 'time1': time_.time(),
                   'location_of_substation': location_of_substation}
        return render(request, 'inspection/log_details.html', content if request.user.has_perm('inspection.view_inspection_log') else {})


def update_log(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    img_path = all_path.downloadimages + f'/{log_id}'
    form = forms.LogForms(request.POST or None, request.FILES or None, instance=log)
    if form.is_valid():
        with open(all_path.images_name, 'r') as f:
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
                change_imagesize(str(i.name), img_path)
        images_dict[f"{log_id}"] = images_name if flag else images_name
        with open(all_path.images_name, 'w') as f:
            json.dump(images_dict, f)
        new_log = form.save(commit=False)
        new_log.user_name_id = request.user
        send_message_tg('изменил запись', request.user.get_full_name(), new_log.job_type, new_log.substation_name)
        new_log.save()
        return redirect('inspection:log_details', log.id)
    return render(request, 'inspection/log_form.html', {'form': form})


def delete_log(request, log_id: int):
    '''
    Удаление записи
    '''
    log = models.Inspection_log.objects.get(id=log_id)
    log.delete()
    send_message_tg('удалил запись', request.user.get_full_name(), log.job_type, log.substation_name)
    return redirect('inspection:inspection_log')


def delete_img(request, log_id: int, name_img: str):
    '''
    Удаление изображения в log_details
    '''
    log = models.Inspection_log.objects.get(id=log_id)
    with open(all_path.images_name, 'r') as f:
        images_dict = json.load(f)
    images_list = images_dict[f"{log_id}"]
    images_list.remove(f'{name_img}')
    with open(all_path.images_name, 'r') as f:
        new_dict = json.load(f)
        new_dict[f"{log_id}"] = images_list
        with open(all_path.images_name, 'w') as file:
            json.dump(new_dict, file)
    return redirect('inspection:log_details', log.id)
