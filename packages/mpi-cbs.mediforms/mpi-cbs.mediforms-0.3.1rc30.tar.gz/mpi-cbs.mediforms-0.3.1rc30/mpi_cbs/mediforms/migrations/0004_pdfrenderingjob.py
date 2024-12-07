from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mediforms', '0003_remove_formdatamrtconnectom_token_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFRenderingJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('language', models.CharField(default='de', max_length=8, verbose_name='Language')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mediforms.method')),
            ],
            options={
                'verbose_name': 'PDF rendering job',
                'verbose_name_plural': 'PDF rendering jobs',
            },
        ),
    ]
