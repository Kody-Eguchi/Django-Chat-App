from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from .models import Profile

# Whenever a new User is saved (created), automatically create a corresponding Profile object.


@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwarges):
    user = instance

    if created:
        Profile.objects.create(
            user=user,
        )
    else:
        try:
            email_address = EmailAddress.objects.get_primary(user)
            if email_address.email != user.email:
                email_address.email = user.email
                email_address.verified = False
                email_address.save()
        except:
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                primary=True,
                verified=False
            )


@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

# @receiver(post_save, sender=User)
# → Listens for the post_save signal on the User model (after it's saved).

# created
# → A boolean that’s True only when the user is created (not just updated).

# instance
# → The actual User instance that was saved.
