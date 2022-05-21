from post.serializers import (PostSerializer,PostListSerializer,PostDetailSerializer,
                              CommentCreateSerializer,LikePostSerialzer, UserSerializer)
from rest_framework.views import APIView
from django.contrib.auth.models import User
from post.models import UserFollowing
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,DestroyAPIView,ListAPIView, RetrieveAPIView, UpdateAPIView
from post.models import Post, Comment
from django.shortcuts import get_object_or_404

# Create your views here.
class GetUserDetailAPI(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_classes =UserSerializer
    def get(self,request):
        user_profile =User.objects.filter(id=request.user.id)
        serilizer =self.get_serializer(user_profile)
        return Response(serilizer.data)

class AddPostAPIView(APIView):
    """
    post:
        Creates a new post instance. Returns created post data
        parameters: [id, title, description, created_at]
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

class ListPostAPIView(ListAPIView):
    """
    get:
        Returns a list of all existing posts
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostRetrieveAPI(RetrieveAPIView):
    """
        get:
            Returns the details of a post instance. Searches post using slug field.
    """
    queryset = Post.objects.all()
    lookup_field = "id"
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

class PostDeleteAPI(DestroyAPIView):
    """
        delete:
            Delete an existing post
            parameters = [slug]
        """
    queryset = Post.objects.all()
    lookup_field = "id"
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

class LikePostAPI(UpdateAPIView):
    """
        post:
            add like the post
        """
    queryset = Post.objects.all()
    lookup_field = "id"
    serializer_class = LikePostSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    def post(self, request, id, *args, **kwargs):
        post =get_object_or_404(Post, pk=request.POST.get(pk=id))
        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)
        serializer = LikePostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

class UnLikePostAPI(UpdateAPIView):
    """
        post:
            add unlike the post
        """
    queryset = Post.objects.all()
    lookup_field = "id"
    serializer_class = LikePostSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    def post(self, request, id, *args, **kwargs):
        post =get_object_or_404(Post, pk=request.POST.get(pk=id))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        serializer = LikePostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

class CreateCommentAPI(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data
        parameters: [id,post,name, body, date_added]
    """
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Post, pk=id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

class UserFollow(APIView):
    def get_object(self,id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, id):
        user = request.user
        follow = self.get_object(id)
        UserFollowing.objects.create(user_id=user.id, following_user_id=follow.id)
        serializer = UserSerializer(follow)
        return Response(serializer.data)

class UserUnfollow(APIView):
    def get_object(self,id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, id):
        user = request.user
        follow = self.get_object(id)
        UserFollowing.objects.delete(user_id=user.id, following_user_id=follow.id)
        serializer = UserSerializer(follow)
        return Response(serializer.data)