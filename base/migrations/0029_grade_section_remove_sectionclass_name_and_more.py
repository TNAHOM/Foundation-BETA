# Generated by Django 4.1.2 on 2022-12-25 13:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_remove_exam_all_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('grade', models.IntegerField()),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.school')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('section', models.CharField(max_length=1)),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.grade')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.school')),
            ],
        ),
        migrations.RemoveField(
            model_name='sectionclass',
            name='name',
        ),
        migrations.DeleteModel(
            name='ClassGrade',
        ),
        migrations.DeleteModel(
            name='SectionClass',
        ),
    ]
