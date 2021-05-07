from django.db import migrations, models
from api.constants import SystemParameterKey


def add_session_expiration_time_sys_param(apps, schema_editor):
    SystemParameter = apps.get_model("api", "SystemParameter")
    SystemParameter(key=SystemParameterKey.session_expiration_date_in_seconds, value='{"value": "7200"}').save()


class Migration(migrations.Migration):

    dependencies = [('api', '0009_systemparameter_description'),]

    operations = [
        migrations.RunPython(add_session_expiration_time_sys_param),
    ]