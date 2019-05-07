from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
#Agregamos modulos personales
from .models import Faq, Conferencias
from inscripciones.models import Inscriptos
from .forms import SignUpForm

def home(request):
    casistentes = Inscriptos.objects.filter(activo=True, categoria=1).count()
    cexpositores = Inscriptos.objects.filter(autorizado=True, categoria=2).count()
    cconferencias = Conferencias.objects.filter(autorizada=True).count()
    texto_central = Faq.objects.filter().first()
    return render(request, 'home.html', {'casistentes': casistentes, 'cexpositores': cexpositores, 'cconferencias': cconferencias,
                                         'texto_central': texto_central, })

def contacto(request):
    return render(request, 'contacto.html', { })

def faq(request):
    faqs = Faq.objects.all().order_by('orden')
    return render(request, 'faq.html', {'faqs' : faqs })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/encuestas/1')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def encontrate(request):
    return render(request, 'encontrate.html', { })