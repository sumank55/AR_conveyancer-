# users/views.py
from rest_framework import generics
from django.shortcuts import render
from .models import User
from .serializers import UserSerializer, RegisterSerializer, UserLoginSerializer, ChangePasswordSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.http import HttpResponsePermanentRedirect
import os
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import FailedLogins
import datetime
from django.utils import timezone
import datetime as timedelta

# Create your views here.

User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


# Show All Users View
class UserListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Register New User View
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Login Users View
class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            try:
                User.objects.get(email=email)
            except:
                return Response({"error": "Your username/email is not correct. Please try again or register your details"})
            user = authenticate(email=email, password=password)
            if user is not None:
                try:
                    loginattempt = FailedLogins.objects.get(user=user)
                    if loginattempt is not None:
                        table_expire_datetime = loginattempt.updated_at + \
                            datetime.timedelta(minutes=30)
                        # Current datetime
                        current_datetime = timezone.now()
                        
                        expired_on = table_expire_datetime
                        checked_on = current_datetime

                        if expired_on > checked_on and loginattempt.failed_count == 5 :
                            return Response({"error": "You’ve been temporarily locked out of your account for 30 minutes. You can either try again in 30 minutes"}, status=400)
                        else:
                            pass
                except Exception as E:
                    pass
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'User logged in successfully',
                    'token': jwt_token,
                }
                status_code = status.HTTP_200_OK
                try:
                    FailedLogins.objects.get(user=user).delete()
                except:
                    pass
                return Response(response, status=status_code)
            else:
                try:
                    userdata = User.objects.get(email=email)
                    if userdata is not None:
                        try:
                            get_failed_login = FailedLogins.objects.get(
                                user=userdata)
                            if get_failed_login is not None:
                                if get_failed_login.failed_count != 5:
                                    attempt = get_failed_login.failed_count + 1
                                    FailedLogins.objects.filter(pk=get_failed_login.pk).update(failed_count=attempt)
                                    if get_failed_login.failed_count == 5:
                                        FailedLogins.objects.filter(pk=get_failed_login.pk).update(updated_at=datetime.datetime.utcnow())
                                else:
                                    return Response({"error": "You’ve been temporarily locked out of your account for 30 minutes. You can either try again in 30 minutes"}, status=400)
                        except Exception as E:
                            FailedLogins.objects.create(
                                failed_count=1, user=userdata)
                except Exception as E:
                    pass
                return Response({"error": 'Your password is not correct please try again or reset your password'}, status=401)


# Change Password View
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Sending Forgot Password Email View
class RequestPasswordResetEmail(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        if serializer.is_valid():
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink = reverse(
                    'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                redirect_url = request.data.get('redirect_url', '')
                absurl = current_site + relativeLink
                email_body = 'Hello, \n Use link below to reset your password  \n' + \
                    absurl+"?redirect_url="+redirect_url
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset your passsword'}
                Util.send_email(data)
                return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": 'Requested Email Not Found'}, status=409)
        else:
            return Response({'error': 'Email feild required'}, status=400)


# Check Password Token API View
class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')
            return Response({"success": True, "messsage": "Credential Valid", "uidb64": uidb64, 'token': token}, status=status.HTTP_200_OK)
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


# Set New Password
class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


# Get Current User Details
class CurrentUserView(generics.GenericAPIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
