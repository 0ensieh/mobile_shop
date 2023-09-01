from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from extensions.utils import jalali_converter
from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from .models import Post, Comment
from django.utils import timezone
from . import views
from .forms import CommentForm, SearchForm, FlatPageForm
from .models import Comment, Post


# unit test for models:
class BlogModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            image='path/to/image.jpg',
            author=self.user,
            body='This is a test post body.',
            publish=timezone.now(),
            status=Post.Status.PUBLISHED
        )
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            title='Test Comment',
            email='test@example.com',
            body='This is a test comment body.',
            created=timezone.now(),
            active=True
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_comment_str(self):
        expected_str = f'{self.user.get_full_name()} ---> {self.post}'
        self.assertEqual(str(self.comment), expected_str)

    def test_post_jpublish(self):
        expected_jalali_date = jalali_converter(self.post.publish)
        self.assertEqual(self.post.jpublish(), expected_jalali_date)

    def test_comment_jcreated(self):
        expected_jalali_date = jalali_converter(self.comment.created)
        self.assertEqual(self.comment.jcreated(), expected_jalali_date)

    def test_post_get_absolute_url(self):
        url = self.post.get_absolute_url()
        expected_url = reverse('blog:post_detail', args=[
            self.post.publish.year,
            self.post.publish.month,
            self.post.publish.day,
            self.post.slug
        ])
        self.assertEqual(url, expected_url)

    def test_published_manager(self):
        # Test if the PublishedManager returns only published posts
        published_posts = Post.published.all()
        self.assertEqual(len(published_posts), 1)
        self.assertEqual(published_posts[0], self.post)

    def test_comment_active_default(self):
        # Test if the default value of the 'active' field in Comment is False
        new_comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            title='Another Test Comment',
            email='another@example.com',
            body='This is another test comment body.',
            created=timezone.now()
        )
        self.assertFalse(new_comment.active)


# unit test for urls:

class BlogUrlsTest(SimpleTestCase):
    
    def test_post_list_url_resolves(self):
        url = reverse('blog:post_list')
        self.assertEqual(resolve(url).func, views.post_list)

    def test_post_list_by_tag_url_resolves(self):
        url = reverse('blog:post_list_by_tag', args=['tag-slug'])
        self.assertEqual(resolve(url).func, views.post_list)

    def test_post_detail_url_resolves(self):
        url = reverse('blog:post_detail', args=[2023, 8, 22, 'post-slug'])
        self.assertEqual(resolve(url).func, views.post_detail)

    def test_post_comment_url_resolves(self):
        url = reverse('blog:post_comment', args=[1])  # You can pass a valid post ID here
        self.assertEqual(resolve(url).func, views.post_comment)


# unit test for forms:
class CommentFormTest(TestCase):

    def test_valid_comment_form(self):
        form_data = {'title': 'Test Title', 'email': 'test@example.com', 'body': 'Test body'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form_data = {'title': 'Test Title', 'email': 'invalid-email', 'body': 'Test body'}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

class SearchFormTest(TestCase):

    def test_valid_search_form(self):
        form_data = {'query': 'search query'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

class FlatPageFormTest(TestCase):

    def test_valid_flat_page_form(self):
        form_data = {'title': 'Test Title', 'body': 'Test body', 'publish': '2023-08-22', 'slug': 'test-slug'}
        form = FlatPageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_flat_page_form(self):
        form_data = {'title': 'Test Title', 'body': 'Test body', 'publish': 'invalid-date', 'slug': 'test-slug'}
        form = FlatPageForm(data=form_data)
        self.assertFalse(form.is_valid())
