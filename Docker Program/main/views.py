from django.shortcuts import render
import cv2 as cv
from . import final2
from . import utils
from . import forms, models
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist
# InMemoryUploadedFile.
# from django.urls import reverse
# Create your views here.


def home(request):

    return render(request, 'home.html', {
        'form':  forms.UploadForm()
    })


def process(request):
    # print(request.POST.get("img"))
    # print(request.FILES, ' files')
    # print(request.FILES.getlist('img'), ' files')
    filelist = request.FILES.getlist('img')
    # print(len(filelist), 'length')
    qrList = []
    tcList = []

    height = 1200
    width = 900
    for f in filelist:
        fs = FileSystemStorage()
        fs.save(f.name, f)
        img = cv.imread('./media/'+f.name)
        tc = final2.get_tc(img)
        qr_code = final2.get_qrcode(
            img[0:height//4, 0:width//2])
        qr_code_sonuc = str(qr_code).split("\n")
        bolum = qr_code_sonuc[0]
        ders = qr_code_sonuc[1]
        sinav_tipi = qr_code_sonuc[2]
        kagit = f.name
        print(tc)
        print(f.name)
        # Algılanan qr kod ve tc değerleri veritabanı eklenecektir
        exists = False
        try:
            n = models.Sinav.objects.get(tc=tc)
            exists = True
        except ObjectDoesNotExist:
            exists = False

        if not exists:

            models.Sinav.objects.create(
                tc=tc, bolum=bolum, ders=ders, sinav_tipi=sinav_tipi, kagit=kagit)
        # models.Sinav.save()

        tup = (tc, qr_code)
        tcList.append(tup)
        # qrList.append(final2.get_qrcode(img[0:height//4, 0:width//2]))
    # file = request.FILES['img']

    # models.Sinav.objects.all().delete()
    print("objects len", len(models.Sinav.objects.all()))

    tc = 2
    qr_code = 2

    return render(request, 'home.html', {
        'form':  forms.UploadForm(),
        'tc': tcList,
        'qr_code': qrList
    })


def list(request):
    print(type(models.Sinav.objects.all()))
    return render(request, 'home.html', {
        'sinavList':  models.Sinav.objects.all()
    })
