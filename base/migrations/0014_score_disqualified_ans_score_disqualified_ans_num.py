# Generated by Django 4.1.2 on 2023-06-22 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_exam_ans_exam_matching_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='disqualified_ans',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='disqualified_ans_num',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
