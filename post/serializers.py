from django.contrib.auth.models import User
from rest_framework import serializers
from post.models import Post, Comment, UserFollowing

#  Create Post Serializer class here-----
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields =['id','title','desc','created_at',]

    def validate_title(self, value):
        if len(value) > 150:
            return serializers.ValidationError("Max title length is 100 characters")
        return value

# create Post detail serializer class here ------
class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =Post
        fields =['id','title','desc','created_at','likes','comments']

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj)
        try:
            serializer = CommentSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data

# create serializer class for list of all post ------
class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'desc', 'created_at','likes', 'comments']

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj).count()
        return qs

# create serilizer class for like a post
class LikePostSerialzer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields =['id','title','desc','created_at','likes']

# create serializer class for add comment in a post
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model =Comment
        fields =['id','post','name','body_text','date_added']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    following = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    followers = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'posts', 'following', 'followers','comments']

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj).count()
        return qs

class FollowersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['id', 'user_id', 'created']