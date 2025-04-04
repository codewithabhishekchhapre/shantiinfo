# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

def members(request):
    return HttpResponse("Hello world!")

def student(request):
     return HttpResponse("Hello student !")
def signup_page(request):
    template = loader.get_template('signup.html')
    return  HttpResponse(template.render());
 
def htmlpage(request):
    template = loader.get_template('new.html')
    return  HttpResponse(template.render());
def home(request):
    template = loader.get_template('index.html')
    return  HttpResponse(template.render());


userdata={
   
}

@csrf_exempt

def logindata(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        if userdata["email"]==email and userdata["password"]==password:
            
            return JsonResponse(
                {"is_login":"true",
                 "is_verified":"false",
                 "message":"Login Success"}
                )
        else:
            return JsonResponse(
                {"is_login":"false",
                 "is_verified":"false",
                 "message":"invalid email or password"}
                )
    
    return JsonResponse(
        {
            "is_login":"false",
            "is_verified":"false",
            "message":"invalid request"
        }
    )

@csrf_exempt

def signupdata(request):
    if request.method=="POST":
        name=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        userdata["username"]=name
        userdata["email"]=email
        userdata["password"]=password
        
        print(userdata)
        return HttpResponse(f"username is: and email is ")
    
    return HttpResponse("Invalid request")