# Generated by Django 2.1.7 on 2020-03-24 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200324_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationuser',
            name='service_catogory',
            field=models.TextField(blank=True, null=True),
        ),
    ]
