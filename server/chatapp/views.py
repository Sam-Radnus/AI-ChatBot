from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import CustomUser
from .APIExampleChatStream import print_response_stream  # Assuming you've converted the main functionality to a function
from django.db.utils import IntegrityError
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt,json
from django.http import HttpResponse
import asyncio
from django.views.decorators.csrf import csrf_exempt
from channels.db import database_sync_to_async
from datetime import datetime

@api_view(['POST'])
def user_signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return JsonResponse({'error': 'Username or password not provided'}, status=400)

    try:
        user = CustomUser.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'User created successfully!',
            'user': user.id,
            'email':username,
            'password':password,
            'access_token': str(refresh.access_token)
        }, status=201)
    
    except IntegrityError:
        return JsonResponse({'error': 'Username already exists'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': f'Some error occurred: {str(e)}'}, status=400)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username)
    print(password)
    user = authenticate(request, username=username, password=password)
    print(user)
    if user:
        try:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            print(refresh.access_token)
            return JsonResponse({
                'message': 'Logged in successfully!',
                'email':username,
                'password':password,
                'access_token': str(refresh.access_token)
            }, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': e}, status=400)
    
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def interact_with_ai(request):  # Note: This is a synchronous function now.
    # Extract Bearer Token from request header
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if not auth_header:
        return HttpResponse({'error': 'Authorization header missing.'}, status=401)
    try:
        
        token = auth_header.split(' ')[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        print(decoded_token)
        user_id=decoded_token['user_id']
        user=CustomUser.objects.get(id=user_id)
        print(user)
        if user is None:
            return HttpResponse({'error': 'Invalid authentication token.'}, status=401)
    except jwt.ExpiredSignatureError:
        return HttpResponse({'error': 'Authentication token expired.'}, status=401)
    except jwt.InvalidTokenError:
        return HttpResponse({'error': 'Invalid authentication token.'}, status=401)
    

    if user.calls_made >= 25:
        return HttpResponse({'error': 'You have exceeded the number of calls allowed.'}, status=401)
    
    data = json.loads(request.body)
    # Validate title and caption fields
    prompt = data.get('prompt')
    print(prompt)
    response = run_sync_print_response_stream(prompt)  # Using the synchronous adapter here.
    print(2)
    if len(response)>0:
       user.calls_made += 1
       user.save()
    #await increment_calls_made(request.user)
    current_time = datetime.now().strftime('%I:%M %p')
    return JsonResponse({'response': response,'current_time':current_time,'calls_left':25-user.calls_made}, status=200)

def run_sync_print_response_stream(prompt):
    loop = asyncio.new_event_loop()
    response = loop.run_until_complete(print_response_stream(prompt))
    loop.close()
    return response

@api_view(['GET'])
def get_calls_made(request):
    # Extract Bearer Token from request header
    print(1)
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if not auth_header:
        return HttpResponse({'error': 'Authorization header missing.'}, status=401)
    print(2)
    try:
        print(3)
        token = auth_header.split(' ')[1]
        print(token)
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        print(user_id)
        user = CustomUser.objects.get(id=user_id)
        if user is None:
            return HttpResponse({'error': 'Invalid authentication token.'}, status=401)
    except jwt.ExpiredSignatureError:
        return HttpResponse({'error': 'Authentication token expired.'}, status=401)
    except jwt.InvalidTokenError:
        return HttpResponse({'error': 'Invalid authentication token.'}, status=401)
     
    return JsonResponse({
        'user_id': user_id,
        'username':user.username,
        'promptsLeft': 25-user.calls_made
    }, status=200)

