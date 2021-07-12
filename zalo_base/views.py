from django.http import HttpResponse

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
 
from .models import ZaloMessage

import json

def index(request):
    return HttpResponse("Hello, world. Welcome to us.")

@api_view(['GET', 'POST', 'DELETE'])
def message(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        return JsonResponse(data, status=status.HTTP_201_CREATED) 
    
    elif request.method == 'DELETE':
        count = ZaloMessage.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def test(request):
    if (request.method == 'GET'):
        # for k,v  in request.headers:
        #     print(item)
        # print(request.headers)
        print(request.headers)
        print(request.query_params)
    return HttpResponse("Ok")

@api_view(['POST'])
def follow_hook(request):
    if (request.method == 'POST'):
        datas = request.body
        print(datas)
    
    return HttpResponse("Ok")



