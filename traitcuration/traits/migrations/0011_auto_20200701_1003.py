# Generated by Django 3.0.7 on 2020-07-01 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0010_merge_20200630_1023'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mappingsuggestion',
            unique_together={('trait_id', 'term_id')},
        ),
    ]
