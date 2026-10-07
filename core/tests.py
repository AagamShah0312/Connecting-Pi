from django.test import TestCase
from django.urls import reverse
from .models import ChatMessage, HireRequest, Skill, User


class ConnectingPieFlowTests(TestCase):
    def setUp(self):
        self.provider = User.objects.create_user(username="maker", password="testpass123", role=User.Role.PROVIDER, first_name="Maya", degree="MSc Brand Strategy")
        self.other_provider = User.objects.create_user(username="builder", password="testpass123", role=User.Role.PROVIDER, first_name="Ravi")
        self.receptor = User.objects.create_user(username="learner", password="testpass123", role=User.Role.RECEPTOR, first_name="Lee")
        self.skill = Skill.objects.create(provider=self.provider, name="Brand strategy", category="Business", description="Build a clear brand direction.", featured=True)

    def test_home_has_featured_skill(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brand strategy")

    def test_receptor_can_discover_skill_but_not_provider_directory(self):
        self.client.login(username="learner", password="testpass123")
        dashboard = self.client.get(reverse("dashboard"))
        self.assertContains(dashboard, "Brand strategy")
        self.assertRedirects(self.client.get(reverse("provider_directory")), reverse("dashboard"))

    def test_provider_can_see_other_providers(self):
        self.client.login(username="maker", password="testpass123")
        response = self.client.get(reverse("provider_directory"))
        self.assertContains(response, "Ravi")
        self.assertNotContains(response, "Lee")

    def test_receptor_can_send_one_hire_request(self):
        self.client.login(username="learner", password="testpass123")
        response = self.client.post(reverse("hire_skill", args=[self.skill.pk]), {"message": "I want to sharpen my launch plan."})
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(HireRequest.objects.filter(skill=self.skill, receptor=self.receptor).exists())

    def test_provider_can_accept_request(self):
        hire_request = HireRequest.objects.create(skill=self.skill, receptor=self.receptor, message="Please help me learn.")
        self.client.login(username="maker", password="testpass123")
        response = self.client.get(reverse("update_request", args=[hire_request.pk, "accept"]))
        self.assertRedirects(response, reverse("dashboard"))
        hire_request.refresh_from_db()
        self.assertEqual(hire_request.status, HireRequest.Status.ACCEPTED)

    def test_only_request_participants_can_chat(self):
        hire_request = HireRequest.objects.create(skill=self.skill, receptor=self.receptor, message="Please help me learn.")
        self.client.login(username="learner", password="testpass123")
        response = self.client.post(reverse("chat", args=[hire_request.pk]), {"body": "Can we discuss the scope and price?"})
        self.assertRedirects(response, reverse("chat", args=[hire_request.pk]))
        self.assertTrue(ChatMessage.objects.filter(hire_request=hire_request, sender=self.receptor).exists())
