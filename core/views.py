from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.views import View
from .forms import FormAutos
from .models import Autos,Detalle
from django.core.files.storage import FileSystemStorage# importar la ubicacion del almacenamiento del archivo.
# Create your views here.
def base (request):
    return render(request,"core/home.html")
#solucionada la carga multiple (no me gusta este diseño pero es el que funciona)
def multicarga(request):
    marca = request.POST.get("marca")
    modelo = request.POST.get("modelo")
    motor = request.POST.get("motor")
    color = request.POST.get("color")
    año = request.POST.get("año")
    precio = request.POST.get("precio")
    kilometros = request.POST.get("kilometros")
    usado = request.POST.get("usado")
    imagenes = request.FILES.get("imagenes")
    imgsdetalle = request.FILES.getlist("imgsdetalle[]")
    fs=FileSystemStorage()
    file_path = fs.save(imagenes.name,imagenes)
    auto = Autos(marca=marca,modelo=modelo,motor=motor,color=color,año=año,precio=precio,kilometros=kilometros,usado=usado,imagenes=file_path)
    auto.save()
    for img in imgsdetalle:
        fs=FileSystemStorage()
        file_path = fs.save(img.name,img)
        detalleAuto = Detalle(auto=auto,imgsdetalle=file_path)
        detalleAuto.save()
    return HttpResponse("archivos cargados")

def home(request):
    autos = Autos.objects.all()
    return render (request, "core/index.html",{'autos':autos})

def detalle(request,pk):
    detalle = Detalle.objects.filter(auto__id=pk)
    return render (request,"core/detalle.html",{'detalle':detalle})

def principal(request):
    autos = Autos.objects.all()
    return render (request,'core/base.html',{'autos':autos})



def usados(request):
    usados=Autos.objects.all()
    return render (request,'core/usados.html',{'usados':usados})