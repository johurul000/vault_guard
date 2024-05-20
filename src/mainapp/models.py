import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):

    first_login = models.BooleanField(default=True)

    REQUIRED_FIELDS = []

    objects = UserManager()



class LoginDetails(models.Model):
    password_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

class QuickPin(models.Model):
    quick_pin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quick_pin = models.CharField(max_length=160)
    user_secret = models.CharField(max_length=160)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class SecureNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=255)
    note_content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

class BankDetails(models.Model):
    bank_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ac_no_last_four = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=50)
    branch_address = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now,)
    updated_at = models.DateTimeField(blank=True, null=True)

class PaymentCards(models.Model):
    card_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    card_holder_name = models.CharField(max_length=255)
    card_type = models.CharField(max_length=100)
    card_number = models.CharField(max_length=255)
    card_no_last_four = models.CharField(max_length=50, blank=True, null=True)
    cvv = models.CharField(max_length=255)
    expiration_month = models.CharField(max_length=255, null=True)
    expiration_year = models.CharField(max_length=255, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now,)
    updated_at = models.DateTimeField(blank=True, null=True)


class PaymentCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    card_holder_name = models.CharField(max_length=255)
    card_type = models.CharField(max_length=100)
    card_number = models.CharField(max_length=50)
    card_no_last_four = models.CharField(max_length=50, blank=True, null=True)
    cvv = models.CharField(max_length=10)
    expiration_month = models.CharField(max_length=50, null=True)
    expiration_year = models.CharField(max_length=50, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now,)
    updated_at = models.DateTimeField(blank=True, null=True)





