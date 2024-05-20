from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Password(models.Model):
    password_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

class SecureNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=255)
    note_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

class BankDetail(models.Model):
    bank_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    expiration_date = models.DateField(blank=True, null=True)
    cvv = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class BankDetail(models.Model):
    bank_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50)
    branch_address = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    # created_at = models.DateTimeField(default=timezone.now,)
    # updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

class PaymentCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    card_holder_name = models.CharField(max_length=255)
    card_type = models.CharField(max_length=100)
    card_number = models.CharField(max_length=50)
    cvv = models.CharField(max_length=10)
    expiration_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    



