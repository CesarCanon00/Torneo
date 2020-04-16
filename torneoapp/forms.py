from django.forms import ModelForm
from django.forms import TextInput, DateInput
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from torneoapp.models import Partido, Equipo, Jugador, Arbitro, Estadio, Patrocinador, Ciudad, Empresa, PersonaNatural, JugadorxEquipo, JugadorxPartido, Evento

class CreateUserForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username','password1','password2']

class CreatePartidoForm(ModelForm):
    class Meta:
        model = Partido
        fields = ['fecha_hora','eq_local','eq_visit','pts_local','pts_visit','estadio','arbitro']
        labels = {'fecha_hora': 'Fecha y Hora (YYYY-MM-DD HH:MM)',
                'eq_local':'Equipo Local',
                'eq_visit':'Equipo Visitante',
                'pts_local':'Goles Equipo Local',
                'pts_visit':'Goles Equipo Visitante',
                'estadio':'Estadio',
                'arbitro':'Árbitro'
                }

class CreateEquipoForm(ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre','a_creacion','ciudad','patrocinador']
        labels = {'nombre': 'Nombre del equipo',
                'a_creacion':'Año de Creación',
                'ciudad':'Ciudad',
                'patrocinador':'Patrocinador'
                }

class CreateJugadorForm(ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre','fecha_nacimiento']
        labels = {'nombre': 'Nombre del jugador',
                'fecha_nacimiento':'Fecha de Nacimiento'
                }

class CreateArbitroForm(ModelForm):
    class Meta:
        model = Arbitro
        fields = ['nombre','tutor']
        labels = {'nombre': 'Nombre del Árbitro',
                'tutor':'Tutor'
                }

    def __init__(self, *args, **kwargs):
        super(CreateArbitroForm, self).__init__(*args, **kwargs)
        self.fields['tutor'].required = False

class CreateEstadioForm(ModelForm):
    class Meta:
        model = Estadio
        fields = ['nombre','capacidad','aconstruccion','ciudad']
        labels = {'nombre': 'Nombre del Estadio',
                'capacidad':'Capacidad',
                'aconstruccion':'Año de Construcción',
                'ciudad':'Ciudad'
                }

class CreatePatrocinadorForm(ModelForm):

    class Meta:
        model = Patrocinador
        fields = ['tipo_patrocinador','empresa','personanatural','equipo']
        labels = {'tipo_patrocinador':'Tipo de Patrocinador',
                'empresa': 'Empresa',
                'personanatural':'Persona Natural',
                'equipo':'Equipo'
                }

    def __init__(self, *args, **kwargs):
        super(CreatePatrocinadorForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].required = False
        self.fields['personanatural'].required = False
        self.fields['equipo'].required = False

class CreateCiudadForm(ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre','poblacion']
        labels = {'nombre':'Nombre',
                'poblacion': 'Población'
                }

class CreateCiudadForm(ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre','poblacion']
        labels = {'nombre':'Nombre',
                'poblacion': 'Población'
                }

class CreateEmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre','representante','email','ubicacion']
        labels = {'nombre':'Nombre',
                'representante': 'Representante',
                'email': 'Correo Electrónico',
                'ubicacion': 'Ubicación'
                }

class CreatePersonaNaturalForm(ModelForm):
    class Meta:
        model = PersonaNatural
        fields = ['nombre','telefono']
        labels = {'nombre':'Nombre',
                'telefono': 'Teléfono'
                }

class CreateTransferenciaForm(ModelForm):
    class Meta:
        model = JugadorxEquipo
        fields = ['jugador','equipo','fechaInicio','fechaFin']
        labels = {'fechaInicio':'Fecha de Ingreso',
                'fechaFin': 'Fecha de Salida',
                'equipo': 'Equipo',
                'jugador': 'Jugador'
                }


class CreateJugadorxPartidoForm(ModelForm):
    class Meta:
        model = JugadorxPartido
        fields = ['jugador','partido','min_ingreso','min_salida']
        labels = {'jugador':'Jugador',
                'partido': 'Partido',
                'min_ingreso': 'Minuto de Ingreso',
                'min_salida': 'Minuto de Salida'
                }

class CreateEventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['tiempo','tipo_evento','jugadorxpartido','partido','descripcion']
        labels = {'tiempo':'Minuto',
                'tipo_evento': 'Tipo de Evento',
                'jugadorxpartido': 'Ejecutor',
                'partido': 'Partido',
                'descripcion':'Descripción'
                }
    def __init__(self, *args, **kwargs):
        super(CreateEventoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False