from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('created the user profile')
    else:
        # profile = UserProfile.objects.get(user=instance)
        # profile.save()
        # print('user is updated')
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)  
            print('userprofile does not exist but I created One') 
             
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username,'this user is being saved')
    # pass    
# post_save.connect(post_save_create_profile_receiver, sender=User) 