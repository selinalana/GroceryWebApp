# Generated by Django 4.2.7 on 2024-10-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadmin', '0008_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.IntegerField(choices=[(1, 'Read'), (2, 'Unread')], default=2),
        ),
    ]
