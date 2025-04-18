# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import json
from .models import User

# username,email,password,mobile,is_verified,role,
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            mobile = data.get('mobile', '').strip()
            role = data.get('role', '').strip()

            errors = {}

            if not email:
                errors['email'] = 'Email is required.'
            if not password:
                errors['password'] = 'Password is required.'
            if not mobile:
                errors['mobile'] = 'Mobile number is required.'
            if not role:
                errors['role'] = 'Role is required.'

            if errors:
                return JsonResponse({'status': False, 'errors': errors}, status=400)

            # # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': False, 'message': 'Email already exists.'}, status=409)

            # Save the user
            User.objects.create(
                username=username,
                email=email,
                password=password,  # Optionally hash this
                mobile=mobile,
                role=role
            )

            return JsonResponse({'status': True, 'message': 'User registered successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': False, 'message': 'Only POST method allowed'}, status=405)



def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all().values(
            'id', 'username', 'email', 'mobile', 'is_verified', 'role'
        )
        user_list = list(users)  # Convert queryset to list of dicts
        return JsonResponse({'status': True, 'users': user_list}, status=200)
    else:
        return JsonResponse({'status': False, 'message': 'Only GET method allowed'}, status=405)