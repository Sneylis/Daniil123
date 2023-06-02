from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as authViews

app_name ='techMarket'
urlpatterns =[
    path('',views.index,name='index'),
    path('about/',views.about,name='About'),
    path('cat/<int:cat_id>',views.ShCat,name='showCategory'),
    path('unit/<int:unit_id>',views.ShUnit,name='ShowUnit'),
    path('register/',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('exit/',authViews.LogoutView.as_view(next_page='techMarket:index'),name='exit'),
    path('addUnit/',views.AddUnit,name='addunit'),
    path('updUnit/<int:pk>/', views.updunit.as_view(), name='updUnit'),
    path('del/<int:unit_id>',views.delunit,name='delUnit'),
    path('addbucket/<int:unit_id>',views.addBucket,name='AddBucket'),
    path('MuBucket/',views.ShBucket,name='ShBucket'),
    path('MuBucket/<int:u_id>',views.updl.as_view(),name='ShBucket'),
    path('delBucket/<int:bucket_id>',views.delBucket,name='DelBucket'),
    path('comm/<int:unit_id>/',views.addComment,name='commen'),
    path('like/<int:unit_id>',views.addLike,name='AddLike'),



]
