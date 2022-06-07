# Generated by Django 4.0.4 on 2022-06-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.SlugField(choices=[('customer', 'Customer'), ('agent', 'Agent')], default='customer', null=True),
        ),
    ]