from django.core.management.base import BaseCommand
from listings.models import Listing, User
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        # Create a host user if not exists
        host, created = User.objects.get_or_create(
            username='host1',
            defaults={
                'email': 'host1@example.com',
                'role': 'host',
                'first_name': 'Host',
                'last_name': 'User',
                'password': 'password123',
            }
        )

        if created:
            host.set_password('password123')
            host.save()
            self.stdout.write(self.style.SUCCESS(f"Created host user: {host.username}"))

        # Create sample listings
        for i in range(5):
            listing, _ = Listing.objects.get_or_create(
                title=f"Sample Listing {i+1}",
                defaults={
                    'description': 'A beautiful place to stay.',
                    'location': random.choice(['Cairo', 'Alexandria', 'Giza']),
                    'price_per_night': random.randint(50, 300),
                    'host': host,
                    'created_at': timezone.now()
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Added listing: {listing.title}"))