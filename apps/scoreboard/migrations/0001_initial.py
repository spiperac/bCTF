# Generated by Django 2.1.2 on 2018-10-31 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=4096)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
