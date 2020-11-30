from django.urls import path
from manager import views

app_name='manager'

urlpatterns = [
    path('register/',views.user_info_view,name='register'),
    path('user_login/',views.user_login,name="user_login"),
    path('home_lead/',views.home_lead,name="home_lead"),
    path('home_mem/',views.home_mem,name="home_mem"),
    path('thanks/',views.thanks,name="thanks"),
    path('no_entry/',views.no_entry,name="no_entry"),
    path('completed/',views.completed,name="completed"),
    path('yet_to_completed/',views.yet_to_completed,name="yet_to_completed"),


]
