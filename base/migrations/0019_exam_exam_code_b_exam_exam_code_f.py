# Generated by Django 4.1.2 on 2023-07-08 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_remove_exam_exam_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='exam_code_b',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_code_f',
            field=models.IntegerField(null=True),
        ),
    ]
