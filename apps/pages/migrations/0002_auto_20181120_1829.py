# Generated by Django 2.1.2 on 2018-11-20 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'get_latest_by': 'created_on'},
        ),
    ]
