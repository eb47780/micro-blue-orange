# Generated by Django 4.1.7 on 2023-04-05 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authcore', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CheckoutUserAddress',
            new_name='CheckoutUser',
        ),
        migrations.AlterModelOptions(
            name='checkoutuser',
            options={'verbose_name': 'Checkout/User', 'verbose_name_plural': 'Checkout/User'},
        ),
    ]