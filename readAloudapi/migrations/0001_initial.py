# Generated by Django 3.1.7 on 2021-03-19 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('author', models.CharField(max_length=75)),
                ('publish_year', models.IntegerField()),
                ('notes', models.TextField(max_length=1500)),
                ('cover_url', models.CharField(max_length=125)),
                ('rating', models.FloatField()),
                ('location', models.CharField(max_length=50)),
                ('synopsis', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=25)),
                ('bio', models.CharField(max_length=500)),
                ('profile_pic', models.ImageField(null=True, upload_to='porfile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vocab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=40)),
                ('definition', models.CharField(max_length=255)),
                ('page', models.CharField(max_length=3)),
                ('notes', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcriber', to='readAloudapi.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribee', to='readAloudapi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150)),
                ('page', models.CharField(max_length=3)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readAloudapi.book')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField()),
                ('comment', models.TextField(max_length=1000)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readAloudapi.book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readAloudapi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='BookVocab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readAloudapi.book')),
                ('vocab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readAloudapi.vocab')),
            ],
        ),
        migrations.CreateModel(
            name='BookTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='readAloudapi.book')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='readAloudapi.topic')),
            ],
        ),
        migrations.CreateModel(
            name='BookSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='readAloudapi.book')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='readAloudapi.skill')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='readAloudapi.profile'),
        ),
    ]
