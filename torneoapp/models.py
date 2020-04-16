from django.db import models
import locale

# Create your models here.

locale.setlocale(locale.LC_TIME, '')

class Ciudad(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200,null=False,unique=True)
    poblacion = models.IntegerField(null=False)

    def save(self):
        super(Ciudad,self).save()
    def __str__(self):
        return self.nombre

class Arbitro(models.Model):
    carne = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200,null=False,unique=True)
    tutor = models.ForeignKey("Arbitro",on_delete=models.CASCADE,null=True)

    def save(self):
        super(Arbitro,self).save()
    def __str__(self):
        return self.nombre

class Estadio(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500,null=False,unique=True)
    capacidad = models.IntegerField(null=False)
    aconstruccion = models.IntegerField(null=False)
    ciudad = models.ForeignKey(Ciudad,on_delete=models.CASCADE,null=True)

    def save(self):
        super(Estadio,self).save()
    def __str__(self):
        return self.nombre

class Empresa(models.Model):
    nombre = models.CharField(primary_key=True,max_length=500,null=False)
    representante = models.CharField(max_length=500,null=False)
    email = models.EmailField(max_length=500,null=False,unique=True)
    ubicacion = models.ForeignKey(
        Ciudad,
        on_delete=models.CASCADE,
        null=True
    )

    def save(self):
        super(Empresa,self).save()
    def __str__(self):
        return self.nombre

class PersonaNatural(models.Model):
    cedula = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500,null=False,unique=True)
    telefono = models.CharField(max_length=10,null=False,unique=True)

    def save(self):
        super(PersonaNatural,self).save()
    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500,null=False,unique=True)
    fecha_nacimiento = models.DateField(null=False)

    def save(self):
        super(Jugador,self).save()
    def __str__(self):
        return self.nombre

class Patrocinador(models.Model):
    TIPOS = (
            ('Empresa', 'Empresa'),
            ('Persona Natural', 'Persona Natural'),
            ('Equipo', 'Equipo'))
    tipo_patrocinador = models.CharField(max_length=20,choices=TIPOS)
    empresa =  models.OneToOneField(Empresa,on_delete=models.CASCADE,null=True,unique=True)  
    personanatural =  models.OneToOneField(PersonaNatural,on_delete=models.CASCADE,null=True,unique=True)
    equipo =  models.OneToOneField("Equipo",related_name='equipo_patrocinador',on_delete=models.CASCADE,null=True,unique=True)

    def nomPtr(self):
        if self.tipo_patrocinador == 'Empresa':
            return "{}".format(self.empresa)
        elif self.tipo_patrocinador == 'Persona Natural':
            return "{}".format(self.personanatural)
        else:
            return "{}".format(self.equipo) 

    def save(self):
        super(Patrocinador,self).save()
    def __str__(self):
        return self.nomPtr()

class Equipo(models.Model):
    nombre = models.CharField(max_length=300,primary_key=True)
    a_creacion = models.IntegerField(null=False)
    ciudad = models.ForeignKey(Ciudad,null=True,on_delete=models.CASCADE)
    patrocinador = models.ForeignKey(Patrocinador,related_name='epatrocinador',on_delete=models.CASCADE,null=True)

    def save(self):
        super(Equipo,self).save()
    def __str__(self):
        return self.nombre

class Partido(models.Model):
    fecha_hora = models.DateTimeField(primary_key=True,unique=True)
    pts_local = models.IntegerField(null=False)
    pts_visit = models.IntegerField(null=False)
    eq_local = models.ForeignKey(Equipo,related_name='eq_local',on_delete=models.CASCADE)
    eq_visit = models.ForeignKey(Equipo,related_name='eq_visit',on_delete=models.CASCADE)
    estadio = models.ForeignKey(Estadio,on_delete=models.CASCADE)
    arbitro = models.ForeignKey(Arbitro,on_delete=models.CASCADE)
    
    def getGanador(self):
        if self.pts_local > self.pts_visit:
            return self.eq_local
        elif  self.pts_local < self.pts_visit:
            return self.eq_visit
        else:
            return "Empate"

    ganador = getGanador

    def getDate(self):
        return self.fecha_hora.date()

    def getMarcador(self):
        return "{} - {}".format(self.pts_local,self.pts_visit)

    def save(self):
        super(Partido,self).save()
    def __str__(self):
        return "{}".format(self.fecha_hora)

class JugadorxPartido(models.Model):
    min_ingreso = models.IntegerField(null=False)
    min_salida = models.IntegerField(null=False)
    jugador = models.ForeignKey(Jugador,on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido,on_delete=models.CASCADE)

    def save(self):
        super(JugadorxPartido,self).save()
    def __str__(self):
        return "{}, {}".format(self.jugador,self.partido)

class Evento(models.Model):
    codigo = models.AutoField(primary_key=True)
    tiempo = models.IntegerField(null=False)
    EVENTO_CHOICES = (
        ("Gol","Gol"),
        ("Falta","Falta"),
        ("Tiro con barrera","Tiro con barrera"),
        ("Tiro de esquina","Tiro de esquina"),
        ("Penal","Penal"),
        ("Saque de arco","Saque de arco"),
        ("Asistencia","Asistencia")
        )
    tipo_evento = models.CharField(max_length=30,choices=EVENTO_CHOICES)
    ejecutor = models.ForeignKey(Jugador,on_delete=models.CASCADE,null=True)
    descripcion = models.CharField(max_length=500,null=True)
    partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
    jugadorxpartido = models.ForeignKey(JugadorxPartido,on_delete=models.CASCADE)

    def save(self):
        super(Evento,self).save()
    def __str__(self):
        return "{}".format(self.tiempo)

class JugadorxEquipo(models.Model):
    codigo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField(null=True)
    fechaFin = models.DateField(null=True)
    equipo = models.ForeignKey(Equipo,on_delete=models.CASCADE,null=True)
    jugador = models.ForeignKey(Jugador,on_delete=models.CASCADE)

    def save(self):
        super(JugadorxEquipo,self).save()
    def __str__(self):
        return "{}, {}".format(self.jugador,self.equipo)
