from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user_with_phone_number(self):
        """Test creating a user with only phone_number, first_name, last_name, and password"""
        user = self.User.objects.create_user(
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            password='testpassword123'
        )
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('testpassword123'))

    def test_phone_number_is_username_field(self):
        """Test that phone_number is used as the username field"""
        user = self.User.objects.create_user(
            phone_number='0987654321',
            first_name='Jane',
            last_name='Doe',
            password='password321'
        )
        self.assertEqual(user.phone_number, '0987654321')
        self.assertEqual(user.USERNAME_FIELD, 'phone_number')

    def test_create_user_without_phone_number_raises_error(self):
        """Test creating a user without a phone_number raises an error"""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                phone_number=None,
                first_name='John',
                last_name='Doe',
                password='password'
            )

    def test_create_user_with_duplicate_phone_number(self):
        """Test that creating a user with a duplicate phone_number raises an IntegrityError"""
        self.User.objects.create_user(
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            password='testpassword123'
        )
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                phone_number='1234567890',  # Duplicate phone number
                first_name='Jane',
                last_name='Smith',
                password='password123'
            )
