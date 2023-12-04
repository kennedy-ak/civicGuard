from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name="main"),

    path('police/register', views.police_register, name='police-register'),
    path('police/setting',views.police_setting,name="police-settings"), 
    path('edit/police/setting',views.edit_setting,name="edit-police"),
    path('police/login',views.police_login,name='police-login'),
    path('police/logout',views.police_logout,name='police-logout'),
    path('index-police',views.index_police,name="landing"),
    path("specific/<int:id>",views.specific_user,name="specific_user"),
    path("complain",views.file_complaint,name="complain"),




    path('citizen/register',views.citizen_register,name="citizen-register"),

    path('citizen/setting',views.citizen_setting,name="citizen-setting"),
    path('citizen/edit/setting',resetviews.edit_citizen_setting,name="citizen-edit"),
    path('citizen/login',views.citizen_login,name="citizen-login"),
    path('citizen/logout',views.citizen_logout,name="citizen-logout"),
    path("password_reset",view.password_reset,name ="password_reset"),
    path("passwoed_reset/done".viewS_password_reset_done,name, name ="password_reset_done"),



    path('citizen-index',views.citizen_homepage,name='home-page'),



    path('test',views.test)

   


]
