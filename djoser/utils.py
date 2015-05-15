from django.conf import settings as django_settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from rest_framework import response, status
from . import settings


def encode_uid(pk):
    try:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        return urlsafe_base64_encode(force_bytes(pk)).decode()
    except ImportError:
        from django.utils.http import int_to_base36
        return int_to_base36(pk)


def decode_uid(pk):
    try:
        from django.utils.http import urlsafe_base64_decode
        return urlsafe_base64_decode(pk)
    except ImportError:
        from django.utils.http import base36_to_int
        return base36_to_int(pk)


def send_email(to_email, from_email, context, subject_template_name,
               plain_body_template_name, html_body_template_name=None):
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(plain_body_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email],)
    if html_body_template_name is not None:
        html_email = loader.render_to_string(html_body_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    email_message.send(fail_silently=False)


class ActionViewMixin(object):

    # Basically This mixin defines a POST method handler
    # that triggers the main action of the view.
        # Main action of the view could be
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return self.action(serializer)
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetrieveActionViewMixin(object):

    # Basically This mixin defines a POST method handler
    # that triggers the main action of the view.
        # Main action of the view could be
    def post(self, request, pk):
        current_object = self.get_object()
        serializer = self.get_serializer(current_object, data=request.data, partial=True)
        if serializer.is_valid():
            return self.action(serializer, pk)
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


import sendgrid
sendgrid_username = django_settings.EMAIL_HOST_USER
sendgrid_password = django_settings.EMAIL_HOST_PASSWORD
# from_email = django_settings.DEFAULT_FROM_EMAIL


def sendgrid_email(to_email, from_email, context, subject_template_name, plain_body_template_name, html_body_template_name=None):
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(plain_body_template_name, context)
    plaintext_body = body
    html_body = "<p>" + plaintext_body.replace("\n", "</p><p>") + "</p>"
    sg = sendgrid.SendGridClient(sendgrid_username, sendgrid_password)
    message = sendgrid.Mail()
    # Set to_email, subject, HTML/text body, from_email
    message.add_to(to_email)
    message.set_subject(subject)
    message.set_html(html_body)
    message.set_text(body)
    message.set_from(from_email)
    # Set the template
    message.add_filter('templates', 'enable', '1')
    message.add_filter('templates', 'template_id', '232a4384-493c-49c1-b41d-4f9f2dcc52f7')
    message.add_filter('template', 'enable', '0')
    topic = context.get('topic', 'account_activation')
    email_url = context['url']
    if topic == 'reset_password':
        email_topic = "you requested a password reset for your user account at Beat Paradigm."
        email_action = "confirm your new password"
    elif topic == 'confirm_account_update':
        email_topic = "you have updated your user account at Beat Paradigm."
        email_action = "confirm the changes made"
    else:
        email_topic = "you created an account on Beat Paradigm."
        email_action = "activate account:"
    # Set the substitution headers
    message.set_substitutions({':topic': [email_topic], ':action': [email_action], ':url': [email_url]})
    # Send the email
    status, msg = sg.send(message)
    print status
    print msg


class SendEmailViewMixin(object):

    #3rd
    def send_email(self, to_email, from_email, context):
        if django_settings.USE_SENDGRID:
            sendgrid_email(to_email, from_email, context, **self.get_send_email_extras())
        else:
            send_email(to_email, from_email, context, **self.get_send_email_extras())

    # 1st
    def get_send_email_kwargs(self, user):
        return {
            'from_email': getattr(django_settings, 'DEFAULT_FROM_EMAIL', None),
            'to_email': user.email,
            'context': self.get_email_context(user, 'account_activation'),
        }

    def get_send_email_extras(self):
        raise NotImplemented

    # 2nd
    def get_email_context(self, user, topic):
        token = self.token_generator.make_token(user)
        uid = encode_uid(user.pk)
        context = {
            'user': user,
            'domain': settings.get('DOMAIN'),
            'site_name': settings.get('SITE_NAME'),
            'uid': uid,
            'token': token,
            'protocol': 'https' if self.request.is_secure() else 'http',
            'topic': topic
        }
        #context['url'] = context['protocol'] + '://' + context['domain'] + '/registration/activate/' + context['uid'] + '/' + context['token']
        return context


# # For local testing
# class SendEmailViewMixin(object):
#
#     #3rd
#     def send_email(self, to_email, from_email, context):
#         sendgrid_email(to_email, from_email, context, **self.get_send_email_extras())
#
#     # 1st
#     def get_send_email_kwargs(self, user):
#         return {
#             'from_email': getattr(django_settings, 'DEFAULT_FROM_EMAIL', None),
#             'to_email': user.email,
#             'context': self.get_email_context(user, 'account_activation'),
#         }
#
#     def get_send_email_extras(self):
#         return {
#             'subject_template_name': 'activation_email_subject.txt',
#             'plain_body_template_name': 'activation_email_body.txt',
#         }
#
#     # 2nd
#     def get_email_context(self, user, topic):
#         token = "token"
#         # if self.token_generator is not None:
#         #     token = self.token_generator.make_token(user)
#         uid = encode_uid(user.pk)
#         context = {
#             'user': user,
#             'domain': settings.get('DOMAIN'),
#             'site_name': settings.get('SITE_NAME'),
#             'uid': uid,
#             'token': token,
#             # 'protocol': 'https' if self.request.is_secure() else 'http',
#             'protocol': 'http',
#             'topic': topic,
#         }
#         context['url'] = context['protocol'] + '://' + context['domain'] + '/registration/activate/' + context['uid'] + '/' + context['token']
#         return context