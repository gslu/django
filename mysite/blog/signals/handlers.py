#coding:utf-8

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from blog.models import Profile,PostClass,Post,Book



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Post)
def create_postclass(sender, instance, created, **kwargs):
    if created:
        PostClass.objects.create(post=instance,user=instance.author)


@receiver(post_save, sender=Post)
def save_postclass(sender, instance, **kwargs):
    try:
        instance.postclass.save()
    except:
        PostClass.objects.create(post=instance,user=instance.author)



#@receiver(post_save,sender=Profile,dispatch_uid="profile_post_save")
#def on_delete(sender,**kwargs):
#    print kwargs
#    patch = kwargs['instance']
#    print patch
#    print dir(patch.image)


