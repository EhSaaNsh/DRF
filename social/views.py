from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer, VoteSerializer
from . models import Post, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly


# Create your views here.

class PostsView(APIView):
    """
    used for get list of all posts
    """
    serializer_class = [PostSerializer,]
    def get(self, request):
        posts = Post.objects.all()
        srz = PostSerializer(instance=posts, many=True)
        return Response(srz.data, status.HTTP_200_OK)


class CreatePostView(APIView):
    """
    used for create a new post

    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = [PostSerializer, ]
    def post(self, request):
        srz_data = PostSerializer(data=request.POST)
        if srz_data.is_valid():
            slug = slugify(srz_data.validated_data['body'][:30])
            Post.objects.create(user=request.user, slug=slug, body=srz_data.validated_data['body'])
            return Response({'message': 'post created successfully'}, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    used for get detail of a post
    parameters = int:post_id
    """
    serializer_class = [PostSerializer, ]
    permission_classes = [IsAuthenticated, ]
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        srz_data = PostSerializer(instance=post)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class UpdatePostView(APIView):
    """
    used for update a post, request user most be owner of the post
    parameters= int:post_id
    """
    permission_classes = [IsOwnerOrReadOnly,]
    serializer_class = [PostSerializer, ]
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        srz_data = PostSerializer(instance=post, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response({'message': 'post updated successfully'}, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_403_FORBIDDEN)


class DeletePostView(APIView):

    """
    used for delete a post, request user most be owner of the post
    parameters= int:post_id
    """
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = [PostSerializer,]
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({'message': 'post deleted successfully'})


class CommentAddToPostView(APIView):
    """
    used for add a comment on a post
    parameters = int:post_id
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = [CommentSerializer, ]

    def post(self, request, post_id):
        post_instance = get_object_or_404(Post, pk=post_id)
        srz_data = CommentSerializer(data=request.POST)
        if srz_data.is_valid():
            validate = srz_data.validated_data
            print(srz_data.data)
            Comment(user=request.user, post=post_instance, body=validate['body']).save()
            return Response({'message': 'comment add successfully'}, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class AddReplyToCommentView(APIView):
    """
    used for add a reply to a comment
    parameters = int:post_id, int:comment_id
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = [CommentSerializer, ]

    def post(self, request, post_id, comment_id):
        post_instance = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        srz_data = CommentSerializer(data=request.POST)
        if srz_data.is_valid():
            Comment(user=request.user, post=post_instance, reply=comment,
                    body=srz_data.validated_data['body'], is_reply=True).save()
            return Response({'message': 'reply add successfully'}, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeView(APIView):
    """
    used for like a post
    parameters = int:post_id
    """
    permission_classes = [IsAuthenticated, ]
    def get(self, request, post_id):
        post_instance = get_object_or_404(Post, pk=post_id)
        vote = Vote.objects.filter(user=request.user, post=post_instance)
        if vote.exists():
            return Response({'error': 'you liked this post before!!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Vote(user=request.user, post=post_instance).save()
            return Response({'message': 'post liked successfully'}, status=status.HTTP_201_CREATED)



