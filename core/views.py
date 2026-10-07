from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ChatMessageForm, HireRequestForm, SignUpForm, SkillForm
from .models import ChatMessage, HireRequest, Skill, User


def home(request):
    featured_skills = Skill.objects.select_related("provider").filter(featured=True)[:3]
    return render(request, "home.html", {"featured_skills": featured_skills})


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.role == User.Role.PROVIDER:
        skills = request.user.skills.all()
        requests = HireRequest.objects.filter(skill__provider=request.user).select_related("skill", "receptor")
        return render(request, "dashboard.html", {"skills": skills, "requests": requests, "is_provider": True})
    recommendations = Skill.objects.select_related("provider").annotate(request_count=Count("hire_requests")).order_by("-featured", "-request_count")[:8]
    sent_requests = request.user.sent_requests.select_related("skill", "skill__provider")
    return render(request, "dashboard.html", {"recommendations": recommendations, "sent_requests": sent_requests, "is_provider": False})


@login_required
def provider_directory(request):
    if request.user.role != User.Role.PROVIDER:
        return redirect("dashboard")
    providers = User.objects.filter(role=User.Role.PROVIDER).exclude(pk=request.user.pk).prefetch_related("skills")
    return render(request, "providers.html", {"providers": providers})


def profile(request, username):
    provider = get_object_or_404(User.objects.prefetch_related("skills"), username=username, role=User.Role.PROVIDER)
    return render(request, "profile.html", {"provider": provider})


@login_required
def create_skill(request):
    if request.user.role != User.Role.PROVIDER:
        return HttpResponseForbidden("Only service providers can create skills.")
    form = SkillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        skill = form.save(commit=False)
        skill.provider = request.user
        skill.save()
        messages.success(request, "Your skill is now live in the Pie.")
        return redirect("dashboard")
    return render(request, "skill_form.html", {"form": form})


@login_required
def hire_skill(request, skill_id):
    if request.user.role != User.Role.RECEPTOR:
        return HttpResponseForbidden("Only service receptors can send hire requests.")
    skill = get_object_or_404(Skill.objects.select_related("provider"), pk=skill_id)
    form = HireRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        hire_request, created = HireRequest.objects.get_or_create(skill=skill, receptor=request.user, defaults={"message": form.cleaned_data["message"]})
        if not created:
            form.add_error(None, "You already sent a request for this skill.")
        else:
            messages.success(request, f"Your request was sent to {skill.provider.get_full_name() or skill.provider.username}.")
            return redirect("dashboard")
    return render(request, "hire_form.html", {"skill": skill, "form": form})


@login_required
def update_request(request, request_id, action):
    if request.user.role != User.Role.PROVIDER:
        return HttpResponseForbidden("Only service providers can update requests.")
    hire_request = get_object_or_404(HireRequest.objects.select_related("skill"), pk=request_id, skill__provider=request.user)
    if action not in ("accept", "decline"):
        raise Http404
    hire_request.status = HireRequest.Status.ACCEPTED if action == "accept" else HireRequest.Status.DECLINED
    hire_request.save(update_fields=("status",))
    messages.success(request, f"Request {hire_request.status}.")
    return redirect("dashboard")


@login_required
def chat(request, request_id):
    hire_request = get_object_or_404(
        HireRequest.objects.select_related("skill", "skill__provider", "receptor"),
        Q(skill__provider=request.user) | Q(receptor=request.user),
        pk=request_id,
    )
    is_provider = hire_request.skill.provider_id == request.user.id
    form = ChatMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        message = form.save(commit=False)
        message.hire_request = hire_request
        message.sender = request.user
        message.save()
        return redirect("chat", request_id=hire_request.id)
    return render(request, "chat.html", {
        "hire_request": hire_request,
        "chat_messages": hire_request.chat_messages.select_related("sender"),
        "form": form,
        "is_provider": is_provider,
    })
