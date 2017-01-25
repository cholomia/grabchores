from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from service.models import UserProfile
from service.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        serializer = UserSerializer(user, many=False)
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user, enable=True)
                if user_profile is not None:
                    return JsonResponse({'success': True, 'message': "Login Successful", 'user': serializer.data})
                else:
                    return JsonResponse({'success': False, 'message': "Email Address not yet validated"})
            except Exception as e:
                return JsonResponse({'success': False, 'message': "Email Address not yet validated"})
        else:
            return JsonResponse({'success': False, 'message': "Login Failed"})


class ValidationView(APIView):
    def get(self, request):
        try:
            user = User.objects.get(username=request.GET['username'])
            if user is not None:
                user_profile = UserProfile.objects.get(user=user, validation_code=request.GET['validation_code'])
                if user_profile is not None:
                    user_profile.enable = True
                    user_profile.save()
                    return JsonResponse({'success': True, 'message': "Email Validation Successful"})
                else:
                    return JsonResponse({'success': False, 'message': "Invalid Code"})
            else:
                return JsonResponse({'success': False, 'message': "Username does not exist"})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': "Invalid Validation"})
