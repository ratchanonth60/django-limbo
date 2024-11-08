import factory
from django.db.models.signals import post_delete, post_save, pre_save
from factory.django import DjangoModelFactory, mute_signals

from .user import UserFactory


class BaseFactory(DjangoModelFactory):
    updated_by = factory.SubFactory(UserFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_at = factory.Faker("date_time")
    created_at = factory.Faker("date_time")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        with mute_signals(pre_save, post_save, post_delete):
            return super()._create(model_class, *args, **kwargs)

    @classmethod
    def update_instance(cls, instance, **kwargs):
        with mute_signals(pre_save, post_save, post_delete):
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

    @classmethod
    def delete_instance(cls, instance):
        with mute_signals(pre_save, post_save, post_delete):
            instance.delete()
