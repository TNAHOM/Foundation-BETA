# Generated by Django 4.1.2 on 2023-05-27 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_exam_fillblank_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='fillblank_answer',
            field=models.CharField(blank=True, max_length=1028, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='truefalse_answer',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]