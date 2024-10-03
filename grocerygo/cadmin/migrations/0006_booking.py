# Generated by Django 4.2.7 on 2024-10-02 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cadmin', '0005_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.TextField(blank=True, default={'objects': []}, null=True)),
                ('total', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Dispatch'), (3, 'On the way'), (4, 'Delivered'), (5, 'Cancel'), (6, 'Return')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
