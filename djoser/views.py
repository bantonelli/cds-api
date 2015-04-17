from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, response
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from provider.oauth2.models import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings as django_settings
from . import serializers, settings, utils, djpermissions

import json
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class OauthUserMixin():

    def get_current_user(self, request):
        # If the user is in session auth get that user
        if request.user:
            return request.user
        # Otherwise get the user based on Auth header
        elif request.META['Authorization']:
            auth_header = request.META['Authorization']
            index = auth_header.find('Bearer') + 7
            token_string = auth_header[index:]
            token = AccessToken.objects.get_token(token=token_string)
            user = token.user
            return user
        else:
            return None


# curl -X GET http://127.0.0.1:8000/api/accounts/resend-activation
# curl -X POST http://127.0.0.1:8000/api/accounts/resend-activation --data 'userID=12&csrfmiddlewaretoken=1jln3sCDdzfTquZighUrMHGk4helQKOs'
# 1jln3sCDdzfTquZighUrMHGk4helQKOs
class SetCSRFView(View):

    def get(self, request):
        return HttpResponse("cookie set")


class ResendActivationEmailView(View, utils.SendEmailViewMixin, OauthUserMixin):

    token_generator = default_token_generator

    def post(self, request):
        result = []
        mail_sent = False
        user_id = request.POST['user_id']

        # Check for user input / post data errors
        user = None
        try:
            user = User.objects.get(pk=user_id)
            if settings.get('SEND_ACTIVATION_EMAIL'):
                self.send_email(**self.get_send_email_kwargs(user))
                mail_sent = True
            # Build JSON response object
            result.append({
                "mail_sent": mail_sent
            })
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp
        except ObjectDoesNotExist:
            result.append({"data_error": "user is invalid"})
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp

    def get_send_email_extras(self):
        return {
            'subject_template_name': 'activation_email_subject.txt',
            'plain_body_template_name': 'activation_email_body.txt',
        }

    def get_email_context(self, user):
        context = super(ResendActivationEmailView, self).get_email_context(user)
        context['url'] = settings.get('ACTIVATION_URL').format(**context)
        return context


class RegistrationView(utils.SendEmailViewMixin, generics.CreateAPIView, OauthUserMixin):
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def get_serializer_class(self):
        if settings.get('LOGIN_AFTER_REGISTRATION'):
            return serializers.UserRegistrationWithAuthTokenSerializer
        return serializers.UserRegistrationSerializer

    def post_save(self, obj, created=False):
        # For Token Based authentication only not Oauth2
        if settings.get('LOGIN_AFTER_REGISTRATION'):
            Token.objects.get_or_create(user=obj)
        if settings.get('SEND_ACTIVATION_EMAIL'):
            self.send_email(**self.get_send_email_kwargs(obj))

    def get_send_email_extras(self):
        return {
            'subject_template_name': 'activation_email_subject.txt',
            'plain_body_template_name': 'activation_email_body.txt',
        }

    def get_email_context(self, user):
        context = super(RegistrationView, self).get_email_context(user)
        context['url'] = settings.get('ACTIVATION_URL').format(**context)
        return context

# class LoginView(utils.ActionViewMixin, generics.GenericAPIView, OauthUserMixin):
#     serializer_class = serializers.UserLoginSerializer
#     permission_classes = (
#         permissions.AllowAny,
#     )
#
#     def action(self, serializer):
#         token, _ = Token.objects.get_or_create(user=serializer.object)
#         return Response(
#             data=serializers.TokenSerializer(token).data,
#             status=status.HTTP_200_OK,
#         )
#
#
# class LogoutView(generics.GenericAPIView, OauthUserMixin):
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#
#     def post(self, request):
#         Token.objects.filter(user=request.user).delete()
#
#         return response.Response(status=status.HTTP_200_OK)


class SetPasswordView(utils.ActionViewMixin, generics.GenericAPIView, OauthUserMixin):
    permission_classes = (
        permissions.IsAuthenticated, djpermissions.IsActiveUser
    )

    def get_serializer_class(self):
        if settings.get('SET_PASSWORD_RETYPE'):
            return serializers.SetPasswordRetypeSerializer
        return serializers.SetPasswordSerializer

    def action(self, serializer):
        user = self.get_current_user(self.request)
        if user is not None:
            user.set_password(serializer.data['new_password'])
            user.save()
            data = {"password_reset": True}
            return response.Response(data=data, status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(utils.ActionViewMixin, utils.SendEmailViewMixin, generics.GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def action(self, serializer):
        user = self.get_user(serializer.data['email'])
        if user is not None:
            if user.is_active:
                new_password = serializer.data['new_password']
                user.set_temp_password(new_password)
                user.save()
                self.send_email(**self.get_send_email_kwargs(user))
                return response.Response(status=status.HTTP_200_OK)
            else:
                data = {"user": ["The user account associated with this email is not active!"]}
                return response.Response(data=data, status=status.HTTP_403_FORBIDDEN)
        else:
            data = {"email": ["The E-mail you have supplied does not match our records!"]}
            return response.Response(data=data, status=status.HTTP_404_NOT_FOUND)

    def get_user(self, email):
        # active_users = User._default_manager.filter(
        #     email__iexact=email,
        #     is_active=True,
        # )
        # return (u for u in active_users if u.has_usable_password())
        user = None
        try:
            user = User.objects.get(email=email)
            return user
        except ObjectDoesNotExist:
            return None

    def get_send_email_extras(self):
        return {
            'subject_template_name': 'password_reset_email_subject.txt',
            'plain_body_template_name': 'password_reset_email_body.txt',
        }

    def get_email_context(self, user):
        context = super(PasswordResetView, self).get_email_context(user)
        context['url'] = settings.get('PASSWORD_RESET_CONFIRM_URL').format(**context)
        return context


class PasswordResetConfirmView(utils.ActionViewMixin, generics.GenericAPIView):
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def get_serializer_class(self):
        # if settings.get('PASSWORD_RESET_CONFIRM_RETYPE'):
        #     return serializers.PasswordResetConfirmRetypeSerializer
        # return serializers.PasswordResetConfirmSerializer
        return serializers.UidAndTokenSerializer

    def action(self, serializer):
        serializer.user.password = serializer.user.temp_password
        serializer.user.save()
        return response.Response(status=status.HTTP_200_OK)


class ActivationView(utils.ActionViewMixin, generics.GenericAPIView):
    serializer_class = serializers.UidAndTokenSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def action(self, serializer):
        if serializer.user.is_suspended:
            data = {"user": ["The user account associated with this email is suspended!"]}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            serializer.user.is_active = True
            serializer.user.save()
            if settings.get('LOGIN_AFTER_ACTIVATION'):
                token, _ = Token.objects.get_or_create(user=serializer.user)
                data = serializers.TokenSerializer(token).data
            else:
                # Make this send back user
                data = {}
            return Response(data=data, status=status.HTTP_200_OK)


class SetUsernameView(utils.ActionViewMixin, generics.GenericAPIView, OauthUserMixin):
    serializer_class = serializers.SetUsernameSerializer
    permission_classes = (
        permissions.IsAuthenticated, djpermissions.IsActiveUser
    )

    def get_serializer_class(self):
        if settings.get('SET_USERNAME_RETYPE'):
            return serializers.SetUsernameRetypeSerializer
        return serializers.SetUsernameSerializer

    def action(self, serializer):
        user = self.get_current_user(self.request)
        if user is not None:
            setattr(user, User.USERNAME_FIELD, serializer.data['new_' + User.USERNAME_FIELD])
            user.save()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveAPIView, OauthUserMixin):
    model = User
    serializer_class = serializers.UserSerializer
    permission_classes = (
        permissions.IsAuthenticated, djpermissions.IsActiveUser
    )

    def get_object(self, *args, **kwargs):
        return self.get_current_user(self.request)

    # def post_save(self, obj, created=False):
    #     print 'tags', self.request.DATA
    #     obj.tags.add(self.request.DATA['tags'])
    #     return super(EventListAPIView, self).post_save(obj)

    # def pre_save(self, obj):
    #     """
    #     Set the object's owner, based on the incoming request.
    #     """
    #     obj.user = self.request.user
    #     return super(EventListAPIView, self).pre_save(obj)

# bantonelli07@gmail.com
# curl -H "Authorization: Bearer 07a5d961e3364d2292da03b0c52156c3969548ed" http://localhost:8000/api/accounts/me
# maddenmoment@gmail.com
# curl -H "Authorization: Bearer a278f591253645a35a262941e8b466f8bf14dde8" http://localhost:8000/api/accounts/me


class UpdateUserView(utils.SendEmailViewMixin, generics.UpdateAPIView, OauthUserMixin):

    model = User
    permission_classes = (
        permissions.IsAuthenticated, djpermissions.IsActiveUser,
    )
    token_generator = default_token_generator

    def get_object(self, *args, **kwargs):
        return self.get_current_user(self.request)

    def get_serializer_class(self):
        return serializers.UpdateUserSerializer

    def post_save(self, obj, created=False):
        self.send_email(**self.get_send_email_kwargs(obj))

    def get_send_email_extras(self):
        return {
            'subject_template_name': 'confirm_user_update_email_subject.txt',
            'plain_body_template_name': 'confirm_user_update_email_body.txt',
        }

    # Override original implementation of this method to send
    # confirmation to temp_email address.
    def get_send_email_kwargs(self, user):
        return {
            'from_email': getattr(django_settings, 'DEFAULT_FROM_EMAIL', None),
            'to_email': user.temp_email,
            'context': self.get_email_context(user),
        }

    def get_email_context(self, user):
        context = super(UpdateUserView, self).get_email_context(user)
        context['url'] = settings.get('ACCOUNT_UPDATE_CONFIRM_URL').format(**context)
        return context


class UpdateUserConfirmView(utils.ActionViewMixin, generics.GenericAPIView):
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def get_serializer_class(self):
        return serializers.UidAndTokenSerializer

    def action(self, serializer):
        serializer.user.email = serializer.user.temp_email
        serializer.user.username = serializer.user.temp_username
        serializer.user.save()
        return response.Response(status=status.HTTP_200_OK)