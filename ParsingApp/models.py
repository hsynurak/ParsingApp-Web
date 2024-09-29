from django.db import models

# Create your models here.
class Cs0000(models.Model):
     dosyaBaslik = models.CharField(max_length=6)
     versiyonNumarasi = models.CharField(max_length=2)
     uyeKodu = models.CharField(max_length=5)
     portfoyKodu = models.CharField(max_length=3)
     rezerveAlan = models.CharField(max_length=62)
     uyeAdi = models.CharField(max_length=30)
     olusturmaTarihi = models.CharField(max_length=8)
     bildirimTarihi = models.CharField(max_length=8)
     rezerveAlan2 = models.CharField(max_length=376)
     
class RawData(models.Model):
     data = models.CharField(max_length=1000)