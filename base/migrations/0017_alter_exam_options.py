# Generated by Django 4.1.2 on 2022-11-29 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_exam_options_exam_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['created']},
        ),
    ]
