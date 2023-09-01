from django.test import TestCase, Client
from django.urls import reverse
from order.models import Address
from django.contrib.auth import get_user_model
from .forms import ProfileForm, SignUpForm, UserChangeForm
from django.urls import reverse, resolve
from . import views

User = get_user_model()  # To handle custom User model


# unit test for models:

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

    def test_create_user(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertFalse(self.user.is_admin)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
        )
        self.assertIsInstance(superuser, User)
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.get_full_name(), 'Admin User')

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'John Doe')

    def test_has_perm(self):
        self.assertTrue(self.user.has_perm('any_permission'))

    def test_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms('any_app_label'))

    def test_is_staff(self):
        self.assertFalse(self.user.is_staff)


# unit test for views:
class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client = Client()
        self.client.login(email='test@example.com', password='testpassword')

    def test_profile_view(self):
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')  


class ProfileAddressViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client = Client()
        self.client.login(email='test@example.com', password='testpassword')
        self.address = Address.objects.create(user=self.user, title='Home Address')

    def test_profile_address_view(self):
        response = self.client.get(reverse('account:profile_address'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home Address') 


class ProfileAddressCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client = Client()
        self.client.login(email='test@example.com', password='testpassword')

    def test_profile_address_create_view(self):
        response = self.client.post(reverse('account:profile_address_create'), {'title': 'New Address'})
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Address.objects.filter(user=self.user, title='New Address').exists())


# unit test for forms:
class ProfileFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'ssn': '123456789',
        }
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid_email',
            'phone_number': '1234567890',
            'ssn': '123456789',
        }
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())


class SignUpFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatch',
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())


class UserChangeFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(
            email='john@example.com',
            password='testpassword',
        )
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'new_email@example.com',
            'phone_number': '1234567890',
            'ssn': '123456789',
            'wallet_amount': 100,
            'is_active': True,
            'is_admin': True,
            'is_superuser': True,
            'password': 'newpassword',
        }
        form = UserChangeForm(data=data, instance=user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = User.objects.create_user(
            email='john@example.com',
            password='testpassword',
        )
        data = {
            'email': 'invalid_email',
        }
        form = UserChangeForm(data=data, instance=user)
        self.assertFalse(form.is_valid())


# unit test for urls:

class AccountUrlsTest(TestCase):
    def test_profile_url_resolves(self):
        url = reverse('account:profile')
        self.assertEqual(resolve(url).func.view_class, views.Profile)

    def test_profile_address_url_resolves(self):
        url = reverse('account:profile_address')
        self.assertEqual(resolve(url).func.view_class, views.ProfileAddress)

    def test_profile_address_create_url_resolves(self):
        url = reverse('account:profile_address_create')
        self.assertEqual(resolve(url).func.view_class, views.ProfileAddressCreate)

    def test_profile_address_update_url_resolves(self):
        url = reverse('account:profile_address_update')
        self.assertEqual(resolve(url).func.view_class, views.ProfileAddressUpdate)

    def test_profile_order_url_resolves(self):
        url = reverse('account:profile_order')
        self.assertEqual(resolve(url).func, views.profile_order)

    def test_profile_order_detail_url_resolves(self):
        url = reverse('account:profile_order_detail', args=[1])  # Use a valid order pk here
        self.assertEqual(resolve(url).func, views.profile_order_detail)

    def test_profile_personal_info_url_resolves(self):
        url = reverse('account:profile_personal_info')
        self.assertEqual(resolve(url).func.view_class, views.ProfilePersonalInfo)

    def test_profile_comment_url_resolves(self):
        url = reverse('account:profile_comment')
        self.assertEqual(resolve(url).func, views.profile_comment)

    def test_comment_delete_url_resolves(self):
        url = reverse('account:comment_delete', args=[1])  # Use a valid comment pk here
        self.assertEqual(resolve(url).func, views.comment_delete)

