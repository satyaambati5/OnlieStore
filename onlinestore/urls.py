from django.urls import path

from .import views

urlpatterns = [
    # pages redirections
    path('', views.home, name='home'),
    path('Profile/', views.profile_view, name='profile'),
    path('categories/', views.category ,name='categories'),
    path('search==true/', views.search, name='search'),

    path('registration/', views.registration_page, name='register_page'),
    path('loginpage/', views.login_page, name='login_page'),
    path('forgotpassword/', views.forgotpage, name='forgotpage'),
    path('cart/',views.cart_page,name='cartpage'),
    path('invoice/', views.invoice, name='order_summary'),
    path('order-process-step==1/', views.orderstep1, name='orderstep1'),
    path('order-process-step==2/', views.orderstep2, name='orderstep2'),
    path('order-process-success/', views.mail_confirm, name='success'),
    # login functionality
    path('signup/', views.save_data, name='save'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('password-restored-success/', views.forgot, name='changepassword'),
    #login end
    # cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('Order_history/',views.order_history, name='carthistory'),
    # path('Canceled/', views.cancelorder, name='cancelorder'),


    path('cart_clear/', views.cart_clear, name='cart_clear'),
    # path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
   
]
  
