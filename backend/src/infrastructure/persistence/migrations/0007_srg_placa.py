from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persistence', '0006_srgevent_delete_checklistitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='srg',
            name='placa',
            field=models.CharField(db_index=True, default='', max_length=10),
            preserve_default=False,
        ),
    ]
