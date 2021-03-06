from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class City(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=15)
    category = models.ForeignKey(Category)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sub-Categories"

    def __str__(self):
        return self.name


class AccountProfile(models.Model):
    user = models.OneToOneField('auth.User')
    preferred_cities = models.ManyToManyField(City)

    def __str__(self):
        return self.user.username


class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    level = models.IntegerField()
    trainer = models.ForeignKey('auth.User')
    categories = models.ForeignKey(SubCategory, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads')
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Pokemon'

    def __str__(self):
        return self.name


@receiver(post_save, sender='auth.User')
def create_account_profile(sender, **kwargs):
    user_instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        AccountProfile.objects.create(user=user_instance)
        Token.objects.create(user=user_instance)

