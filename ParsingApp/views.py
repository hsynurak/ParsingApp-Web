from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from tablib import Dataset
from .models import RawData, Cs0000
from .forms import RawDataForm
import pandas as pd
from django.http import JsonResponse
from django.db import models
from django.apps import apps
from django.core.management import call_command
from django.db import connection
from openpyxl import Workbook
from io import BytesIO


def index(request):
    success = False
    error = False
    if request.method == 'POST':
        try:
            # Veritabanındaki tüm verileri sil
            RawData.objects.all().delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='ParsingApp_rawdata'")
            # Yeni verileri ekleme işlemi
            dataset = Dataset()
            new_data = request.FILES['dataFile']
            imported_data = dataset.load(new_data.read(), format='xlsx')
            for data in imported_data:
                value = RawData(data=data[0])
                value.save()
            success = True  # İşlem başarılı olursa success True olur
        except Exception as e:
            error = True  # Bir hata meydana gelirse error True olur
    delete = request.GET.get('delete') == 'True'
    return render(request, 'index.html', {'success': success, 'error': error, 'delete': delete})

def resetDataBase(request):
    if request.method == 'POST':
        RawData.objects.all().delete()
    return redirect('/?delete=True')

def create_model(table_name, fields):
    attrs = {'__module__': 'ParsingApp.models', }
    for field in fields:
        attrs[field['name']] = models.CharField(max_length=255) 
    model = type(table_name, (models.Model,), attrs)
    if not apps.is_installed('ParsingApp'):
        apps.register_model('ParsingApp', model)
    try:
        call_command('makemigrations', 'ParsingApp')
        call_command('migrate', 'ParsingApp')
    except Exception as e:
        print(f"Migration sırasında hata: {e}")
    return model

def extract_fields_from_excel(df):
    fields = []
    for _, row in df.iterrows():
        fields.append({
            'name': row.iloc[4],  # 5. sütun: Alan adı
            'start_index': row.iloc[5],  # 6. sütun: Başlangıç indeksi
            'length': row.iloc[6]  # 7. sütun: Uzunluk
        })
    return fields

table_names = []
dynamic_vars = {}
def createModel(request):
    if request.method == 'POST':
        model_data = request.FILES['modelFile']
        df = pd.read_excel(model_data)
        table_name = ''.join(df.iloc[0, 0:4])
        dynamic_vars[f"{table_name}_length_list"] = []
    for index, row in df.iterrows():
        start_index = int(row.iloc[5] - 1)  # 6. sütun: Başlangıç indeksi
        length = int(row.iloc[6])            # 7. sütun: Uzunluk
        end_index = start_index + length      # Bitiş indeksi
        
        dynamic_vars[f"{table_name}_length_list"].append((start_index, end_index))
        dynamic_vars[f"{table_name}_start_index"] = start_index
        dynamic_vars[f"{table_name}_end_index"] = end_index
        
        fields = extract_fields_from_excel(df)
        model = create_model(table_name, fields)
        if table_name not in table_names:
            table_names.append(table_name)
    return render(request, 'index.html', {'table_names': table_names})

def parsing_raw_data(raw_data, length_list):
    parsed_data = [raw_data[start:end] for start, end in length_list]
    return parsed_data

def parseData(request):
    parsingSuccess = False
    parsed_data_list = []
    field_names = [] 
    if request.method == 'POST':
        parsingModel = (request.POST.get('parsingModel'))
        table_name = parsingModel
        start_index = f"{table_name}_start_index"
        end_index = f"{table_name}_end_index"
        length_list = dynamic_vars[f"{table_name}_length_list"]
        
        ModelClass = apps.get_model('ParsingApp', table_name)
        field_names = [field.name for field in ModelClass._meta.fields[1:]]
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM "{ModelClass._meta.db_table}"')  # Verileri sil
            cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{ModelClass._meta.db_table}"')  # ID'yi sıfırla

        for rawData in RawData.objects.all():
            # Kullanıcının seçimini al
            parsed_data = parsing_raw_data(rawData.data, length_list)
            model_instance = ModelClass()
            for i, field in enumerate(ModelClass._meta.fields[1:]):  # İlk alan genelde ID olur, o yüzden onu geçiyoruz
                setattr(model_instance, field.name, parsed_data[i])
            model_instance.save()
            
            parsed_data_list.append(parsed_data)
            parsingSuccess = True
    return render(request, 'index.html', {'parsingSuccess': parsingSuccess, 'parsed_data_list': parsed_data_list, 'field_names': field_names, 'table_names': table_names})
                
def create_excel(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        ModelClass = apps.get_model('ParsingApp', table_name)
        field_names = [field.name for field in ModelClass._meta.fields[1:]]  # İlk alan genelde ID olduğu için onu atlıyoruz
        
        # Yeni bir Excel dosyası oluştur
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = table_name

        # Başlıkları yaz
        sheet.append(field_names)

        # Verileri ekle
        for obj in ModelClass.objects.all():
            row = [getattr(obj, field) for field in field_names]
            sheet.append(row)

        # Excel dosyasını bir BytesIO nesnesine kaydet
        output = BytesIO()
        workbook.save(output)
        output.seek(0)  # Dosyanın başına geri dön

        # Excel dosyasını yanıt olarak döndür
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.xlsx"'
        return response

    return render(request, 'index.html', {'table_names': table_names})

def excelToRaw(request):
    success = False
    if request.method == 'POST':
        RawData.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='ParsingApp_rawdata'")  
        parsed_data_excel = request.FILES['parsedDataFile']
        df = pd.read_excel(parsed_data_excel)
        df_combined = df.apply(lambda row: ''.join(row.values.astype(str)), axis=1)
        df_combined = pd.DataFrame(df_combined, columns=['RawData'])
        for _, row in df_combined.iterrows():
            value = RawData(data=row[0])
            value.save()
        success = True
    return render(request, 'index.html', {'success': success})

def create_raw_data_excel(request):
    if request.method == 'POST' or request.method == 'GET':
        field_names = [field.name for field in RawData._meta.fields[1:]]  # İlk alan genelde ID olduğu için onu atlıyoruz
        
        # Yeni bir Excel dosyası oluştur
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "RawData"

        # Başlıkları yaz
        sheet.append(field_names)

        # Verileri ekle
        for obj in RawData.objects.all():
            row = [getattr(obj, field) for field in field_names]
            sheet.append(row)

        # Excel dosyasını bir BytesIO nesnesine kaydet
        output = BytesIO()
        workbook.save(output)
        output.seek(0)  # Dosyanın başına geri dön

        # Excel dosyasını yanıt olarak döndür
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="RawData.xlsx"'
        return response

    else:
        # POST ve GET dışında bir istek geldiğinde hata yanıtı döndür
        return HttpResponse("This view only supports GET and POST requests.", status=405)

def to_detail_page(request):
    return render(request, 'detail.html')

def to_main_page(request):
    return render(request, 'index.html')