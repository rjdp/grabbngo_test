import requests
import sys
from datetime import datetime
from io import BytesIO
import xlsxwriter
from django.http import StreamingHttpResponse
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from .models import Store
from .serializers import StoreSerializer, StoreCsvSerializer, ItemCsvSerializer, StoreCategorySerializer
from .utils import create_store_from_json
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

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



@api_view(['GET'])
def store_xlsx_view(request, uuid=None):
    if uuid:
        store = get_object_or_404(Store.objects.prefetch_related('item_set', 'categories'), uuid=uuid)
        
        output = BytesIO()
        xldoc = xlsxwriter.Workbook(output)
        worksheet_store = xldoc.add_worksheet('Store')
        worksheet_menu = xldoc.add_worksheet('Menu')
        worksheet_store_categories = xldoc.add_worksheet('Store Categories')


        store_header = {'uuid': 'UUID', 'title':'TITLE', 'categories':'CATEGORIES',
                'menu_items':'MENU ITEMS', 'hero_image_url':'HERO IMAGE URL', 'location':'LOCATION',
                'city':'CITY', 'currency':'CURRENCY'}

        menu_header = {'uuid':'UUID', 'title':'TITLE', 'description':'DESCRIPTION', 'image_url': 'IMAGE URL',
         'price': 'PRICE', 'store': 'STORE'}

        categories_header = {'uuid': 'UUID', 'name':'TITLE'}

        headers = [store_header, menu_header, categories_header]

        worksheets = [worksheet_store, worksheet_menu, worksheet_store_categories]

        serializers = [StoreCsvSerializer, ItemCsvSerializer, StoreCategorySerializer]

        obj_or_qsets = [store, store.item_set.all(), store.categories.all()]

        for header, worksheet, serializer, obj_or_qs in zip(headers, worksheets, serializers, obj_or_qsets):
            for i, col_name in enumerate(header.values()):
                worksheet.write(0, i, col_name)

            kwargs = {}

            if isinstance(obj_or_qs, QuerySet):
                kwargs['many'] = True

            data = serializer(obj_or_qs, **kwargs).data

            if kwargs.get('many'):
                for i, row_dict in enumerate(data):
                    for j, key in enumerate(header.keys()):
                        worksheet.write(i+1, j, row_dict.get(key, ''))
            else:
                for i, key in enumerate(header.keys()):
                    worksheet.write(1, i, data.get(key, ''))

        xldoc.close()
        response = StreamingHttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s-%s.xlsx' % (store.title, datetime.now(
        ).strftime('%Y/%m/%d-%H:%M:%S.%f'))
        return response
