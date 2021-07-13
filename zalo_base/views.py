from django.http import HttpResponse

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
 
from .services import ZaloService

import json

def index(request):
    return HttpResponse("Hello, world. Welcome to us.")

@api_view(['GET'])
def tkyt(request):
    if (request.method == 'GET'):
        print(request.headers)
        return JsonResponse({
            # "GET": request.GET,
            # "POST": request.POST,
            # "COOKIES": request.COOKIES,
            # "META": request.META,
            # "FILES": request.FILES,
            # "method": request.method,
            "content_params": request.content_params
        })

    return JsonResponse({
        'success': 0, 
        'message': f"Request method {request.method} is not allowed!"
        })

@api_view(['POST'])
def follow_hook(request):
    if (request.method == 'POST'):
        datas = json.loads(request.body)
        event = datas.get('event_name', False)
        if event:
            result = ZaloService().action_by_event(event, datas)
            return JsonResponse(result)

    return JsonResponse({
        'success': 0, 
        'message': f"Request method {request.method} is not allowed!"
        })

@api_view(['POST'])
def confirm_destination(request):
    if (request.method == 'POST'):
        datas = json.loads(request.body)
        phone = datas.get('phone', False)
        if phone:
            return ZaloService().send_confirm_message(phone)
    return JsonResponse({
        'success': 0, 
        'message': f"Request method {request.method} is not allowed!"
        })


