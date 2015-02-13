# Create your views here.
import datetime

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import stripe
from django.contrib import auth
from django.core.context_processors import csrf
from CustomDrumSamples import settings
from userprofile.forms import *
from userprofile.models import *
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET


























