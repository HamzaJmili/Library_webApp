from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("book/<int:id_book>/<str:borrowed>",views.book,name="single_book"),
    path("login",views.login,name="login"),
    path("borrow/<int:id_book>",views.borrow_book,name="borrow"),
    path("logout",views.logout,name="logout"),
    path("profile",views.profile,name="profile"),
     path('emprunt/<int:pk>/confirm_return/', views.confirm_return_emprunt, name='confirm_return_emprunt'),
     path('emprunt/<int:pk>/confirm/', views.confirm, name='confirm'),

]