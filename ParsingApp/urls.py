from django.urls import path
from .views import index, resetDataBase, parseData, createModel, create_excel, excelToRaw, create_raw_data_excel, to_detail_page, to_main_page

urlpatterns = [
    path('', index, name='index'),
    path('resetDataBase/', resetDataBase, name='resetDataBase'),
    path('parseData/', parseData, name='parseData'),
    path('createModel/', createModel, name='createModel'),
    path('create_excel/', create_excel, name='create_excel'),  # Yeni yol
    path('excelToRaw/', excelToRaw, name='excelToRaw'),  # Yeni yol
    path('create_raw_data_excel/', create_raw_data_excel, name='create_raw_data_excel'),  # Yeni yol
    path('to_detail_page//', to_detail_page, name='to_detail_page'),
    path('to_main_page/', to_main_page, name='to_main_page'),
]

