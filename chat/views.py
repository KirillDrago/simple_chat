from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination


from .models import Thread, Message
from .serializers import (
    ThreadSerializer,
    MessageSerializer,
    UserSerializer,
    ThreadRetrieveSerializer,
)


class ThreadPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = ThreadPagination

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user).order_by("-updated")


class ThreadCreateView(generics.CreateAPIView):
    serializer_class = ThreadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user)


class ThreadRetrieveView(generics.RetrieveAPIView):
    serializer_class = ThreadRetrieveSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        thread_id = self.kwargs["pk"]
        user = self.request.user
        try:
            thread = Thread.objects.get(pk=thread_id)
            if user in thread.participants.all():
                return Thread.objects.filter(pk=thread_id)
            else:
                raise Http404("You are not a member of this thread")
        except Thread.DoesNotExist:
            raise Http404("Thread not found")

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, Http404):
            response.data = {"detail": str(exc)}
        return response


class ThreadDeleteView(generics.DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadRetrieveSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MessagePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        thread_id = self.kwargs["pk"]
        return Message.objects.filter(thread_id=thread_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        thread_id = self.kwargs["pk"]
        serializer.save(thread_id=thread_id)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
