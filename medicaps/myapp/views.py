# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import EmployeeProfile
import json
from .models import User

import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=email,
        subject='Your OTP Code',
        plain_text_content=f'Your OTP code is: {otp}',
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"SendGrid Error: {e}")
        return None

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


@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"message": "Email and password are required"}, status=400)

        try:
            user = User.objects.get(email=email, password=password)
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "mobile": user.mobile,
                "role": user.role,
                "is_verified": user.is_verified,
            }
            return JsonResponse({"message": "Login successful", "user": user_data}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "Invalid email or password"}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "Server error", "error": str(e)}, status=500)

def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all().values(
            'id', 'username', 'email', 'mobile', 'is_verified', 'role'
        )
        user_list = list(users)  # Convert queryset to list of dicts
        return JsonResponse({'status': True, 'users': user_list}, status=200)
    else:
        return JsonResponse({'status': False, 'message': 'Only GET method allowed'}, status=405)
    
    
@csrf_exempt
def create_employee_profile(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            bio = request.POST.get('bio')
            company_name = request.POST.get('company_name')
            position = request.POST.get('position')
            experience = request.POST.get('experience')
            tech = request.POST.get('tech')
            image = request.FILES.get('image')
            print(experience,tech,position,bio,company_name)
            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            profile, created = EmployeeProfile.objects.get_or_create(user=user)
            profile.bio = bio
            profile.company_name = company_name
            profile.position = position
            profile.experience = experience
            profile.tech = tech
            if image:
                profile.image = image
            profile.save()

            return JsonResponse({'message': 'Employee profile saved successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_employee_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = EmployeeProfile.objects.get(user=user)
        data = {
            'name': user.username,
            'email': user.email,
            'bio': profile.bio,
            'company_name': profile.company_name,
            'position': profile.position,
            'experience': str(profile.experience),
            'tech': profile.tech,
            'image_url': profile.image.url if profile.image else ''
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except EmployeeProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"message": "Email is required"}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message": "User does not exist"}, status=404)

            otp = generate_otp()
            status = send_otp_email(email, otp)

            if status == 202:
                return JsonResponse({"message": "OTP sent successfully"})
            else:
                return JsonResponse({"message": "Failed to send OTP"}, status=500)

        except Exception as e:
            return JsonResponse({"message": "Error", "error": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)