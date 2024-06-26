# Generated by Django 4.2.1 on 2023-05-22 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickPin',
            fields=[
                ('quick_pin_id', models.AutoField(primary_key=True, serialize=False)),
                ('quick_pin', models.CharField(max_length=160)),
                ('user_secret', models.CharField(max_length=160)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
