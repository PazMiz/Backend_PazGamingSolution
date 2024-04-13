# Generated by Django 4.2.2 on 2023-08-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_topic_created_at_alter_topic_author_alter_topic_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='answers',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='topic',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='topic',
            name='text',
            field=models.TextField(default='default_text'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]