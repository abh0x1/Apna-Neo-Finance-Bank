import random
from django.contrib.auth.models import AbstractUser
from django.db import models
import os
import uuid
from django.db.models.signals import pre_save, post_delete

from django.dispatch import receiver

ACCOUNT_PLANS = [
    ('queen', 'Queen'),
    ('king', 'King'),
    ('knight', 'Knight'),
]

ACCOUNT_TYPES = [
    ('savings', 'Savings'),
    ('current', 'Current'),
]

RESIDENCY_STATUS = [
    ('indian', 'Indian'),
    ('nri', 'NRI'),
]

MARITAL_STATUS = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
]

OCCUPATIONS = [
    ('student', 'Student'),
    ('employee', 'Employee'),
    ('business', 'Business'),
    ('other', 'Other'),
]



def generate_account_number():
    while True:
        number = random.randint(180000000000, 189999999999)
        if not CustomUser.objects.filter(account_number=number).exists():
            return number



def generate_virtual_card():
    return random.randint(18180000000000, 18189999999999)  # total 14 digits


def user_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    folder_name = f"{instance.username}_{instance.mobile}"
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(folder_name, 'profile_images', filename)

def user_kyc_path(instance, filename):
    ext = filename.split('.')[-1]
    folder_name = f"{instance.username}_{instance.mobile}"
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(folder_name, 'kyc_docs', filename)



class CustomUser(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, default='single')
    occupation = models.CharField(max_length=15, choices=OCCUPATIONS, default='student')
    account_plan = models.CharField(max_length=10, choices=ACCOUNT_PLANS, default='queen')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='savings')
    residency_status = models.CharField(max_length=10, choices=RESIDENCY_STATUS, default='indian')
    account_number = models.BigIntegerField(default=generate_account_number, unique=True)
    virtual_card_number = models.BigIntegerField(default=generate_virtual_card, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    profile_image = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True)
    kyc_doc = models.FileField(upload_to=user_kyc_path, null=True, blank=True)
    city = models.CharField(max_length=100, blank=False)
    ifsc_code = models.CharField(max_length=11, blank=True, unique=True)
    upi_id = models.CharField(max_length=50, blank=True, unique=True)

    def generate_ifsc(self):
        import string, random
        while True:
            code = self.city[:3].upper() + ''.join(random.choices(string.digits, k=7))
            if not CustomUser.objects.filter(ifsc_code=code).exists():
                return code
            
    def save(self, *args, **kwargs):
        from django.db import IntegrityError, transaction
        if not self.upi_id:
            self.upi_id = f"{self.username.lower()}@anfb"

        if not self.ifsc_code:
            if not self.city:
                raise ValueError("City is required to generate IFSC code")
            self.ifsc_code = self.generate_ifsc()

        super().save(*args, **kwargs)

    @property
    def is_adult(self):
        import datetime
        if self.dob:
            today = datetime.date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age >= 18
        return False
    
# from django.db.models.signals import pre_save, post_delete
# from django.dispatch import receiver

# # Delete old file when updating profile image
# @receiver(pre_save, sender=CustomUser)
# def auto_delete_profile_image_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return False
    
#     try:
#         old_user = CustomUser.objects.get(pk=instance.pk)
#     except CustomUser.DoesNotExist:
#         return False
    
#     # Check if profile image has changed
#     if old_user.profile_image and old_user.profile_image != instance.profile_image:
#         # Delete the old image file
#         if os.path.isfile(old_user.profile_image.path):
#             os.remove(old_user.profile_image.path)

# # Delete file when user is deleted
# @receiver(post_delete, sender=CustomUser)
# def auto_delete_profile_image_on_delete(sender, instance, **kwargs):
#     if instance.profile_image:
#         if os.path.isfile(instance.profile_image.path):
#             os.remove(instance.profile_image.path)