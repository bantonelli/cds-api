from django.conf.urls import patterns, url
from . import views
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

User = get_user_model()

urlpatterns = patterns('',
    url(r'^me$', views.UserView.as_view(), name='user'),
    #REGISTER uses DRF create view
    url(r'^register$', views.RegistrationView.as_view(), name='register'),
    # url(r'^login$', views.LoginView.as_view(), name='login'),
    # url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^activate$', views.ActivationView.as_view(), name='activate'),
    #url(r'^setusername$', views.SetUsernameView.as_view(), name='set_username'),
    #UPDATE uses DRF update view
    url(r'^update$', views.UpdateUserView.as_view(), name="update_account"),
    url(r'^update/confirm$', views.UpdateUserConfirmView.as_view(), name="update_account_confirm"),
    #PASSWORD uses action view mixin to get the serializer errors
    url(r'^password$', views.SetPasswordView.as_view(), name='set_password'),
    url(r'^password/reset$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm$', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #Resend activation view requires csrf token in the post data and request cookies.
    url(r'^resend-activation$', views.ResendActivationEmailView.as_view(), name='resend_activate'),
    url(r'^setup$', ensure_csrf_cookie(views.SetCSRFView.as_view()), name='set_cookie'),
)