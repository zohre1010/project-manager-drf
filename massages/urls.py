from django.urls import path
from . import views



app_name = 'massage'
urlpatterns = [    
    path('ticket/list/<int:pk>/',views.TicketListView.as_view(),name='ticket_list'),
    path('ticket/reply/<int:project_id>/<int:ticket_id>/', views.TicketReplyView.as_view(), name='Reply_ticket'),
    path('ticket/create/<int:project_id>/', views.TicketCreateView.as_view(), name='add_ticket'),
    path('ticket/replys/<int:ticket_id>/', views.ReplyForOneTicket.as_view(), name='replys_ticket'),
    path('ticket/check/<int:pk>/', views.DoneTicketView.as_view(), name='check_ticket'),
    # _____________________________________________________________________________________________
    path('newchat/', views.ChatCreateView.as_view(), name='newchat'),
    path('chat/<int:chat_id>/', views.SendMessageView.as_view(), name='chat'),
    path('list/<int:pk>/', views.ListConversazioneView.as_view(), name='listchat'),    
    path('delete/<int:pk>/', views.DeleteConversazioneView.as_view(), name='deletechat'),
    path('block/<int:pk>/', views.BlockConversazioneView.as_view(), name='blockchat'),
    path('unblock/<int:pk>/', views.UnBlockConversazioneView.as_view(), name='unblockchat'),    
  
    # ______________________________________________________________________________________________
    
    path('channel/create/', views.ChannelCreateView.as_view(), name='create_channel'),
    path('channel/<int:channel_id>/', views.SendMessageChannelView.as_view(), name='channel'),   
    path('channel/list/<int:pk>/', views.ListChannelView.as_view(), name='list_channel'), 
    path('channel/delete/<int:pk>/', views.DeleteChannelView.as_view(), name='delete_channel'), 
    path('channel/join/<int:pk>/', views.JoinChannelView.as_view(), name='join_channel'), 
    path('channel/edit/<int:pk>/', views.EditChannelView.as_view(), name='edit_channel'),  
    path('channel/remove-member/<int:pk>/', views.RemoveMemberView.as_view(), name='edit_channel'),  
]
