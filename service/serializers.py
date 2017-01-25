from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail
from .models import UserProfile
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
                  + "http://grabchores.pythonanywhere.com/api/user/validation/?username=" + user.username
                  + "&validation_code=" + validation_code,
                  "grabchores@gmail.com", [user.email])
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'user_profile', 'password')
