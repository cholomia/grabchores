import django_filters
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from service.models import UserProfile, Classification, Job, JobApplication, UserRating
from service.permissions import IsOwnerOrReadOnly
from service.serializers import UserSerializer, ClassificationSerializer, JobSerializer, JobApplicationSerializer, \
    UserRatingSerializer


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


class ProfileUpdateView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            user_profile = UserProfile.objects.get(user=request.user)
            if user is not None and user_profile is not None:
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                user_profile.mobile_number = request.POST['mobile_number']
                user_profile.save()
                serializer = UserSerializer(user, many=False)
                return JsonResponse({'success': True, 'message': "Update Profile Successful", 'user': serializer.data})
            else:
                return JsonResponse({'success': False, 'message': "Error Retrieving User/User Profile"})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': "Error Updating Profile"})


class ChangePasswordView(APIView):
    def post(self, request):
        valid_user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if valid_user is not None:
            user = User.objects.get(username=request.POST['username'])
            user.set_password = request.POST['new_password']
            user.save()
            return JsonResponse({'success': True, 'message': "Change Password Successful"})
        else:
            return JsonResponse({'success': False, 'message': "Invalid Authentication"})


class ApplicationAcceptView(APIView):
    def post(self, request):
        try:
            user = request.user
            job_application = JobApplication.objects.get(id=request.POST['id'])
            if user is not None and job_application is not None:
                if user == job_application.job.user:
                    job_application.accept = request.POST['accept']
                    job_application.save()
                    serializer = JobApplicationSerializer(job_application, many=False)
                    message = "Job Application Accepted" if job_application.accept \
                        else "Job Application Acceptance Canceled"
                    return JsonResponse({'success': True, 'message': message, 'applicant': serializer.data})
                else:
                    return JsonResponse({'success': False, 'message': "Unauthorized Access to Application"})
            else:
                return JsonResponse({'success': False, 'message': "Invalid User/Job Application"})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': "Error Updating Application"})


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    pagination_class = None


class JobFilter(django_filters.rest_framework.FilterSet):
    username = django_filters.CharFilter(name="user__username")

    class Meta:
        model = Job
        fields = ['username', 'classification']


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    filter_class = JobFilter
    search_fields = ('title', 'description')
    ordering = ('-created',)

    def get_queryset(self):
        queryset = Job.objects.all()
        if self.request.query_params.get('open', False):
            queryset = Job.objects.exclude(
                id__in=JobApplication.objects.filter(accept=True).values_list('job_id', flat=True))
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobApplicationFilter(django_filters.rest_framework.FilterSet):
    job_id = django_filters.NumberFilter(name="job__id")

    class Meta:
        model = JobApplication
        fields = ["job_id"]


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = JobApplicationFilter
    ordering = ('created',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRatingAvailFilter(django_filters.rest_framework.FilterSet):
    rate_username = django_filters.CharFilter(name="rate_user__username")

    class Meta:
        model = UserRating
        fields = ['rate_username', 'type', ]


class UserRatingViewSet(viewsets.ModelViewSet):
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = UserRatingAvailFilter
    ordering = ('-created',)

    def perform_create(self, serializer):
        rate_user = User.objects.get(username=self.request.POST['rate_username'])
        serializer.save(user=self.request.user, rate_user=rate_user)
