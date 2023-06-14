from django.urls import path
from ecolors import views

urlpatterns=[
     path('',views.index),
     path('register',views.user_register),
     path('user_login',views.user_login),
     path('user_logout',views.user_logout),
     path('addshade',views.addshade),
     path('editshade/<rid>',views.editshade),
     path('delshade/<rid>',views.delshade),
     path('sort/<sv>',views.sort),
    path('catfilter/<catv>',views.catfilter),
    path('pricefilter/<pv>',views.pricefilter),
    path('pricerange',views.pricerange),
     path('cdetails/<pid>',views.color_details),
     path('cart/<pid>',views.addtocart),
     path('viewcart',views.viewcart),
     path('changeqty/<pid>/<f>',views.changeqty),
     path('placeorder',views.placeorder),

]