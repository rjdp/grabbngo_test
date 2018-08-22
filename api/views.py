import requests
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from .models import Store
from .serializers import StoreSerializer
from .utils import create_store_from_json

BASE_STORE_URL = 'https://www.ubereats.com/rtapi/eats/v2/eater-store/'

SAMPLE_STORE_UUID = '1f7228e3-f6b3-4be3-bea9-b4e48dae8b9e'

class StoreApiVew(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    queryset = Store.objects.prefetch_related('item_set', 'categories')
    serializer_class = StoreSerializer
    lookup_field = 'uuid'

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = self.queryset.get(**filter_kwargs)
        except Store.DoesNotExist:
            store_resp = requests.get(BASE_STORE_URL + filter_kwargs.get(self.lookup_field))
            if store_resp.status_code is not 200:
                raise Http404
            obj = create_store_from_json(store_resp.json())
            
        self.check_object_permissions(self.request, obj)

        return obj

    def get(self, request, *args, **kwargs):
        if self.lookup_field in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)