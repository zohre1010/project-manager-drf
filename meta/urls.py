from django.urls import path
from . import views



app_name = 'meta'
urlpatterns = [  
     path('', views.ReportsView.as_view(), name='meta'),
     path('<int:pk>/', views.ReportOneUserView.as_view(), name='meta_user'),
     #________________________________________________________________________  
     path('notif/create/', views.CreateNotifView.as_view(), name='newnotif'),
     path('notif/', views.LastNotifView.as_view(), name='notif'),
     path('notifs/', views.NotifsView.as_view(), name='notifs'),
     #___________________________________________________________________
     path('ticket/', views.ReportTicketView.as_view(), name='ticket_meta'),
     path('chat/', views.ReportChatView.as_view(), name='chat_meta'),
     path('login-logout/', views.ReportLoginView.as_view(), name='login_meta'),
    
]
