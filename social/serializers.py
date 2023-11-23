from rest_framework import serializers
from .models import Post, Comment, Vote
from . relation_fields import UserNameRelationField


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()
    user = UserNameRelationField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'slug': {'required': False},
            'user': {'required': False}
        }

    def get_comments(self, obj):
        result = obj.pcomments.all()
        return CommentSerializer(instance=result, many=True).data

    def get_votes(self, obj):
        result = obj.pvotes.all()
        return VoteSerializer(instance=result, many=True).data



class CommentSerializer(serializers.ModelSerializer):
    user = UserNameRelationField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'post': {'required': False},
            'body': {'required': True}
        }


class VoteSerializer(serializers.ModelSerializer):
    user = UserNameRelationField(read_only=True)
    class Meta:
        model = Vote
        fields = '__all__'

