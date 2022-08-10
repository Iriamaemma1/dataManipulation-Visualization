from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static



#app_name = "datavisual"

urlpatterns=[
    path('home',views.home,name="datavisual"),
    path('histogram/',views.histogram,name="view histogram page"),  
    path('scatter/',views.scatter,name="view scatter page"),
    path('first5/',views.first5,name="view first5 page"), 
    path('last5/',views.last5,name="view last5 page"), 
    path('modelStats/',views.modelStats,name="view modelStats page"), 
    path('normalDistCurve/',views.normalDistCurve,name="view normalDistCurve page"), 
    path('description/',views.description,name="view description page"),  
    path('', views.upload_file_view, name="upload_csv"),
    #path('csvs', include("csvs.urls"),name="csvs"),      


            ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




            #william codes