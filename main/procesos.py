from django.db           import connection
from django.db           import transaction

from Condominio.models   import AcumuladoMes, Registro, CuotasCondominio, Movimiento, Condomino
from Catalogos.models    import CuentaContable, PeriodoCorte

from explorer.models     import Query
from datetime            import datetime, timedelta

def dictfetchall(cursor):
	desc = cursor.description
	if desc:
		return [
       		dict(zip([col[0] for col in desc],row))
       		for row in cursor.fetchall()
		]
	else:
		return None

def execsql(consulta):
	cursor = connection.cursor()
	print(consulta)
	cursor.execute(consulta)
	result_list = dictfetchall(cursor)
	cursor.close()
	return result_list

def run_acum(condominio):
	print(" generando acumulados %s " % condominio)
	with transaction.atomic():
		#
		#Borra acumulados
		borrado = 'delete from condominio_acumulado_mes'
		nq1 = 1
		nq2 = 2		
		#
		n = execsql(borrado)
		#
		#Trae saldo inicial de cada cuenta
		saldo_condominio = 0 
		rows = execsql(Query.objects.get(id=nq1).sql)
		print(rows)
		#
		#Por cada cuenta
		for r in rows:
			saldo = float(r['saldo_inicial'])
			#
			#Agrega depositos y retiros por cuenta y mes
			rows2 = execsql(Query.objects.get(id=nq2).sql)
			for r2 in rows2:
				if r2['cuenta'] == r['cuenta']:
					saldo = round(saldo + float(r2['depositos']) - float(r2['retiros']),2) 
						
					#print(r2['cuenta'], r2['mes'], r2['depositos'], r2['retiros'], saldo)

					reg = AcumuladoMes(cuenta_banco=r2['cuenta'],   \
									   mes=r2['mes'],               \
									   fecha_inicial=r2['fec_ini'], \
									   fecha_final=r2['fec_fin'],   \
									   depositos=r2['depositos'],   \
									   retiros=r2['retiros'],       \
									   saldo=saldo)
					reg.save()

			saldo_condominio = saldo_condominio + saldo		
			#print(saldo_condominio)
		#
		#Actualiza saldo en periodos	
		oPer = PeriodoCorte.objects.get(id=1)
		oPer.saldo_final=saldo_condominio
		oPer.save()

def run_determinacionSaldos(condomino):
	print(" determinando saldos %s " % condomino.depto)
	with transaction.atomic():
		#tipo   = TipoMovimiento.objects.get(id=21)
		#prop   = TipoMovimiento.objects.get(id=30)
		cuenta = CuentaContable.objects.get(id=82)
		#prove  = Proveedore.objects.get(id=1)
		#
		#Borra asientos 
		n = execsql('delete from condominio_registro where condomino_id = %s' % condomino.id)
		#
		#Agrega adeudo inicial
		if not condomino.depto == '0000':
			ade = condomino.adeudo_inicial
			sal = 0
			deb = 0
			sal = sal + deb - ade
			#adeudo = condomino.adeudo_inicial
			reg_i = Registro(fecha = condomino.fecha_adeudo_inicial, \
							 descripcion='SALDO INICIAL A LA FECHA', \
							 debe = deb, \
							 haber= ade, \
							 saldo= sal, \
							 cuenta_contable=cuenta, \
							 condomino = condomino)
			reg_i.save()
		#
		#Agrega adeudos por cuotas
		rows = CuotasCondominio.objects.all().order_by('mes_inicial')
		for r in rows:
			delta = (r.mes_final - r.mes_inicial)
			#print(r.descripcion,r.mes_inicial,r.mes_final,r.monto,r.cuenta_contable,delta.days)
			condom = r.condomino.filter(depto__contains=condomino.depto)
			if condom:	
				base = r.mes_inicial
				for x in range (0, delta.days + 1):
					fecha = base + timedelta(days=x)
					if fecha.day == 1:
						reg_a = Registro(fecha = fecha, \
								         descripcion='CARGO {}'.format(r.descripcion) , \
								         debe = 0, \
								         haber=r.monto, \
								         saldo=0, \
								         cuenta_contable=r.cuenta_contable, \
								         condomino = condomino)
						reg_a.save()
		#
		#Agrega depositos por movimiento de banco
		if not condomino.depto == '0000':
			movtos = Movimiento.objects.filter(condomino__id=condomino.id)
			for m in movtos:
				reg_m = Registro(fecha = m.fecha_movimiento,  \
						         descripcion=m.descripcion , \
						         debe = m.deposito, \
						         haber=0, \
						         saldo=0, \
						         cuenta_contable=r.cuenta_contable, \
						         condomino = condomino)
				reg_m.save()
			#
	#Recalcula saldos
	if not condomino.depto == '0000':
		sal = 0
		car = 0
		dep = 0
		rec = Registro.objects.filter(condomino__id=condomino.id).order_by('fecha','id')
		for rr in rec:
			car = car + rr.haber
			dep = dep + rr.debe
			sal = sal + rr.haber - rr.debe
			rr.saldo = sal
			rr.save()
			
		reg_c = Condomino.objects.get(id=condomino.id)
		reg_c.cargos = car
		reg_c.abonos = dep
		reg_c.saldo  = sal
		reg_c.save()


