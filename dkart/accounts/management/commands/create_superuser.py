from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        User.objects.create_superuser(
            username='dhyey',
            email='dhyeykakadiya1015@gmail.com',
            password='dhyey1015'
        )
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
