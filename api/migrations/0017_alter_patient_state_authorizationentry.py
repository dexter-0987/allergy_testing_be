# Generated by Django 5.2 on 2025-05-15 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_alter_allergentest_test_date_alter_patient_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="state",
            field=models.CharField(
                choices="(('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))",
                max_length=50,
            ),
        ),
        migrations.CreateModel(
            name="AuthorizationEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("drug_name", models.CharField(max_length=255)),
                ("dose", models.CharField(max_length=100)),
                ("frequency", models.CharField(max_length=100)),
                ("insurance", models.CharField(max_length=255)),
                ("auth_number", models.CharField(max_length=100)),
                ("expiration_date", models.DateField()),
                ("at_home", models.BooleanField(default=False)),
                ("cost_estimate", models.CharField(blank=True, max_length=100)),
                ("visit_history", models.TextField(blank=True)),
                (
                    "uploaded_doc",
                    models.FileField(
                        blank=True, null=True, upload_to="authorization_docs/"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="authorization_entries",
                        to="api.patient",
                    ),
                ),
            ],
        ),
    ]
