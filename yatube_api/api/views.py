from rest_framework import viewsets

from posts.models import Comment, Group, Post
from posts.serializers import (CommentSerializer, GroupSerializer,
                               PostSerializer)

from .mixins import EditDeleteAuthorOnlyViewSetMixin


class PostViewSet(EditDeleteAuthorOnlyViewSetMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(EditDeleteAuthorOnlyViewSetMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        comments_queryset = Comment.objects.filter(post=post_id)
        return comments_queryset
