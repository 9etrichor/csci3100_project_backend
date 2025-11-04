from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, min_length=6)
  class Meta:
    model = User
    fields = ['username', 'password', 'score']

  def create(self, validated_data):
    user = User.objects.create_user(
      username = validated_data["username"],
      password = validated_data["password"],
      score = validated_data.get('score', 0)
    )
    return user

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)