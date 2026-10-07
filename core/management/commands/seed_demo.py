from django.core.management.base import BaseCommand
from core.models import Skill, User


PROVIDERS = [
    ("Aarav", "Shah", "aarav-shah", "MSc Computer Science", "Bengaluru", "Python automation", "Computer"),
    ("Maya", "Patel", "maya-patel", "MBA Marketing", "Mumbai", "Brand strategy", "Business"),
    ("Rohan", "Mehta", "rohan-mehta", "BFA Visual Design", "Pune", "Visual identity", "Design"),
    ("Sara", "Khan", "sara-khan", "MA English", "Delhi", "Creative writing", "Writing"),
    ("Dev", "Iyer", "dev-iyer", "BTech Electronics", "Chennai", "Arduino prototyping", "Technology"),
    ("Nisha", "Rao", "nisha-rao", "MSc Data Science", "Hyderabad", "Data storytelling", "Data"),
    ("Kabir", "Singh", "kabir-singh", "LLB", "Jaipur", "Contract basics", "Legal"),
    ("Anika", "Verma", "anika-verma", "MA Psychology", "Lucknow", "Interview coaching", "Career"),
    ("Ishaan", "Das", "ishaan-das", "BArch", "Kolkata", "Space planning", "Architecture"),
    ("Tara", "Joshi", "tara-joshi", "MCom Finance", "Ahmedabad", "Personal budgeting", "Finance"),
    ("Vikram", "Nair", "vikram-nair", "BSc Nutrition", "Kochi", "Meal planning", "Wellness"),
    ("Meera", "Kapoor", "meera-kapoor", "MA Sociology", "Chandigarh", "Community building", "Community"),
    ("Aditya", "Gupta", "aditya-gupta", "MTech Cloud Computing", "Noida", "Cloud foundations", "Technology"),
    ("Kiara", "Malhotra", "kiara-malhotra", "BA Film Studies", "Mumbai", "Short film editing", "Film"),
    ("Arjun", "Bose", "arjun-bose", "MDes Interaction Design", "Kolkata", "UX research", "Design"),
    ("Pia", "Menon", "pia-menon", "BSc Biology", "Thiruvananthapuram", "Science tutoring", "Education"),
    ("Yash", "Sethi", "yash-sethi", "BCA", "Gurugram", "No-code products", "Technology"),
    ("Ira", "Chopra", "ira-chopra", "MA History", "Delhi", "Research methods", "Education"),
    ("Neel", "Kulkarni", "neel-kulkarni", "BFA Photography", "Nashik", "Street photography", "Photography"),
    ("Riya", "Bhat", "riya-bhat", "MSc Statistics", "Mysuru", "Spreadsheet modeling", "Data"),
    ("Manav", "Ahuja", "manav-ahuja", "BBA Entrepreneurship", "Amritsar", "Pitch storytelling", "Business"),
    ("Zoya", "Ali", "zoya-ali", "MA Fashion Design", "Hyderabad", "Textile illustration", "Craft"),
    ("Om", "Prasad", "om-prasad", "BTech Mechanical", "Nagpur", "3D printing", "Making"),
    ("Aisha", "Roy", "aisha-roy", "MA Journalism", "Kolkata", "Podcast production", "Media"),
    ("Karan", "Pillai", "karan-pillai", "MCA", "Bengaluru", "Web accessibility", "Technology"),
    ("Lavanya", "Mishra", "lavanya-mishra", "MPhil Economics", "Bhopal", "Decision economics", "Finance"),
    ("Sahil", "Dutta", "sahil-dutta", "BA Music", "Goa", "Home recording", "Music"),
    ("Jhanvi", "Saxena", "jhanvi-saxena", "MS Human Resources", "Indore", "People operations", "Career"),
    ("Reyansh", "Goyal", "reyansh-goyal", "BSc Physics", "Surat", "Robotics basics", "Making"),
    ("Noor", "Thomas", "noor-thomas", "MA Public Policy", "Kochi", "Policy writing", "Writing"),
]


class Command(BaseCommand):
    help = "Create 30 varied demo service providers and one skill for each."

    def handle(self, *args, **options):
        created_count = 0
        for first_name, last_name, username, degree, location, skill_name, category in PROVIDERS:
            provider, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": f"{username}@connectingpi.local",
                    "role": User.Role.PROVIDER,
                    "degree": degree,
                    "location": location,
                    "bio": f"I enjoy helping people make progress with {skill_name.lower()}.",
                },
            )
            if created:
                provider.set_password("demo12345")
                provider.save()
                created_count += 1
            else:
                provider.role = User.Role.PROVIDER
                provider.degree = degree
                provider.location = location
                provider.save(update_fields=("role", "degree", "location"))

            Skill.objects.get_or_create(
                provider=provider,
                name=skill_name,
                defaults={
                    "category": category,
                    "description": f"Learn practical {skill_name.lower()} with a clear, friendly starting point.",
                    "featured": False,
                },
            )

        self.stdout.write(self.style.SUCCESS(f"Ready: {len(PROVIDERS)} providers. Created {created_count} new accounts."))
