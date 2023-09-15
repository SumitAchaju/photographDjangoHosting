from rest_framework.routers import DefaultRouter
from Account.views import UserViewSet
from Post.views import PostViewSet,CategoryViewSet
from Follow.views import AllFriendsViewSet

router = DefaultRouter()
router.register('user',UserViewSet)
router.register('Post',PostViewSet)
router.register('Allfriends',AllFriendsViewSet)
router.register('postcategory',CategoryViewSet)
