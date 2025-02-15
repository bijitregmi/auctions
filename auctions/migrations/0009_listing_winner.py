# Generated by Django 4.1.7 on 2024-01-09 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_bidder_alter_bid_item_alter_comment_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listing_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
