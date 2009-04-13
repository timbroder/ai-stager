from django.test import TestCase
from stager.staging.models import Project, Client, Category
from django.contrib.auth.models import User


class ProjectTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('testclient', 'lennon@thebeatles.com', 'password')
        user.is_staff = True
        user.save()
        self.user1 = User.objects.create(username="test", password="test")
        self.client1 = Client.objects.create(name="project1", user=self.user1)
        self.project1 = Project.objects.create(name="project1", client=self.client1)
        self.category = Category.objects.create(name="Test/Category", project=self.project1)

    def testDefaultCategory(self):
        self.assertEquals(self.project1.default_category, 'testcategory')

    def testLoginToAdmin(self):
        login = self.client.login(username='testclient', password='password')
        self.failUnless(login, 'Could not log in')
