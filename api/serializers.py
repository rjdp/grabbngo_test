from rest_framework import serializers
from .fields import PrimaryKeyRelatedDictField
from .models import Store, Item, StoreCategory


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'

class ItemCsvSerializer(ItemSerializer):
	store = serializers.CharField(source="store.title")


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

class StoreCsvSerializer(StoreSerializer):
	categories = serializers.SerializerMethodField()
	menu_items = serializers.SerializerMethodField()
	location = serializers.SerializerMethodField()

	def get_location(self, obj):
		return obj.location.get('address').get('formattedAddress')

	def get_categories(self, obj):
		return ', '.join(obj.categories.values_list('name', flat=True))

	def get_menu_items(self, obj):
		return ', '.join(obj.item_set.values_list('title', flat=True))