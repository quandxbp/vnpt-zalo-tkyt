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
def declare_confirm(request):
    message = f"Request method {request.method} is not allowed!"
    if (request.method == 'GET'):
        datas = request.GET
        if datas.get('zuser_id'):
            result = ZaloService().send_confirm_message(datas)
            return JsonResponse(result)
        message = 'Zalo User ID is not provided'
    return JsonResponse({
        'success': 0, 
        'message': message
        })

@api_view(['GET'])
def checkpoint_confirm(request):
    if (request.method == 'GET'):
        datas = request.GET
        if datas.get('phone'):
            result = ZaloService().send_confirm_at_checkpoint(datas.get('phone'))
            return JsonResponse(result)
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


