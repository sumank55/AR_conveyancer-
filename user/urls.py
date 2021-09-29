from django.urls import path
from user import views




urlpatterns = [
    path('', views.UserListView.as_view()),
    path('register/', views.RegisterUserView.as_view(), name='auth_register'), #Register New User Url
    path('login/', views.UserLoginView.as_view(), name='auth_login'),#Login User Url
    path('change-password/', views.ChangePasswordView.as_view(), name='auth_change_password'),#Change Password User Ur
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),#Send Email User Url For Reset Password
    path('password-reset/<uidb64>/<token>', views.PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),#Password Reset Confirm User Url
    path('password-reset-complete/',views.SetNewPasswordAPIView.as_view(), name="password-reset-complete"),#Password Reset  User Url
    path('current-user/', views.CurrentUserView.as_view(), name='current-user'),#Get Current User Url

]