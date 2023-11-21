# Generated by Django 4.2.1 on 2023-11-21 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_dormroom_comments_dormroom_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='dormroom',
            name='bookmarked_by',
            field=models.ManyToManyField(blank=True, related_name='bookmarked', to='users.register'),
        ),
        migrations.AlterField(
            model_name='dormroom',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted', to='users.register'),
        ),
    ]
