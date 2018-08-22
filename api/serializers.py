from rest_framework import serializers
from .fields import PrimaryKeyRelatedDictField
from .models import Store, Item, StoreCategory


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'

class StoreCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = StoreCategory
		fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
	menu_items = ItemSerializer(source="item_set", many=True)
	categories = PrimaryKeyRelatedDictField(many=True, queryset=StoreCategory.objects.all(), repr_serializer=StoreCategorySerializer)
	class Meta:
		model = Store
		fields = '__all__'
