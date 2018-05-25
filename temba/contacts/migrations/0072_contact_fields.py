# Generated by Django 1.11.6 on 2018-03-06 16:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("contacts", "0071_contactgroup_status")]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="fields",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                help_text="The fields set for this contact, keyed by UUID", null=True, verbose_name="Fields"
            ),
        )
    ]
