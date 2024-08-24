from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Client

# Signal handler that creates a Client instance whenever a new User is created
@receiver(post_save, sender=User)
def create_client(instance, created, **kwargs):
    if created:
        # Create a Client object associated with the new User
        Client.objects.get_or_create(
            user=instance,  # Associate the Client with the created User instance
            defaults={
                'name': instance.username,  # Set the Client's name to the User's username
                'email': instance.email,  # Set the Client's email to the User's email
            }
        )
