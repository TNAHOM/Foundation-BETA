# Generated by Django 4.1.2 on 2023-07-05 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_score_disqualified_ans_score_disqualified_ans_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='exam_code',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
