# Generated by Django 3.0.7 on 2020-07-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0004_auto_20200724_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ontologyterm',
            name='status',
            field=models.CharField(choices=[('CURRENT', 'current'), ('OBSOLETE', 'obsolete'), ('DELETED', 'deleted'), ('NEEDS_IMPORT', 'needs_import'), ('AWAITING_IMPORT', 'awaiting_import'), ('NEEDS_CREATION', 'needs_creation'), ('AWAITING_CREATION', 'awaiting_creation')], max_length=30),
        ),
        migrations.AlterField(
            model_name='trait',
            name='status',
            field=models.CharField(choices=[('CURRENT', 'current'), ('UNMAPPED', 'unmapped'), ('OBSOLETE', 'obsolete'), ('DELETED', 'deleted'), ('NEEDS_IMPORT', 'needs_import'), ('AWAITING_IMPORT', 'awaiting_import'), ('NEEDS_CREATION', 'needs_creation'), ('AWAITING_CREATION', 'awaiting_creation'), ('AWAITING_REVIEW', 'awaiting_review')], editable=False, max_length=30),
        ),
    ]