from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Relation
from social.relation_fields import UserNameRelationField



def clean_email(value):
    """
    this method used for checking duplicate email
    """
    user = User.objects.filter(email=value)
    if 'admin' in value:
        raise serializers.ValidationError('admin word cant be in email!!')
    if user.exists():
        raise serializers.ValidationError('Email is already exists!!')
    return value

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': [clean_email], 'required': True},
        }

    def create(self, validated_data):

        """
         create method for register and create new user
        """

        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def validate_username(self, data):
        """
            this method used for check if admin word in username or not
        """

        if data == 'admin':
            raise serializers.ValidationError('username cant be admin!!')
        return data

    def validate(self, data):
        """
            this method used for checking password and confirm password matches
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords are not matches!!')
        return data


class RelationSerializer(serializers.ModelSerializer):
    from_user = UserNameRelationField(read_only=True)
    to_user = UserNameRelationField(read_only=True)
    class Meta:
        model = Relation
        fields = '__all__'
