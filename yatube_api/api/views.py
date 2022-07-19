from posts.models import Comment, Group, Post
from rest_framework import viewsets
from rest_framework.permissions import (SAFE_METHODS,
                                        BasePermission,
                                        IsAuthenticated)

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class EditDeleteOnlyAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [EditDeleteOnlyAuthor & IsAuthenticated]
    queryset = (
        Post.objects
        .select_related('author', 'group')
        .prefetch_related('comments')
    )
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [EditDeleteOnlyAuthor & IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        comments_queryset = Comment.objects.filter(post=post_id)
        return comments_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
