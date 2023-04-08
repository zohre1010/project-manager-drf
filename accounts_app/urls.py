from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

app_name = 'accounts_app'
urlpatterns = [
    path('update/<int:pk>/',views.UserProfileUpdateView.as_view(),name='user_update'),
    path('edit/<int:pk>/',views.UserEditUpdateView.as_view(),name='user_update_'),
    path('list/',views.UserlistView.as_view(),name='user_list'),
    path('delete/<int:pk>/',views.UserDeleteView.as_view(),name='user_delete'),
    path('login/', views.LoginView.as_view(),name='user_login'),
    path('login-status/', views.current_user, name="login_status"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name="profile"),  
    # ____________________________________________________________________________________________
    path('forget_password/', views.UserPasswordResetView.as_view(), name="forget_password"),
    path('forget_password/verify/', views.UserPasswordResetConfirmView.as_view(), name="forget_password"),
    path('forget_password/set/<int:pk>/', views.ForgetPasswordView.as_view(), name="forget_password"),
    #___________________________________________________________________________________________________
    path('admins/', views.ListOfAdminView.as_view(), name="admins"),
    path('managers/', views.ListOfManagerView.as_view(), name="managers"),
    path('employees/', views.ListEmployeeView.as_view(), name="employees"),
    path('up-to-admin/<int:pk>/', views.UpToAdminView.as_view(), name="admin"),
    path('up-to-manager/<int:pk>/', views.UpToManagerView.as_view(), name="manager"),
    # ___________________________________________________________________________________
    path('set-online/<int:pk>/', views.SetOnlineView.as_view(), name="set_online"),
    path('set-offline/<int:pk>/', views.SetOfflineView.as_view(), name="set_offline"),
    path('online/<int:pk>/', views.GetOnlineOrOfflineView.as_view(), name="online"),
]
router = DefaultRouter()
router.register('', views.OTPViewSet, basename='otp')

urlpatterns += router.urls