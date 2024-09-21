# Generated by Django 4.1 on 2024-09-21 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("userid", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=20, unique=True)),
                ("firstname", models.CharField(max_length=30)),
                ("lastname", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "questionid",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("tag", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "userid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forum.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                ("answerid", models.AutoField(primary_key=True, serialize=False)),
                ("answer", models.TextField()),
                (
                    "questionid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forum.question"
                    ),
                ),
                (
                    "userid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forum.user"
                    ),
                ),
            ],
        ),
    ]
