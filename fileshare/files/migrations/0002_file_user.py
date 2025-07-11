# Generated by Django 5.2.3 on 2025-06-25 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
        ('user', '0002_remove_fileuser_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='File_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.fileuser')),
            ],
        ),
    ]
