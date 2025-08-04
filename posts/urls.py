from django.urls import path, include
from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import TokenObtainPairView

from posts.views import UserViewSet, PostViewSet, CommentViewSet


router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('', include(router.urls)),
]
