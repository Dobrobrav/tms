# Generated by Django 5.2.1 on 2025-07-07 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_rename_commenter_id_commentmodel_commenter'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskAttachmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='tasks.taskmodel')),
            ],
        ),
    ]
