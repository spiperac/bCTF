# Generated by Django 2.1.2 on 2018-11-12 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0006_firstblood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='data',
            field=models.FileField(max_length=500, upload_to='media/attachments/'),
        ),
    ]
