from rest_framework import serializers

from locations.models import Location
from .models import User


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._loc = self.initial_data.pop('location')
        self._role = self.initial_data['role']
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        loc, _ = Location.objects.get_or_create(name=self._loc,
                                                defaults={'lat': 0, 'lng': 0})
        user.set_password(validated_data["password"])
        user.location = loc
        if self._role.lower() == 'admin' or self._role.lower() == 'moderator':
            user.is_staff = True

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    location = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['password', 'role']

    def is_valid(self, *, raise_exception=False):
        self._loc = self.initial_data.pop('location')
        self._role = self.initial_data['role']
        super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        loc, _ = Location.objects.get_or_create(name=self._loc,
                                                defaults={'lat': 0, 'lng': 0})
        user.location = loc
        if self._role.lower() == 'admin' or self._role.lower() == 'moderator':
            user.is_staff = True
        else:
            user.is_staff = False

        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
