from django.urls import path
from post import views
from rest_framework_simplejwt.views import (TokenObtainPairView,)

urlpatterns =[
    path('token/',TokenObtainPairView.as_view(),name='user_authenticate'),  # POST request
    path('follow/<int:id>/',views.UserFollow.as_view(),name='user_follow'),  # POST request
    path('unfollow/<int:id>',views.UserUnfollow.as_view(),name='user_unfollow'),  # POST request
    path('user/',views.GetUserDetailAPI.as_view(),name='user_profile'),  # GET request
    path('posts/',views.AddPostAPIView.as_view(),name='new_post'),  # POST request
    path('del_posts/<int:id>/',views.PostDeleteAPI.as_view(),name='delete_post'),  # DELETE request
    path('like/<int:id>/',views.LikePostAPI.as_view(),name='like_post'),  # POST request
    path('unlike/<int:id>/',views.UnLikePostAPI.as_view(),name='unlike_post'),  # POST request
    path('comment<int:id>',views.CreateCommentAPI.as_view(),name='comment_post'),  # POST request
    path('post_detail/<int:id>/',views.PostRetrieveAPI.as_view(),name='post_detail'),  # GET request
    path('all_posts/',views.ListPostAPIView.as_view(),name='view_all_post'),  # GET request
]