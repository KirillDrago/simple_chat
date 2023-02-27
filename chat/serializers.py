from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from .models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ("id", "participants", "created", "updated", "last_message")

    # Get the last message in the thread
    def get_last_message(self, obj):
        """
        Returns the last message of the thread.
        """
        last_message = obj.messages.order_by("-created").first()
        if last_message:
            return MessageSerializer(last_message).data

    # Create a new thread
    def create(self, validated_data):
        """
        Creates a new thread or returns an existing one if a thread with the same
        participants already exists.
        """
        with transaction.atomic():
            members = validated_data.pop("participants")
            participants = [
                User.objects.get(id=member.id).id for member in members
            ]
            thread = Thread.objects.filter(
                participants=participants[0]
            ).filter(participants=participants[1])
            if thread.exists():
                return thread.first()
            else:
                thread = Thread.objects.create()
                thread.participants.set(participants)
                return thread

    # Validate the participants of the thread
    def validate_participants(self, attrs):
        """
        Validates that there are only two participants and the requesting user is one of them.
        """
        request = self.context.get("request")
        user = request.user

        # Ensure that there are exactly two participants
        if len(attrs) != 2:
            raise serializers.ValidationError(
                "Thread have only two participants."
            )
        # Ensure that the current user is one of the participants
        if user not in attrs:
            raise serializers.ValidationError(
                "You should choose yourself to create a thread"
            )
        return attrs


class ThreadRetrieveSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ("id", "messages")

    def get_messages(self, obj):
        thread_id = obj.id
        messages = Message.objects.filter(thread_id=thread_id)
        return MessageSerializer(messages, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "sender", "text", "thread", "created", "is_read")
        read_only_fields = ("id", "thread", "sender", "is_read", "created")

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["sender"] = self.validate_sender(request.user)
        thread = Thread.objects.get(
            id=request.parser_context.get("kwargs")["pk"]
        )
        validated_data["thread"] = self.validate_thread(thread)
        return super().create(validated_data)

    # Validate the sender of the message
    def validate_sender(self, value):
        """
        Validate the sender of the message.
        This method checks if the sender is allowed to send messages on behalf of other users.
        """
        request = self.context.get("request")
        if request and request.user != value:
            raise serializers.ValidationError(
                "You are not allowed to send messages on behalf of other users."
            )
        return value

    # Validate the thread of the message
    def validate_thread(self, thread):
        """
        Validate the thread of the message.
        This method checks if the message is being sent to a thread that the user is a participant of.
        """
        request = self.context.get("request")
        user = request.user
        if user not in thread.participants.all():
            raise serializers.ValidationError(
                "You can't send a message to a thread you're not a participant of."
            )
        return thread


class UserSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "unread_messages"]

    def get_unread_messages(self, user):
        """Calculate and return the number of unread messages for the user."""
        unread_messages = (
            Message.objects.filter(thread__participants=user, is_read=False)
            .exclude(sender=user)
            .count()
        )
        return unread_messages
