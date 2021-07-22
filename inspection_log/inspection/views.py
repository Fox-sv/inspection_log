from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms


def home(request):
    return render(request, 'index.html', {})


def inspection_log(request):
    '''
    Журнал осмотра
    '''
    log = models.Inspection_log.objects.all()
    return render(request, 'inspection_log.html', {'logs': log})


def log_form(request):
    '''
    Форма здля записи в журнал
    '''
    if request.method == 'POST':
        form = forms.LogForms(request.POST, request.FILES)
        img_obj = form.instance
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.user_name_id = request.user          # сохранение в журнале залогиниившегося юзера
            new_log.responsible_user_id =request.user
            new_log.save()
            img_obj = form.instance
            return redirect('inspection:start_page')
        else:
            return render(request, 'log_form.html', {'form': form, 'img_obj': img_obj})
    else:
        form = forms.LogForms()
        return render(request, 'log_form.html', {'form': form})


def log_details(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    if not log:
        raise Exception('No such log')
    else:
        return render(request, 'log_details.html', {'log': log})


def update_log(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    form = forms.LogForms(request.POST or None, instance=log)
    if form.is_valid():
        form.save()
        return redirect('inspection:log_details', log.id)
    return render(request, 'log_form.html', {'form': form})


def delete_log(request, log_id: int):
    log = models.Inspection_log.objects.get(id=log_id)
    log.delete()
    logs = models.Inspection_log.objects.all()
    #return render(request, 'inspection_log.html', {'logs': logs, })
    return redirect('inspection:inspection_log')