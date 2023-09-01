from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from account.models import User
from shop.models import Category, Product, Image, Property, Description, TechnicalDescription, Banner, Comment, Contact
from .forms import ContactForm, CommentForm, PostForm, ColorForm

# unit test for models:
class ShopModelsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.product = Product.objects.create(
            title='Test Product',
            english_name='Test Product EN',
            category=self.category,
            slug='test-product',
            brand='Test Brand',
            guarantee=1,
            price=100,
            discount=10,
            discount_time=timezone.now(),
            delivery=3
        )
        self.image = Image.objects.create(product=self.product, image='path_to_image.png')
        self.property = Property.objects.create(product=self.product, title='Test Property', detail='Property Detail')
        self.description = Description.objects.create(product=self.product, title='Test Description', detail='Description Detail')
        self.technical_description = TechnicalDescription.objects.create(product=self.product, title='Test Technical Description')
        self.banner = Banner.objects.create(image='path_to_banner_image.png', link='http://example.com', title='Test Banner')
        self.comment = Comment.objects.create(
            product=self.product,
            user=self.user,
            title='Test Comment',
            email='test@example.com',
            description='Test comment description',
            created_on=timezone.now(),
            status='accepted',
            offer_vote=True
        )
        self.contact = Contact.objects.create(
            subject='PROPOSAL',
            name='Test User',
            email='test@example.com',
            phone=1234567890,
            message='Test contact message'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_image_str(self):
        self.assertEqual(str(self.image), 'Test Product')

    def test_property_str(self):
        self.assertEqual(str(self.property), 'Test Property')

    def test_description_str(self):
        self.assertEqual(str(self.description), 'Test Description')

    def test_technical_description_str(self):
        self.assertEqual(str(self.technical_description), 'Test Technical Description')

    def test_banner_str(self):
        self.assertEqual(str(self.banner), 'Test Banner')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f'Comment by {self.user.username} on {self.product}')

    
    def test_category_absolute_url(self):
        expected_url = reverse('shop:product_list_by_category', args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), expected_url)

    def test_product_get_price_after_discount(self):
        self.product.discount_time = timezone.now() + timezone.timedelta(days=1)
        self.assertEqual(self.product.get_price_after_discount(), Decimal(90))

    def test_product_get_price_after_discount_expired(self):
        self.product.discount_time = timezone.now() - timezone.timedelta(days=1)
        self.assertEqual(self.product.get_price_after_discount(), Decimal(100))

   
    def test_product_get_absolute_url(self):
        expected_url = reverse('shop:product_detail', kwargs={'id': self.product.id, 'slug': self.product.slug})
        self.assertEqual(self.product.get_absolute_url(), expected_url)

   

class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.product = Product.objects.create(
            title='Test Product',
            english_name='Test Product',
            category=Category.objects.create(title='Test Category', slug='test-category'),
            slug='test-product',
            brand='Test Brand',
            guarantee=1,
            available=True,
            price=100,
            discount=10,
            discount_time=timezone.now() + timezone.timedelta(days=7),
            delivery=2
        )
        self.comment = Comment.objects.create(
            product=self.product,
            user=self.user,
            title='Test Comment',
            email='test@example.com',
            description='This is a test comment',
            created_on=timezone.now(),
            status='accepted',
            offer_vote=True
        )

    def test_accepted_manager(self):
        accepted_comments = Comment.accepted.all()
        self.assertIn(self.comment, accepted_comments)

    def test_status_choices(self):
        status_choices = dict(Comment.STATUS)
        self.assertIn(self.comment.status, status_choices)


class ContactModelTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            subject='PROPOSAL',
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            message='This is a test message'
        )

    def test_subject_choices(self):
        subject_choices = dict(Contact.CHOICES)
        self.assertIn(self.contact.subject, subject_choices)


# unit test for views 
class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('shop:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/home.html')

    def test_search_list_view(self):
        response = self.client.get(reverse('shop:search'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/search_list.html')

    def test_product_list_by_category_view(self):
        category = Category.objects.create(title='Test Category', slug='test-category')
        response = self.client.get(reverse('shop:product_list_by_category', kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list_by_category.html')

    def test_product_offer_list_view(self):
        response = self.client.get(reverse('shop:product_offer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_offer_list.html')

    def test_contact_view(self):
        response = self.client.get(reverse('shop:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/contact.html')

        # Test submitting the contact form
        post_data = {
            'subject': 'PROPOSAL',
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'message': 'Test message',
        }
        response = self.client.post(reverse('shop:contact'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirect after form submission
        self.assertRedirects(response, reverse('shop:contact'))  # Redirect to the same page
   

# unit test for forms:
class FormsTestCase(TestCase):
    def test_contact_form_valid(self):
        form_data = {
            'subject': 'PROPOSAL',
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'message': 'Test message',
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_valid(self):
        form_data = {
            'title': 'Test Title',
            'email': 'john@example.com',
            'description': 'Test description',
            'offer_vote': True,
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_valid(self):
        form_data = {
            'content': 'Test content',
        }
        form = PostForm(data=form_data)

    def test_contact_form_invalid(self):
        form_data = {
            'subject': 'PROPOSAL',
            'name': 'John Doe',
            'email': 'invalid-email',  # Invalid email format
            'phone': '1234567890',
            'message': 'Test message',
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_comment_form_empty_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_color_form_valid(self):
        form_data = {
            'color': 'red',
        }
        form = ColorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_color_form_invalid(self):
        form_data = {
            'color': '',
        }
        form = ColorForm(data=form_data)



# integration test for models:
class ModelIntegrationTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='TestCategory', slug='test-category')
        self.product = Product.objects.create(title='TestProduct', category=self.category, 
                                              english_name='test', slug='testslug', brand='testbrand', 
                                              guarantee=3, available=True, price=100, discount=4, 
                                              discount_time=timezone.now(), delivery=4)

    def test_category_product_relation(self):
        self.assertEqual(self.category.products.count(), 1)
        self.assertEqual(self.category.products.first(), self.product)

    def test_product_discount(self):
        self.product.discount = 20
        self.product.discount_time = timezone.now() + timezone.timedelta(days=1)
        self.product.save()

        self.assertEqual(self.product.get_discount(), 20.0)
        self.assertEqual(self.product.get_price_after_discount(), 80)

    def test_comment_creation(self):
        user = User.objects.create(username='testuser')
        comment = Comment.objects.create(product=self.product, user=user, title='Test Comment', description='Test Description')
        
        self.assertEqual(comment.product, self.product)
        self.assertEqual(comment.user, user)

    def test_contact_creation(self):
        contact_data = {
            'subject': 'Test Subject',
            'name': 'Test Name',
            'email': 'test@example.com',
            'phone': '1234567890',
            'message': 'Test Message',
        }
        contact = Contact.objects.create(**contact_data)

        self.assertEqual(contact.subject, contact_data['subject'])
        self.assertEqual(contact.name, contact_data['name'])
        self.assertEqual(contact.email, contact_data['email'])
        self.assertEqual(contact.phone, contact_data['phone'])
        self.assertEqual(contact.message, contact_data['message'])
 