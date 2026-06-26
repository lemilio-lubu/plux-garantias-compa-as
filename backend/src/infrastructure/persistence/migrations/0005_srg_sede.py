from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persistence', '0004_audit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='srg',
            name='km_cierre',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='codigo_tecnico',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='desc_problema',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='posibles_causas',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='solucion',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='cod_naturaleza',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='cod_causa',
        ),
        migrations.RemoveField(
            model_name='srg',
            name='parte_causal',
        ),
        migrations.AddField(
            model_name='srg',
            name='sede',
            field=models.CharField(
                choices=[('SURMOTOR', 'Surmotor'), ('GRANDA_CENTENO', 'Granda Centeno'), ('SHYRIS', 'Shyris')],
                default='SURMOTOR',
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
