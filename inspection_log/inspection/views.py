from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms
import datetime, os


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
    Форма здля записи в журнал
    '''
    if request.method == 'POST':
        form = forms.LogForms(request.POST, request.FILES)

        if form.is_valid():
            if not os.path.isdir(
                    f"inspection/static/downloadimages/{request.user}_{str(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M'))}"):
                new_path = os.mkdir(
                    f"inspection/static/downloadimages/{request.user}_{str(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M'))}")
            else:
                new_path = f"{request.user}_{datetime.datetime.today().strftime('%Y-%m-%d_%H-%M')}"
            for number, files in enumerate(request.FILES.getlist('myFile')):   # итерация по добавленным файлам и получение байт кода
                dest_file = open(f'inspection/static/downloadimages/{str(new_path)}/{number}.jpg', 'wb+')    # создание картинки
                dest_file.write(files.file.getvalue())
                dest_file.close()
            new_log = form.save(commit=False)
            new_log.user_name_id = request.user          # сохранение в журнале залогиниившегося юзера
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
    if not log:
        raise Exception('No such log')
    else:
        return render(request, 'inspection/log_details.html', {'log': log})


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
