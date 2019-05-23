# Generated by Django 2.2 on 2019-05-21 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Catalogos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcumuladoMes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuenta_banco', models.CharField(blank=True, max_length=20, null=True)),
                ('mes', models.CharField(blank=True, max_length=7, null=True)),
                ('fecha_inicial', models.DateField(blank=True, null=True)),
                ('fecha_final', models.DateField(blank=True, null=True)),
                ('depositos', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('retiros', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
            ],
            options={
                'verbose_name_plural': 'Acumulados mensuales',
                'db_table': 'condominio_acumulado_mes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Condomino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depto', models.CharField(blank=True, max_length=15, null=True)),
                ('propietario', models.CharField(blank=True, max_length=60, null=True)),
                ('poseedor', models.CharField(blank=True, max_length=60, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=25, null=True)),
                ('telefono', models.CharField(blank=True, max_length=30, null=True)),
                ('fecha_escrituracion', models.DateField(blank=True, null=True)),
                ('referencia', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('indiviso', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('adeudo_inicial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('fecha_adeudo_inicial', models.DateField(blank=True, null=True)),
                ('cargos', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('abonos', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
            ],
            options={
                'db_table': 'condominio_condomino',
                'ordering': ['depto'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CuentaBanco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clabe', models.CharField(max_length=18)),
                ('apoderado', models.CharField(max_length=60)),
                ('saldo_inicial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('fecha_saldo_inicial', models.DateField(blank=True, null=True)),
                ('saldo_final', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('fecha_saldo_final', models.DateField(blank=True, null=True)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Catalogos.Banco')),
            ],
            options={
                'verbose_name_plural': 'Cuentas bancarias',
                'db_table': 'condominio_cuenta_banco',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('debe', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Depositos')),
                ('haber', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Cargos')),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('condomino', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Condominio.Condomino')),
                ('cuenta_contable', models.ForeignKey(limit_choices_to=models.Q(clave_mayor='23'), on_delete=django.db.models.deletion.CASCADE, to='Catalogos.CuentaContable', verbose_name='Cuenta Contable')),
            ],
            options={
                'verbose_name_plural': 'Registros',
                'db_table': 'condominio_registro',
                'ordering': ['fecha'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_movimiento', models.DateField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('deposito', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('retiro', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('condomino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Condominio.Condomino')),
                ('cuenta_banco', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Condominio.CuentaBanco')),
            ],
            options={
                'db_table': 'condominio_movimiento',
                'ordering': ['fecha_movimiento'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DetalleMovimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('comentario', models.CharField(blank=True, default='.', max_length=20, null=True)),
                ('cuenta_contable', models.ForeignKey(limit_choices_to=models.Q(('clave_mayor', '41'), ('clave_mayor', '51'), ('num_cuenta', '2318'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='Catalogos.CuentaContable', verbose_name='Cuenta Contable Ingreso/Egreso')),
                ('movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Condominio.Movimiento', verbose_name='Movto')),
            ],
            options={
                'db_table': 'condominio_detalle_movimiento',
                'ordering': ['movimiento'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CuotasCondominio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=30, null=True)),
                ('mes_inicial', models.DateField(blank=True, null=True)),
                ('mes_final', models.DateField(blank=True, null=True)),
                ('dia_vencimiento', models.DecimalField(blank=True, decimal_places=0, default=1, max_digits=2, null=True)),
                ('monto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('condomino', models.ManyToManyField(related_name='sadiochouno_cuotas_condomino_id', to='Condominio.Condomino')),
                ('cuenta_contable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Catalogos.CuentaContable', verbose_name='Cuenta Contable')),
            ],
            options={
                'verbose_name_plural': 'Cuotas del condominio',
                'db_table': 'condominio_cuotas',
                'ordering': ['mes_inicial'],
                'managed': True,
            },
        ),
    ]