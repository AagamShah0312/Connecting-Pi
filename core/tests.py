from django.test import TestCase
from django.urls import reverse
from .forms import SkillForm
from .models import ChatMessage, HireRequest, Skill, User


class ConnectingPieFlowTests(TestCase):
    def setUp(self):
        self.provider = User.objects.create_user(username="maker", password="testpass123", role=User.Role.PROVIDER, first_name="Maya", degree="MSc Brand Strategy")
        self.other_provider = User.objects.create_user(username="builder", password="testpass123", role=User.Role.PROVIDER, first_name="Ravi")
        self.receptor = User.objects.create_user(username="learner", password="testpass123", role=User.Role.RECEPTOR, first_name="Lee")
        self.receptor.business_name = "Lee Learns Ltd"
        self.receptor.save(update_fields=("business_name",))
        self.skill = Skill.objects.create(provider=self.provider, name="Brand strategy", category="Business", description="Build a clear brand direction.", featured=True)

    def test_home_has_featured_skill(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brand strategy")

    def test_signup_page_renders_once(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Join Connecting Pi")
        self.assertEqual(response.content.count(b"Create your profile"), 1)

    def test_receptor_can_discover_skill_but_not_provider_directory(self):
        self.client.login(username="learner", password="testpass123")
        dashboard = self.client.get(reverse("dashboard"))
        self.assertContains(dashboard, "Brand strategy")
        self.assertRedirects(self.client.get(reverse("provider_directory")), reverse("dashboard"))

    def test_receptor_can_search_by_skill_or_category(self):
        Skill.objects.create(provider=self.other_provider, name="Python automation", category="Computer", description="Automate useful tasks.")
        self.client.login(username="learner", password="testpass123")
        response = self.client.get(reverse("dashboard"), {"q": "Computer"})
        self.assertContains(response, "Python automation")
        self.assertNotContains(response, "Brand strategy")

    def test_skill_form_does_not_expose_featured_checkbox(self):
        self.assertNotIn("featured", SkillForm().fields)

    def test_provider_can_see_other_providers(self):
        self.client.login(username="maker", password="testpass123")
        response = self.client.get(reverse("provider_directory"))
        self.assertContains(response, "Ravi")
        self.assertNotContains(response, "Lee")

    def test_profiles_show_role_specific_identity_fields(self):
        provider_response = self.client.get(reverse("profile", args=[self.provider.username]))
        receptor_response = self.client.get(reverse("profile", args=[self.receptor.username]))
        self.assertContains(provider_response, "MSc Brand Strategy")
        self.assertContains(receptor_response, "Lee Learns Ltd")

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
