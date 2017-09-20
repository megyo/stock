import json
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from app.forms import TermekKategoriaForm
from app.models import TermekKategoria
from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers.json import DjangoJSONEncoder


@staff_member_required(login_url='/login/')
def termekkategoria_list(request):
    termekkategoria_list = TermekKategoria.objects.all().values()
    termekkategoria = json.dumps(list(termekkategoria_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/termekkategoria_list.html',
        {
            'title': 'Termékkategóriák listája',
            'termekkategoria': termekkategoria,
        }
    )



@staff_member_required(login_url='/login/')
def termekkategoria_new(request):
    if request.method == "POST":
        form = TermekKategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('termekkategoria_list')
    else:
        form = TermekKategoriaForm()

    return render(
        request,
        'app/termekkategoria_new.html',
        {
            'title': 'Új termékkategoria létrehozása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termekkategoria_edit(request, pk):
    termekkategoria = get_object_or_404(TermekKategoria, pk=pk)
    if request.method == "POST":
        form = TermekKategoriaForm(request.POST, instance=termekkategoria)
        if form.is_valid():
            form.save()
            return redirect('termekkategoria_list')
    else:
        form = TermekKategoriaForm(instance=termekkategoria)

    return render(
        request,
        'app/termekkategoria_edit.html',
        {
            'title': 'Termékkategória módosítása',
            'form': form
        }
    )