# Generated by Django 4.2 on 2023-04-07 09:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer', models.UUIDField()),
                ('address', models.UUIDField()),
                ('payment_method', models.UUIDField()),
                ('remote_id', models.CharField(blank=True, default=None, help_text='remote invoice id at the payment gateway', max_length=255, null=True, verbose_name='remote_invoice_id')),
            ],
            options={
                'verbose_name': 'checkout',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.CharField(choices=[('Processing Purchase', 'Processing Purchase'), ('Approved Purchase', 'Approved Purchase'), ('Purchase Denied', 'Purchase Denied'), ('Purchase Sent', 'Purchase Sent')], max_length=30)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'status',
            },
        ),
        migrations.CreateModel(
            name='CheckoutItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product', models.UUIDField()),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout_items', to='checkout.checkout')),
            ],
            options={
                'verbose_name': 'checkout item',
            },
        ),
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status', to='checkout.status'),
        ),
    ]
