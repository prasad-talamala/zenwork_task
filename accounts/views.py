import json
import os

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views.decorators.csrf import csrf_exempt

from zenwork.settings import BASE_DIR
from .models import UserProfile
from rest_framework.authtoken.models import Token
from tika import parser
from pathlib import Path

from accounts.forms import RegistrationForm


def home(request):
    if request.user.is_authenticated:
        messages.warning(request, "User logged in. please logout and try login!")
        return redirect('profile')
    return render(request, "home.html")


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = request.POST.copy()
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        p1 = data.get("password1")
        p2 = data.get("password2")

        if p1 == p2:
            password = p1
            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                username=username, password=password)
                user.save()

                user_profile = UserProfile.objects.create(user_id=user.id)
                user_profile.save()

                token = Token.objects.get(user=user).key
                data.update({"token": token})

                messages.success(request, 'Registration Successful.')
                return redirect("login")

            except Exception as e:
                messages.error(request, str(e))

        else:
            messages.error(request, 'Passwords didnt Match.')

    if request.user.is_authenticated:
        messages.warning(request, "User logged in. please logout and try login!")
        return redirect('profile')

    context = {
        'form': RegistrationForm(),
    }

    return render(request, "register.html", context=context)


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        token = Token.objects.get(user=user).key

        if user is None:
            messages.error(request, 'Invalid Login Credentials')
        else:
            auth_login(request, user)
            messages.success(request, 'Login Successful')
            return redirect("profile")

    if request.user.is_authenticated:
        messages.warning(request, "User logged in. please logout and try login!")
        return redirect('profile')

    context = {
        'form': AuthenticationForm(),
    }

    return render(request, "login.html", context=context)


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'Successfully Logged Out!')
    return redirect("home")


@csrf_exempt
@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_obj = User.objects.get(id=request.user.id)
    if request.method == "POST":

        if request.POST["first_name"]:
            user_obj.first_name = request.POST["first_name"]
        if request.POST["last_name"]:
            user_obj.last_name = request.POST["last_name"]
        if request.POST["email"]:
            user_obj.email = request.POST["email"]

        user_obj.save()

        if request.POST["address_line_1"]:
            user_profile.address_line_1 = request.POST["address_line_1"]
        if request.POST["address_line_2"]:
            user_profile.address_line_2 = request.POST["address_line_2"]
        if request.POST["city"]:
            user_profile.city = request.POST["city"]
        if request.POST["state"]:
            user_profile.state = request.POST["state"]
        if request.POST["pin_code"]:
            user_profile.pin_code = request.POST["pin_code"]

        user_profile.save()

        messages.success(request, "Profile Updated!")
    return render(request, 'profile.html', {'user_data': user_obj, 'user_profile': user_profile})


@csrf_exempt
def get_profile(request):
    auth_token = json.loads(request.body)['token']
    user_obj = User.objects.get(auth_token=auth_token)
    user_profile = UserProfile.objects.get(user=user_obj)

    user_details = {
        "id": user_obj.id,
        "username": user_obj.username,
        "first_name": user_obj.first_name,
        "last_name": user_obj.last_name,
        "email": user_obj.email,
        "address_line_1": user_profile.address_line_1,
        "address_line_2": user_profile.address_line_2,
        "city": user_profile.city,
        "state": user_profile.state,
        "pincode": user_profile.pin_code,
        "auth_token": auth_token
    }
    return JsonResponse(user_details, safe=False)


def crawl_pdf(request):
    if request.method == "POST":
        url = request.POST.get("pdf_url")
        name = "a"                       # url.split("/")[-1].split(".")[0]
        filename = Path(os.path.join(BASE_DIR) + '/static/files/{}.pdf'.format(name))

        if url:
            response = requests.get(url)
            filename.write_bytes(response.content)

        if filename:
            parsed_data = parser.from_file(str(filename))
            metadata = parsed_data["metadata"]
            content = parsed_data['content'].split(".")

            context = {
                # 'pdf_name': name.capitalize(),
                'metadata': metadata.items(),
                'content': content
            }
            return render(request, "crawl_pdf.html", context=context)

    return render(request, "crawl_pdf.html")
