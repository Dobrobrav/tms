# Generated by Django 5.2.1 on 2025-06-16 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_commentmodel_commenter_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentmodel',
            old_name='commenter_id',
            new_name='commenter',
        ),
    ]
