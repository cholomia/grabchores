from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail
from .models import UserProfile, Classification, Job, JobApplication
import uuid


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_profile = UserProfileSerializer(many=False, read_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        my_uuid = uuid.uuid4()
        validation_code = str(my_uuid)
        user_profile = UserProfile.objects.create(
            user=user,
            validation_code=validation_code,
            enable=False,
        )
        user_profile.save()
        send_mail("Grab Chores Validation",
                  "Please validate your account using the link: "
                  + "http://192.168.1.6:8000/api/user/validation/?username=" + user.username
                  + "&validation_code=" + validation_code,
                  "grabchores@gmail.com", [user.email])
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'user_profile', 'password')


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    classification_id = serializers.ReadOnlyField(source='classification.id')
    classification_title = serializers.ReadOnlyField(source='classification.title')
    apply = serializers.SerializerMethodField()
    open = serializers.SerializerMethodField()
    my_status = serializers.SerializerMethodField()

    def get_apply(self, obj):
        try:
            job_application = JobApplication.objects.get(user=self.context['request'].user, job=obj)
            return job_application is not None
        except Exception as e:
            return False

    def get_open(self, obj):
        try:
            job_application = JobApplication.objects.get(accept=True, job=obj)
            return job_application is None
        except Exception as e:
            return True

    def get_my_status(self, obj):
        try:
            accept = JobApplication.objects.get(user=self.context['request'].user, job=obj).accept
            return accept
        except Exception as e:
            return False

    class Meta:
        model = Job
        fields = ('id', 'username', 'classification_id', 'classification_title', 'title', 'description', 'created',
                  'date_start', 'date_end', 'fee', 'location', 'apply', 'open', 'my_status')


class JobApplicationSerializer(serializers.ModelSerializer):
    job_obj = JobSerializer(source='job', read_only=True)

    class Meta:
        model = JobApplication
        fields = ('id',)
