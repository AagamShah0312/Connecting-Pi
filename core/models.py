from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    class Role(models.TextChoices):
        PROVIDER = "provider", "Service provider"
        RECEPTOR = "receptor", "Service receptor"

    role = models.CharField(max_length=20, choices=Role.choices)
    degree = models.CharField(max_length=160, blank=True)
    business_name = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    avatar_initials = models.CharField(max_length=4, blank=True)

    def save(self, *args, **kwargs):
        if not self.avatar_initials:
            self.avatar_initials = "".join(part[0] for part in self.get_full_name().split()[:2]).upper() or self.username[:2].upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})


class Skill(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills", limit_choices_to={"role": User.Role.PROVIDER})
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="Other")
    description = models.TextField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created_at"]

    def __str__(self):
        return f"{self.name} by {self.provider.get_full_name() or self.provider.username}"


class HireRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="hire_requests")
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests", limit_choices_to={"role": User.Role.RECEPTOR})
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["skill", "receptor"], name="one_request_per_skill_receptor")]

    def __str__(self):
        return f"{self.receptor.username} -> {self.skill.name}"


class ChatMessage(models.Model):
    hire_request = models.ForeignKey(HireRequest, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message from {self.sender.username} on request {self.hire_request_id}"
