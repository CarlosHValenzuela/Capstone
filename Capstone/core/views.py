from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from core.utils.videoReconocer import   generate_frames
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import PersonaForm, AutoForm
from .models import Persona, Auto
from django.contrib.auth.models import User

@login_required
def main(request):
    autos = Auto.objects.all()
    residentes = Persona.objects.all()
    return render(request, 'main.html', {'residentes': residentes, 'autos': autos})

@login_required
def perfil(request):
    usuario = User.objects.all()
    return render(request, 'perfil.html', {'usuarios': usuario})

@login_required
def residentes(request):
    residentes = Persona.objects.all()
    return render(request, 'residentes.html', {'residentes': residentes})

@login_required
def crear_auto(request):
    if request.method == 'GET':
        return render(request, 'crearAuto.html', {
            'form': AutoForm
        })
    else:
        try:
            form = AutoForm(request.POST)
            new_auto = form.save(commit=False)
            new_auto.user = request.user
            new_auto.save()
            return redirect('reconocedor')
        except ValueError:
            return render(request, 'crearAuto.html', {
                'form': AutoForm,
                'error':'Porfavor ingresar datos validos'
            })

@login_required
def crear_residente(request):
    if request.method == 'GET':
        return render(request, 'crearResidente.html', {
            'form': PersonaForm
        })
    else:
        try:
            form = PersonaForm(request.POST)
            new_residente = form.save(commit=False)
            new_residente.user = request.user
            new_residente.save()
            return redirect('Residentes')
        except ValueError:
            return render(request, 'crearResidente.html', {
                'form': PersonaForm,
                'error':'Porfavor ingresar datos validos'
            })

@login_required
def edicion_auto(request, id):
    if request.method == 'GET':
        detalle = get_object_or_404(Auto, pk=id)
        form = AutoForm(instance=detalle)
        return render(request, 'editarAuto.html', {'detalle': detalle, 'form': form})
    else:
        try:
            detalle = get_object_or_404(Auto, pk=id)
            form = AutoForm(request.POST, instance=detalle)
            form.save()
            return redirect ('reconocedor')
        except:
            return render (request, 'editarAuto.html', {'detalle': detalle, 'form': form, 
                                                             'error': "Error actualizando datos"})

@login_required
def edicion_residente(request, id):
    if request.method == 'GET':
        detalle = get_object_or_404(Persona, pk=id)
        form = PersonaForm(instance=detalle)
        return render(request, 'editarResidente.html', {'detalle': detalle, 'form': form})
    else:
        try:
            detalle = get_object_or_404(Persona, pk=id)
            form = PersonaForm(request.POST, instance=detalle)
            form.save()
            return redirect ('Residentes')
        except:
            return render (request, 'editarResidente.html', {'detalle': detalle, 'form': form, 
                                                             'error': "Error actualizando datos"})

@login_required
def eliminar_auto(request, id):
    auto = Auto.objects.get(id=id)
    auto.delete()
    
    return redirect('reconocedor')

@login_required
def eliminar_residente(request, id):
    residente = Persona.objects.get(id=id)
    residente.delete()
    
    return redirect('Residentes')

@login_required
def reconocedor(request):
    autos = Auto.objects.all()
    return render(request, 'reconocedor.html', {'autos': autos})

@login_required
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def inicioSesion(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'login.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o password esta incorrecto'
        })
        else:
            login(request, user)
            return redirect('Pagina Principal')
        
def cerrarSesion(request):
    logout(request)
    return redirect('/')