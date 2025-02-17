from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.users.tests.factories.models_factories import UserFactory


class UserTestCase(TestCase):
    """ Testing the default user model"""
    def setUp(self):
        self.user = UserFactory()

    def test_user_creation(self):
        user = get_user_model().objects.create_user(username='testuser', email='test@example.com',
                                                    password='defaultpassword')
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('defaultpassword'))

    def test_change_user_fields(self):
        # Todo add more fields
        new_first_name = 'NewName'
        new_middle_name = 'NewLastName'
        self.user.first_name = 'NewName'
        self.user.last_name = 'NewLastName'
        self.user.save()
        updated_user = self.user.__class__.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, new_first_name)
        self.assertEqual(updated_user.last_name, new_middle_name)
