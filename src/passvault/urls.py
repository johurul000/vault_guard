"""
URL configuration for passvault project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage, name='home'),
    path('signup/', views.SignUpPage, name='signup'),
    path('login/', views.LogInPage, name='login'),
    path('logout/', views.LogOutPage, name='logout'),

    path('quickpin/', views.AddQuickPin, name='quickpin'),
    path('checkpin/', views.CheckPin, name='checkpin'),


    path('addpass/', views.AddPass, name='addpass'),
    path('editpass/<int:password_id>/', views.EditPass, name='editpass'),
    path('viewpass/<int:password_id>/', views.ViewPass, name='viewpass'),
    path('deletepass/<int:password_id>/', views.DeletePass, name='deletepass'),
    

    path('addnote/', views.AddNote, name='addnote'),
    path('editnote/<int:note_id>/', views.EditNote, name='editnote'),
    path('viewnote/<int:note_id>/', views.ViewNote, name='viewnote'),
    path('deletenote/<int:note_id>/', views.DeleteNote, name='deletenote'),

    path('addbank/', views.AddBank, name='addbank'),
    path('editbank/<int:bank_id>/', views.EditBank, name='editbank'),
    path('viewbank/<int:bank_id>/', views.ViewBank, name='viewbank'),
    path('deletebank/<int:bank_id>/', views.DeleteBank, name='deletebank'),


    path('addcard/', views.AddCard, name='addcard'),
    path('editcard/<int:card_id>/', views.EditCard, name='editcard'),
    path('viewcard/<int:card_id>/', views.ViewCard, name='viewcard'),
    path('deletecard/<int:card_id>/', views.DeleteCard, name='deletecard'),

    path('listpass/', views.ListPass, name='listpass'),
    path('listnote/', views.ListNote, name='listnote'),
    path('listbank/', views.ListBank, name='listbank'),
    path('listcard/', views.ListCard, name='listcard'),


    path('updateprofile/', views.UpdateProfile, name='updateprofile'),
    path('viewprofile/', views.ViewProfile, name='viewprofile'),
    path('updatepassword/', views.UpdatePassword, name='updatepassword'),
    path('updatequickpin/', views.UpdateQuickpin, name='updatequickpin'),

]
