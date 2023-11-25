from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name="main"),
    # path('police-landing', views.police_landing,name='landing-police'),
    path('police/register', views.police_register, name='police-register'),
    path('police/setting',views.police_setting,name="police-settings"), 
    path('edit/police/setting',views.edit_setting,name="edit-police"),
    path('police/login',views.police_login,name='police-login'),
    path('police/logout',views.police_logout,name='police-logout'),
    path('index-police',views.index_police,name="landing"),
    path('complain',views.log_complain,name='offense'),


    # path("citizen/landing",views.citizen_landing, name="citizen-landing"),
    path('citizen/register',views.citizen_register,name="citizen-register"),
    path('view-complains',views.view_offense,name='view-offense'),
    path('citizen/setting',views.citizen_setting,name="citizen-setting"),
    path('citizen/edit/setting',views.edit_citizen_setting,name="citizen-edit"),
    path('citizen/login',views.citizen_login,name="citizen-login"),
    path('citizen/logout',views.citizen_logout,name="citizen-logout"),
    path('citizen/specific/<str:identifier>', views.specific, name="specific"),  


    path('citizen-index',views.citizen_homepage,name='home-page'),



    path('test',views.test)

   


]
