# Generated by Django 5.1.2 on 2024-11-26 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_evento_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evento',
            options={'ordering': ['fecha_inicio']},
        ),
    ]
