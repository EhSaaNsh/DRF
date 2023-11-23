from rest_framework import status
from django.contrib.auth.models import User
from . models import Relation
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserRegisterSerializer, RelationSerializer
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.

class APIRegisterView(APIView):
    """
        used for register new account
        parameters: str:username, str:password, str:confirm password

    """
    def post(self, request):
        srz_data = UserRegisterSerializer(data=request.POST)
        if srz_data.is_valid():
            srz_data.create(validated_data=srz_data.validated_data)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)



class UserFollowView(APIView):
    """
            used for follow a user
            parameter: int:user_id
    """
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            return Response({'error': 'you already follow this user'}, status=status.HTTP_403_FORBIDDEN)
        else:
            Relation(from_user=request.user, to_user=user).save()
            return Response({'message': 'successfully followed'}, status=status.HTTP_200_OK)


class UserUnFollowView(APIView):
    """
        used for unfollow a user
        parameter =  int:user_id
    """
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            return Response({'message': 'successfully unfollowed'}, status=status.HTTP_200_OK)
        return Response({'error': 'you are not following this user'}, status=status.HTTP_400_BAD_REQUEST)


class UserFollowingListView(APIView):
    """
        to get list of user followings
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = [RelationSerializer,]

    def get(self, request):
        result = request.user.followers
        srz_data = RelationSerializer(instance=result, many=True)
        followings = []
        for fo in srz_data.data:
            followings.append(fo['to_user'])
        return Response({'followings': followings}, status=status.HTTP_200_OK)


class UserFollowersListView(APIView):
    """
    to get list of user followers
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = [RelationSerializer, ]
    def get(self, request):
        result = request.user.following
        srz_data = RelationSerializer(instance=result, many=True)
        followers = []
        for fo in srz_data.data:
            followers.append(fo['from_user'])
        return Response({'followers': followers}, status=status.HTTP_200_OK)