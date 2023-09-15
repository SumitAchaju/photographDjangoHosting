from django.urls import path,re_path
from Follow.views import UserFriend,FriendPosts,UserFollowFollowing,FriendSuggestion,AddFriend,RemoveFriend
from Account.views import RegisterView,UpdateProfile,ChangePassword
from Post.views import PostCategory,SinglePost,AddComment,DeleteComment,PostLikes,PostLikesOut,UserPost,UploadPost,UpdatePost,DeletePost,PostSaved
from More.views import Feedback,ImproveSugg
from chat.views import ChatMessage,LatestMessage,msg_seen,UnSeenMsg


urlpatterns = [
    path("friend/",UserFriend),
    path("friendposts/",FriendPosts),
    path("register/",RegisterView.as_view()),
    path("categoryposts/<pk>",PostCategory),
    path("singlepost/<pk>",SinglePost),
    path("addcomment/<pk>",AddComment),
    path("deletecomment/<pk>",DeleteComment),
    path("postlike/<pk>",PostLikes),
    path("postlikeout/<pk>",PostLikesOut),
    path("userpost/<pk>",UserPost),
    path("userfollowfollowing/<pk>",UserFollowFollowing),
    path("followsuggestion/",FriendSuggestion),
    path("addfriend/<pk>",AddFriend),
    path("removefriend/<pk>",RemoveFriend),
    path("updateprofile/",UpdateProfile),
    path("changepassword/",ChangePassword),
    path("uploadpost/",UploadPost),
    path("updatepost/<pk>",UpdatePost),
    path("deletepost/<pk>",DeletePost),
    path("savedpost/",PostSaved),
    path("improvesuggestion/",ImproveSugg),
    path("feedback/",Feedback),
    re_path(r"chatmessage/(?P<friend_id>\w+)/$",ChatMessage.as_view()),
    re_path(r"latest_message/",LatestMessage.as_view()),
    path("message_seen/<msg_id>",msg_seen),
    path("unseen_msg/",UnSeenMsg.as_view()),
]