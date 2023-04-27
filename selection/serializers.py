from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ads.models import Ad
from .models import Selection
from ads.serializers import AdSerializer


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True, read_only=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Ad.objects.all(),
        many=True
    )

    def create(self, validated_data):
        items = validated_data.pop('items')
        selection = Selection.objects.create(**validated_data)
        for item in items:
            obj = get_object_or_404(Ad, pk=item.id)
            selection.items.add(obj)

        selection.owner = self.context['request'].user

        selection.save()
        return selection

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    items = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Ad.objects.all(),
        many=True
    )

    def is_valid(self, *, raise_exception=False):
        self._items = self.initial_data.pop('items')
        super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        selection = super().save()
        for item in self._items:
            obj = get_object_or_404(Ad, pk=item)
            selection.items.add(obj)

        if self.context['request'].user != self.initial_data['owner']:
            selection.owner = self.context['request'].user

        selection.save()
        return selection

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id']
