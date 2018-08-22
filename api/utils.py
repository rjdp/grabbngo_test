import collections
from .serializers import StoreSerializer, ItemSerializer, StoreCategorySerializer

def create_store_from_json(json_data):
	json_store = json_data['store']

	category_data  = [{'name': category['name'], 'key': category['keyName'], 'uuid': category['uuid'] }
		for category in json_store['categories']]
	category_serializer = StoreCategorySerializer(data=category_data, many=True)
	if category_serializer.is_valid():
		store_categories = category_serializer.save()


		store_data = {'uuid': json_store['uuid'], 'city': json_store['cityName'], 'title': json_store['title'],
			'currency': json_store['currencyCode'], 'hero_image_url': json_store['heroImageUrl'],
			'location': json_store['location'], 'categories':[{'id': cat.id} for cat in store_categories]}
		digits_after_decimal = json_store['currencyNumDigitsAfterDecimal']
		store_serializer = StoreSerializer(data=store_data)
		if store_serializer.is_valid():
			store = store_serializer.save()


			items_list = [ {'store': store.id, 'price': item['price']/(10**digits_after_decimal),
							'title': item['title'], 'image_url':item.get('imageUrl', ''),
							'uuid': item['uuid'], 'description': item.get('itemDescription', '')} for item in collections.ChainMap(*tuple(x['itemsMap']
							for x in json_store['sectionEntitiesMap'].values())).values()]

			item_serializer = ItemSerializer(data= items_list, many=True)
			if item_serializer.is_valid():
				item_serializer.save()

			return store








