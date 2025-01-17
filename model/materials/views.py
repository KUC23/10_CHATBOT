from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.models import News
from accounts.models import Category
import redis
import json
from django.conf import settings
