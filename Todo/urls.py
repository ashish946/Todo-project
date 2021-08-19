
from django.contrib import admin
from django.urls import path, include
from todowo import views
from api import urls

urlpatterns = [
    #Auth
    path('admin/', admin.site.urls),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    

    #Todos
    path('', views.home, name='home'),
    path('currenttodo/', views.currenttodo, name='currenttodo'),
    path('create/', views.createtodos, name='createtodos'),
    path('completed/', views.completed, name='completed'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),


    # API
    path('api/',include('api.urls')),


]
