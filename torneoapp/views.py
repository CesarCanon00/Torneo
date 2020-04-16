from django.shortcuts import render, get_object_or_404 
from django.views import generic
from django.urls import path, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
from .forms import CreateUserForm
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib import messages
from torneoapp.models import Partido, Equipo, Jugador, JugadorxEquipo, Arbitro, Estadio, Patrocinador, Ciudad, Empresa, PersonaNatural, JugadorxPartido, Evento
from torneoapp.forms import CreatePartidoForm, CreateEquipoForm, CreateJugadorForm, CreateArbitroForm, CreateEstadioForm, CreatePatrocinadorForm, CreateCiudadForm, CreateEmpresaForm, CreatePersonaNaturalForm, CreateTransferenciaForm, CreateJugadorxPartidoForm, CreateEventoForm

# Create your views here.
INFO = {
        'partido':{
            'form':CreatePartidoForm,
            'name':'Partido',
            'model':Partido,
            'pk':'fecha_hora'
        },
        'equipo':{
            'form':CreateEquipoForm,
            'name':'Equipo',
            'model':Equipo,
            'pk':'nombre'
        },
        'jugador':{
            'form':CreateJugadorForm,
            'name':'Jugador',
            'model':Jugador,
            'pk':'codigo'
        },
        'arbitro':{
            'form':CreateArbitroForm,
            'name':'Árbitro',
            'model':Arbitro,
            'pk':'carne'
        },
        'estadio':{
            'form':CreateEstadioForm,
            'name':'Estadio',
            'model':Estadio,
            'pk':'codigo'
        },
        'patrocinador':{
            'form':CreatePatrocinadorForm,
            'name':'Patrocinador',
            'model':Patrocinador,
            'pk':'id'
        },
        'ciudad':{
            'form':CreateCiudadForm,
            'name':'Ciudad',
            'names':'Ciudades',
            'model':Ciudad,
            'lqset':Ciudad.objects.all().order_by('nombre'),
            'pk':'codigo'
        },
        'empresa':{
            'form':CreateEmpresaForm,
            'name':'Empresa',
            'names':'Empresas',
            'model':Empresa,
            'lqset':Empresa.objects.all().order_by('nombre'),
            'pk':'nombre'
        },
        'personanatural':{
            'form':CreatePersonaNaturalForm,
            'name':'Persona Natural',
            'names':'Personas Naturales',
            'model':PersonaNatural,
            'lqset':PersonaNatural.objects.all().order_by('nombre'),
            'pk':'cedula'
        },
        'transferencia':{
            'form':CreateTransferenciaForm,
            'name':'Transferencia',
            'names':'Transferencias',
            'model':JugadorxEquipo,
            'lqset':JugadorxEquipo.objects.all().order_by('equipo'),
            'pk':'codigo'
        },
         'transferencia2':{
            'form':CreateTransferenciaForm,
            'name':'Transferencia',
            'names':'Transferencias',
            'model':JugadorxEquipo,
            'lqset':JugadorxEquipo.objects.all().order_by('equipo'),
            'pk':'codigo'
        },
        'jugadorxpartido':{
        'form':CreateJugadorxPartidoForm,
        'name':'Jugador del partido',
        'names':'Jugadores del Partido',
        'model':JugadorxPartido,
        'pk':'id'
        },
        'evento':{
        'form':CreateEventoForm,
        'name':'Evento',
        'names':'Eventos',
        'model':Evento,
        'pk':'tiempo'
        },
    }

def registroUsuario(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:login'))

    context = {'form':form}
    return render(request,'main/auth/registro.html',context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))
    else:
        form = AuthenticationForm()
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    do_login(request, user)
                    return HttpResponseRedirect(reverse('main:home'))

        context = {'form':form}
        return render(request, "main/auth/login.html",context)

def Home(request):
    if request.user.is_authenticated:
        partidos = Partido.objects.all().order_by('fecha_hora')
        equipos = Equipo.objects.all()
        jugadores = Jugador.objects.all().order_by('codigo')
        arbitros = Arbitro.objects.all().order_by('carne')
        estadios = Estadio.objects.all().order_by('codigo')
        patrocinadores = Patrocinador.objects.all().order_by('id')
        context = {'partidos':partidos,
        'equipos':equipos,
        'jugadores':jugadores,
        'arbitros':arbitros,
        'estadios':estadios,
        'patrocinadores':patrocinadores,
        }
        return render(request, 'main/home.html',context)
    return HttpResponseRedirect(reverse('auth:login'))

def logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('auth:login'))

def add(request,model):
    model_name = INFO[model]['name']
    form = INFO[model]['form']
    if request.method == 'POST':
        form = INFO[model]['form'](request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:home'))

    context = {'form':form,'model_name':model_name}
    
    return render(request, "main/add.html",context)

def addid(request,model,id):
    model_name = INFO[model]['name']+" "+id
    form = INFO[model]['form']
    print(INFO[model]['name'])

    if INFO[model]['name'] in ('Jugador del partido','Evento'):
        if request.method == 'POST':
            form = INFO[model]['form'](request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('main:partido',kwargs={'id':id}))    
    else:
        if request.method == 'POST':
                form = INFO[model]['form'](request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('main:home'))

    context = {'form':form,'model_name':model_name}
    
    return render(request, "main/add.html",context)

def listar(request,model):
    context = {}
    model_name = INFO[model]['names']
    QSETS = {
        'ciudad':Ciudad.objects.all().order_by('nombre'),
        'empresa':Empresa.objects.all().order_by('nombre'),
        'personanatural':PersonaNatural.objects.all().order_by('nombre'),
        'transferencia':JugadorxEquipo.objects.all().order_by('equipo')
    }
    queryset = QSETS[model]
    context = {'queryset':queryset,'model_name':model_name,'model':model}
    
    return render(request, "main/listar.html",context)

def listarid(request,model,id):
    context = {}
    queryset = ""

    if model in 'jugadorxpartido':
        queryset = JugadorxPartido.objects.filter(partido=id)
        model_name = INFO[model]['names']
        context = {'queryset':queryset,'model_name':model_name,'model':model,'idmol':id}
    elif model in  'transferencia2':
        queryset = JugadorxEquipo.objects.filter(jugador=id)
        model_name = INFO['transferencia']['names']
        name = Jugador.objects.get(pk=id).nombre
        context = {'queryset':queryset,'model_name':model_name,'model':'transferencia2','idmol':id,'name':name}

    return render(request, "main/listar.html",context)

def modify(request,model,id):
    model_name = INFO[model]['name']
    obj= get_object_or_404(INFO[model]['model'], pk=id)
    print(obj)
    form = INFO[model]['form'](request.POST or None, instance= obj)

    if request.method == 'POST':
        if form.is_valid():
            if INFO[model]['name'] in 'partido':
                INFO[model]['model'].objects.get(pk=id).delete()
                
            obj=form.save(commit=False)
            obj.save()
            messages.success(request, "successfully updated")
            context = {'form':form,'model_name':model_name,'id':id}
            return HttpResponseRedirect(reverse('main:home'))
        else:
            context= {'form': form,
            'error': 'The form was not updated successfully. Please enter in a title and content'}
            return render(request, "main/modify.html",context)

    context = {'form':form,'model_name':model_name,'id':id}
    return render(request, "main/modify.html",context)

def delete(request,model,id):
    model_name = INFO[model]['name']

    if request.method == 'POST':
        print("if")
        INFO[model]['model'].objects.get(pk=id).delete()
        return HttpResponseRedirect(reverse('main:home'))
    else:
        print("else")
        context = {'model_name':model_name,'id':id}
        return render(request, "main/delete.html",context)

    context = {'model_name':model_name,'id':id}
    return render(request, "main/delete.html",context)

def deleteid(request,model,id,idmol):
    model_name = INFO[model]['name']

    if request.method == 'POST':
        print("if")
        INFO[model]['model'].objects.get(pk=id).delete()
        if model == 'jugadorxpartido':
            return HttpResponseRedirect(reverse('main:partido',kwargs={'id':idmol}))
        else:
            return HttpResponseRedirect(reverse('main:home'))
    else:
        print("else")
        context = {'model_name':model_name,'id':id}
        return render(request, "main/delete.html",context)

    context = {'model_name':model_name,'id':id}
    return render(request, "main/delete.html",context)

def partido(request,id):

    eq_local = Partido.objects.get(pk=id).eq_local
    eq_visit = Partido.objects.get(pk=id).eq_visit
    fecha = Partido.objects.get(pk=id).fecha_hora
    fechac = Partido.objects.get(pk=id).getDate()
    arbitro = Partido.objects.get(pk=id).arbitro
    pts_local = Partido.objects.get(pk=id).pts_local
    pts_visit = Partido.objects.get(pk=id).pts_visit
    ganador = Partido.objects.get(pk=id).getGanador()
    j_local = JugadorxEquipo.objects.filter(equipo=eq_local).values('jugador','fechaInicio','fechaFin')
    j_visit = JugadorxEquipo.objects.filter(equipo=eq_visit).values('jugador','fechaInicio','fechaFin')
    jugadores_l = []
    jugadores_v = []

    for jugador in j_local:
        actual = JugadorxPartido.objects.filter(jugador=jugador['jugador'],partido=id).values('min_ingreso','min_salida')
        l_actual = list(actual)
        print(actual.query)
        print(l_actual)
        fechaInicio = jugador['fechaInicio']
        fechaFin = jugador['fechaFin']

        if actual.count() > 0 and fechaInicio<fechac and fechaFin>fechac:
            minEntra = l_actual[0]['min_ingreso']
            minSale = l_actual[0]['min_salida']
            jname = Jugador.objects.get(pk=jugador['jugador']).nombre
            jugadores_l.append("{}, {}-{}".format(jname,minEntra,minSale))

    for jugador in j_visit:
        actual = JugadorxPartido.objects.filter(jugador=jugador['jugador'],partido=id).values('min_ingreso','min_salida')
        l_actual = list(actual)
        fechaInicio = jugador['fechaInicio']
        fechaFin = jugador['fechaFin']

        if actual.count() > 0 and fechaInicio<fechac and fechaFin>fechac:
            minEntra = l_actual[0]['min_ingreso']
            minSale = l_actual[0]['min_salida']
            jname = Jugador.objects.get(pk=jugador['jugador']).nombre
            jugadores_v.append("{}, {}-{}".format(jname,minEntra,minSale))

    eventos = Evento.objects.filter(partido=id)

    context = {'eq_local':eq_local,'eq_visit':eq_visit,'id':id,
               'fecha':fecha,'arbitro':arbitro,'pts_local':pts_local,'pts_visit':pts_visit,
               'ganador':ganador,'j_local':jugadores_l,'j_visit':jugadores_v,'eventos':eventos}
               
    return render(request, "main/partido.html",context)

