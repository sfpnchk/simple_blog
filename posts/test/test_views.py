from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from posts.models import Posts
from users.models import User


class HomePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        activated_user = User.objects.create(email='test1@test.com', password='test_pass2', is_active=True)

        published_Posts = Posts.objects.create(content='PUBLISHED posts by activated user',
                                               title='test', author=activated_user,
                                               status=Posts.PostStatus.PUBLISHED)
        unpublished_Posts = Posts.objects.create(content='UNPUBLISHED posts by activated user',
                                                 title='test', author=activated_user,
                                                 status=Posts.PostStatus.UNPUBLISHED)
        waiting_confirmation_Posts = Posts.objects.create(content='WAITING_CONFIRMATION posts by activated user',
                                                          title='test', author=activated_user,
                                                          status=Posts.PostStatus.WAITING_CONFIRMATION)

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/posts/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('posts:main'))
        self.assertEquals(resp.status_code, 200)

    def test_views_uses_correct_template(self):
        resp = self.client.get(reverse('posts:main'))
        self.assertTemplateUsed(resp, 'posts/home.html')

    def test_published_posts_from_activated_user_show(self):
        resp = self.client.get(reverse('posts:main'))
        self.assertContains(resp, 'PUBLISHED posts by activated user', status_code=200)

    def test_unpublished_posts_from_activated_user_not_show(self):
        resp = self.client.get(reverse('posts:main'))
        self.assertNotContains(resp, 'UNPUBLISHED posts by activated user', status_code=200)

    def test_wait_confirmation_posts_from_activated_user_not_show(self):
        resp = self.client.get(reverse('posts:main'))
        self.assertNotContains(resp, 'WAITING_CONFIRMATION posts by activated user', status_code=200)

    def test_pagination_on_1_posts_not_show(self):
        resp = self.client.get(reverse('posts:main'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['is_paginated'])

    def test_pagination_on_15_posts_show(self):
        activated_user = User.objects.create(email='testpagination@test.com', password='test_pass2', is_active=True)

        for i in range(15):
            posts = Posts.objects.create(content=f'PUBLISHED posts {i} by activated user',
                                         title='test', author=activated_user,
                                         status=Posts.PostStatus.PUBLISHED)
            posts.save()

        resp = self.client.get(reverse('posts:main'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'])

        self.assertEquals(len(resp.context['post_list']), 3)


class PostsDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        activated_user = User.objects.create(email='test1@test.com', password='test_pass2', is_active=True)

        published_posts = Posts.objects.create(content='PUBLISHED posts by activated user',
                                               title='test', author=activated_user,
                                               status=Posts.PostStatus.PUBLISHED)
        published_posts.save()

        waiting_confirmation_published_posts = Posts.objects.create(
            content='PUBLISHED WAITING_CONFIRMATION posts by activated user',
            title='test', author=activated_user,
            status=Posts.PostStatus.WAITING_CONFIRMATION)
        waiting_confirmation_published_posts.save()

        unpublished_posts = Posts.objects.create(content='PUBLISHED WAITING_CONFIRMATION posts by activated user',
                                                 title='test', author=activated_user,
                                                 status=Posts.PostStatus.WAITING_CONFIRMATION)
        unpublished_posts.save()

    def test_detail_page_status_code(self):
        resp = self.client.get('/posts/1/')
        self.assertEquals(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('posts:detail', kwargs={'pk': 1}))
        self.assertEquals(resp.status_code, 200)

    def test_views_uses_correct_template(self):
        resp = self.client.get(reverse('posts:detail', kwargs={'pk': 1}))
        self.assertTemplateUsed(resp, 'posts/post_detail.html')

    def test_view_on_nonexistent_posts(self):
        resp = self.client.get(reverse('posts:detail', kwargs={'pk': 999}))
        self.assertEquals(resp.status_code, 404)

    def test_comment_form_available(self):
        resp = self.client.get(reverse('posts:detail', kwargs={'pk': 1}))
        self.assertIsNotNone(resp.context['comment_form'])


class PostsCreateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='testcreate@test.com', password='test_pass2', is_active=True)
        posts = Posts.objects.create(content='PUBLISHED posts by activated user',
                                     title='test', author=user,
                                     status=Posts.PostStatus.PUBLISHED)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        call_command('create_default_groups')

    def test_detail_page_status_code_by_authorized_user(self):
        resp = self.client.get('/posts/create/')
        self.assertEquals(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('posts:create'))
        self.assertEquals(resp.status_code, 200)

    def test_views_uses_correct_template(self):
        resp = self.client.get(reverse('posts:create'))
        self.assertTemplateUsed(resp, 'posts/posts_create.html')

    def test_creation_posts_by_authorized_user(self):
        resp = self.client.post(reverse('posts:create'), {'title': 'test', 'content': 'testcontent'})
        self.assertRedirects(resp, '/posts/', status_code=302, target_status_code=200)

    def test_creation_posts_by_no_authorized_user(self):
        self.client.logout()
        resp = self.client.post(reverse('posts:create'), {'title': 'test', 'content': 'testcontent'})
        self.assertRedirects(resp, '/accounts/login/?next=/posts/create/', status_code=302, target_status_code=404)

    def test_posts_created_by_user_without_perms_not_show(self):
        resp = self.client.post(reverse('posts:create'), {'title': 'test', 'content': 'testcontent'}, follow=True)
        self.assertNotContains(resp, 'testcontent')

    def test_posts_created_by_user_from_groups_with_perms_show(self):
        self.user.groups.add(Group.objects.get(name='redactors'))
        resp = self.client.post(reverse('posts:create'),
                                {'title': 'test', 'content': 'test content from groups with perms'},
                                follow=True)

        self.assertContains(resp, 'test content from groups with perms')


class postsDeleteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_with_publication = User.objects.create(email='user_with_publication@test.com',
                                                    password='test_pass2',
                                                    is_active=True)
        redactor_user = User.objects.create(email='redactor_user@test.com', password='test_pass2', is_active=True)
        admin_user = User.objects.create(email='admin_user@test.com', password='test_pass2', is_active=True)

        call_command('create_default_groups')

    def setUp(self):
        self.user_with_publication = User.objects.get(email='user_with_publication@test.com')
        self.user_with_publication.groups.add(Group.objects.get(name='users'))

        self.redactor_user = User.objects.get(email='redactor_user@test.com')
        self.redactor_user.groups.add(Group.objects.get(name='redactors'))

        self.admin_user = User.objects.get(email='admin_user@test.com')
        self.admin_user.groups.add(Group.objects.get(name='admins'))

    def create_posts(self):
        posts = posts.objects.get_or_create(content='PUBLISHED posts by activated user',
                                            title='test from activated user', author=self.user_with_publication,
                                            status='PUBLISHED', id=1)

    def test_delete_from_not_authorized_user(self):
        self.create_posts()
        resp = self.client.post(reverse('posts:delete', kwargs={'pk': 1}))
        self.assertEquals(resp.status_code, 403)

    def test_delete_from_user_without_perm(self):
        self.create_posts()
        self.client.force_login(self.redactor_user)
        resp = self.client.post(reverse('posts:delete', kwargs={'pk': 1}))
        self.assertEquals(resp.status_code, 403)

    def test_delete_from_author(self):
        self.create_posts()
        self.client.force_login(self.user_with_publication)
        resp = self.client.post(reverse('posts:delete', kwargs={'pk': 1}))
        self.assertRedirects(resp, reverse('posts:main'))

    def test_delete_from_admin(self):
        self.create_posts()
        self.client.force_login(self.admin_user)
        resp = self.client.post(reverse('posts:delete', kwargs={'pk': 1}))
        self.assertRedirects(resp, reverse('posts:main'))

    def test_delete_not_exiting_posts(self):
        self.client.force_login(self.admin_user)
        resp = self.client.post(reverse('posts:delete', kwargs={'pk': 999}))
        self.assertEquals(resp.status_code, 404)


class postsUpdateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_with_publication = User.objects.create(email='user_with_publication@test.com', password='test_pass2',
                                                    is_active=True)
        redactor_user = User.objects.create(email='redactor_user@test.com', password='test_pass2', is_active=True)
        admin_user = User.objects.create(email='admin_user@test.com', password='test_pass2', is_active=True)
        posts = posts.objects.create(content='PUBLISHED posts by activated user',
                                     title='test', author=user_with_publication,
                                     status='PUBLISHED')

    def setUp(self):
        call_command('create_default_groups')

        self.user_with_publication = User.objects.get(email='user_with_publication@test.com')
        self.user_with_publication.groups.add(Group.objects.get(name='users'))

        self.redactor_user = User.objects.get(email='redactor_user@test.com')
        self.redactor_user.groups.add(Group.objects.get(name='redactors'))

        self.admin_user = User.objects.get(email='admin_user@test.com')
        self.admin_user.groups.add(Group.objects.get(name='admins'))

    def test_update_from_not_authorized_user(self):
        resp = self.client.post(reverse('posts:update', kwargs={'pk': 1}), {'title': 'updated_test_status',
                                                                            'content': 'sdfsdfsdcscs'})
        self.assertEquals(resp.status_code, 403)

    def test_update_from_user_without_perm(self):
        self.client.force_login(self.redactor_user)
        resp = self.client.post(reverse('posts:update', kwargs={'pk': 1}), {'title': 'updated_test_status',
                                                                            'content': 'sdfsdfsdcscs'})
        self.assertEquals(resp.status_code, 403)

    def test_update_from_author(self):
        self.client.force_login(self.user_with_publication)

    def test_delete_from_admin(self):
        self.client.force_login(self.admin_user)
        resp = self.client.post(reverse('posts:update', kwargs={'pk': 1}), {'title': 'updated_test_status',
                                                                            'content': 'sdfsdfsdcscs'})
        self.assertRedirects(resp, reverse('posts:detail', kwargs={'pk': 1}))

    def test_delete_not_exiting_posts(self):
        self.client.force_login(self.admin_user)
        resp = self.client.post(reverse('posts:update', kwargs={'pk': 155}), {'title': 'updated_test_status',
                                                                              'content': 'sdfsdfsdcscs'})
        self.assertEquals(resp.status_code, 404)
