import factory
from django.contrib.auth import get_user_model
from factory import Faker


class UserFactory(factory.django.DjangoModelFactory):
    """ User factory for default user model """
    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')

    class Meta:
        model = get_user_model()
