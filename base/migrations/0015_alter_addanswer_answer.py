# Generated by Django 4.1.2 on 2022-11-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_addanswer_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addanswer',
            name='answer',
            field=models.CharField(max_length=255),
        ),
    ]
