from django.db import models
from Catalogos.models import Banco, Condominio, CuentaContable
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.html import format_html

class CuentaBanco(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    clabe = models.CharField(max_length=18)
    apoderado = models.CharField(max_length=60)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    fecha_saldo_inicial = models.DateField(blank=True, null=True)
    saldo_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    fecha_saldo_final = models.DateField(blank=True, null=True)
 
    def __str__(self):
        return '%s %s %d' % (self.clabe, self.apoderado[:10], self.saldo_final)

    class Meta:
        managed = True
        db_table = 'condominio_cuenta_banco'
        verbose_name_plural = "Cuentas bancarias"

class Condomino(models.Model):
    depto = models.CharField(max_length=15, blank=True, null=True)
    propietario = models.CharField(max_length=60, blank=True, null=True)
    poseedor = models.CharField(max_length=60, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=25, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fecha_escrituracion = models.DateField(blank=True, null=True)
    referencia = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    indiviso = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    adeudo_inicial = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    fecha_adeudo_inicial = models.DateField(blank=True, null=True)
    cargos = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,default = 0)
    abonos = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,default = 0)
    saldo  = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default = 0)
    
    def __str__(self):
        return '%s %s' % (self.depto, self.poseedor)

    def estado_cuenta(self):
        icon_url = static('admin/img/icon-viewlink.svg')
        text = format_html('<img src="{}" alt="view">', icon_url)
        return mark_safe('<a href="/admin/Condominio/registro/?condomino__id__exact=%d">%s</a>' % (self.id, text))

    def detalle(self):
        icon_url = static('admin/img/icon-viewlink.svg')
        text = format_html('<img src="{}" alt="view">', icon_url)
        return mark_safe('<a href="/admin/Condominio/movimiento/?condomino__id__exact=%d">%s</a>' % (self.id, text))

    def descarga(self):
        text = '''
        <svg width="16" height="16" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <defs>
                <g id="down">
                    <path d="M1412 897q0-27-18-45l-91-91q-18-18-45-18t-45 18l-189 189v-502q0-26-19-45t-45-19h-128q-26 0-45 19t-19 45v502l-189-189q-19-19-45-19t-45 19l-91 91q-18 18-18 45t18 45l362 362 91 91q18 18 45 18t45-18l91-91 362-362q18-18 18-45zm252-1q0 209-103 385.5t-279.5 279.5-385.5 103-385.5-103-279.5-279.5-103-385.5 103-385.5 279.5-279.5 385.5-103 385.5 103 279.5 279.5 103 385.5z"/>
                </g>
            </defs>
            <use xlink:href="#down" x="0" y="0" fill="#447e9b" />
        </svg>
        '''
        return mark_safe('<a href="/explorer/5/download?format=csv&params=depto:\'%s\'">%s</a>' % (self.depto, text))

    estado_cuenta.allow_tags = True
    detalle.allow_tags = True
    descarga.allow_tags = True

    class Meta:
        managed = True
        db_table = 'condominio_condomino'
        ordering = ['depto']

class Movimiento(models.Model):
    cuenta_banco = models.ForeignKey(CuentaBanco, default = 1, on_delete=models.PROTECT)
    fecha_movimiento = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    deposito = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    retiro = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    condomino = models.ForeignKey(Condomino, on_delete=models.PROTECT)

    def __str__(self):
        return u'%d %s %d %s' % (self.id, self.fecha_movimiento.strftime('%d/%m/%Y'), self.deposito, self.descripcion[:15])

    class Meta:
        managed = True
        db_table = 'condominio_movimiento'
        ordering = ['fecha_movimiento']

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, verbose_name = ('Movto'), on_delete = models.CASCADE)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable Ingreso/Egreso'), on_delete = models.CASCADE, limit_choices_to = Q(clave_mayor='41') | Q(clave_mayor='51') | Q(num_cuenta='2318'))
    comentario = models.CharField(max_length=20, blank=True, null=True, default=".")

    def __str__(self):
        return '%s %d' % (self.cuenta_contable, self.monto)

    class Meta:
        managed = True
        db_table = 'condominio_detalle_movimiento'
        ordering = ['movimiento']

class Registro(models.Model):
    condomino = models.ForeignKey(Condomino, default=1, on_delete=models.PROTECT)
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    debe = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0, verbose_name = 'Depositos')
    haber = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0, verbose_name = 'Cargos' )
    saldo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable'), on_delete = models.CASCADE, limit_choices_to = Q(clave_mayor='23'))
 
    def __str__(self):
        return u'%d %s %d %d %d' % (self.id, self.fecha.strftime('%d/%m/%Y'), self.debe, self.haber, self.saldo)

    class Meta:
        managed = True
        db_table = 'condominio_registro'
        ordering = ['fecha']
        verbose_name_plural = "Registros"

class CuotasCondominio(models.Model):
    descripcion = models.CharField(max_length=30, blank=True, null=True)
    mes_inicial = models.DateField(blank=True, null=True)
    mes_final = models.DateField(blank=True, null=True)
    dia_vencimiento = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True, default=1)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable'), on_delete = models.CASCADE)
    condomino = models.ManyToManyField(Condomino, related_name='sadiochouno_cuotas_condomino_id')

    def __str__(self):
        return u'%s %s %s %d %s' % (self.descripcion, self.mes_inicial.strftime('%m-%Y'), self.mes_final.strftime('%m-%Y'), self.monto, self.cuenta_contable)

    class Meta:
        managed = True
        db_table = 'condominio_cuotas'
        ordering = ['mes_inicial']
        verbose_name_plural = "Cuotas del condominio"

class AcumuladoMes(models.Model):
    cuenta_banco = models.CharField(max_length=20, blank=True, null=True)
    mes = models.CharField(max_length=7, blank=True, null=True)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    depositos = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    retiros = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return u'%s %s %s %s %d %d %d' % (self.cuenta_banco,self.mes,self.fecha_inicial.strftime('%d/%m/%Y'), self.fecha_final.strftime('%d/%m/%Y'),self.depositos, self.retiros, self.saldo)
 
    class Meta:
        managed = True
        db_table = 'condominio_acumulado_mes'
        verbose_name_plural = "Acumulados mensuales"

