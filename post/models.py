from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title =models.CharField(max_length=150, unique=True)
    desc =models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)
    likes =models.ManyToManyField(User, related_name='like_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(parent=instance)
        return qs

class Comment(models.Model):
    post =models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    body_text =models.TextField()
    date_added =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s-%s' %(self.post.title,self.name)


class UserFollowing(models.Model):
    user_id = models.ForeignKey('auth.User', related_name='following', on_delete=models.SET_NULL, null=True, blank=True)
    following_user_id = models.ForeignKey('auth.User', related_name='followers', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name='unique_following')
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_id} is following {self.following_user_id}'