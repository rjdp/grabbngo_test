from rest_framework import serializers

class PrimaryKeyRelatedDictField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.repr_serializer = kwargs.pop('repr_serializer', None)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        from django.core.exceptions import ObjectDoesNotExist
        if isinstance(data, dict):
            data = data.get('id')
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        if self.repr_serializer:
            return self.repr_serializer(value).data
        super().to_representation(value)