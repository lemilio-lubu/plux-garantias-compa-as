from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persistence', '0007_srg_placa'),
    ]

    operations = [
        migrations.AddField(
            model_name='srgevent',
            name='location',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
