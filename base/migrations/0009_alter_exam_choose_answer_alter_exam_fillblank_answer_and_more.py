# Generated by Django 4.1.2 on 2023-02-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_exam_school_name_alter_exam_teacher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='choose_answer',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='fillblank_answer',
            field=models.CharField(blank=True, max_length=1028, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='truefalse_answer',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
