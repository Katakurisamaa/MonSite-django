# Generated by Django 4.0.5 on 2022-09-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0003_variation'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='boutique.variation'),
        ),
    ]