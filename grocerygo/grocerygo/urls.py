from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings
from cadmin.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('navigation/', navigation, name="navigation"),
    path('about/', about, name="about"),
    path('', index, name="index"),
    path('contact/', contact, name="contact"),
    path('admin_login/',adminLogin, name="admin_login"),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),
    path('add-product/', add_product, name='add_product'),
    path('view-product/', view_product, name='view_product'),
    path('edit-product/<int:pid>/', edit_product, name="edit_product"),
    path('delete-product/<int:pid>/', delete_product, name="delete_product"),
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    path('profile/', profile, name="profile"),
    path('logout/', logoutuser, name="logout"),
    path('change-password/', change_password, name="change_password"),
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('booking/', booking, name="booking"),
    path('my-order/', myOrder, name="myorder"),
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    path('user-feedback/', user_feedback, name="user_feedback"),
    path('manage-feedback/', manage_feedback, name="manage_feedback"),
    path('delete-feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    path('feedback-read/<int:pid>/', read_feedback, name="read_feedback"),
    path('payment/', payment, name="payment"), 
    path('manage-order/', manage_order, name="manage_order"), 
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
    path('manage-messages/', manage_messages, name="manage_messages"), 
    path('read_messages/<int:pid>/', read_messages, name='read_messages'),
    path('get_message_counts/', get_message_counts, name='get_message_counts'),
    path('delete-messages/<int:pid>/', delete_messages, name='delete_messages'), 
    # path('message-read/<int:pid>/', read_messages, name="read_messages"),
    path('track-purchase/<int:pid>/', track_purchase, name='track_purchase'),

    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)