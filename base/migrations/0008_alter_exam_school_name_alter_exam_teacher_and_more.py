# Generated by Django 4.1.2 on 2023-02-23 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_score_incorrect_ans_score_incorrect_ans_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='school_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.school'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher', to='base.teacher'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.school'),
        ),
    ]