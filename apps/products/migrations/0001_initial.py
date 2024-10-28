# Generated by Django 5.0.1 on 2024-10-28 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("sku", models.CharField(editable=False, max_length=20, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock_quantity", models.PositiveIntegerField()),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2, help_text="Weight in kg", max_digits=6
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="products.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                ("image", models.ImageField(upload_to="products/")),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductVariant",
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
                ("name", models.CharField(max_length=100)),
                ("value", models.CharField(max_length=100)),
                (
                    "price_adjustment",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("stock_quantity", models.PositiveIntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
