# Sistema de Gestion de pagos Diarios

import cPickle as pickle, datetime

class Cliente(object):
	
	def __init__(self, id):
		self.id = id
		self.productos = [];
		self.direccion = ""
		self.telefono = ""
		self.comentarios = ""
		self.fecha_creacion = datetime.date.today()
		self.resto = 0 # diferencia que no alcanza para una cuota completa

	def GetMinProd(self):
		if len(self.productos)!=0:
			return min(self.productos, key = lambda x: x.cuota) # b es el producto mas barato
		else:
			return None

	def GetMaxProdAtr(self):
		if len(self.productos)!=0:
			return max(self.productos, key = lambda x: x.cuotas_atrasadas) # el producto mas atrasado
		else:
			return None 
    
	@property
	def cuota(self):
		c = 0.00
		for i in self.productos:
			c += i.saldo_atrasado
			if (i.cuotas_pagas + i.cuotas_atrasadas + 1) < i.cuotas:
				c += i.cuota
			else:
				if self.resto > 0 :
					c += (i.cuota - self.resto)
				else:
					c += i.cuota

		return c

	@property
	def saldo(self):
		x = 0
		for i in self.productos:
			x += i.saldo
		return x

	@property
	def saldo_atrasado(self):
		sa = self.resto
		for i in self.productos:
			sa += i.cuotas_atrasadas * i.cuota
		return sa


	def esMoroso(self):
		if self.saldo_atrasado != 0:
			return True
		else:
			return False

	def pagar(self, monto):
		b = self.GetMinProd()
		for p in self.productos:
			a = self.GetMaxProdAtr() # Primero cobramos los atrasos, del mas atrasado al menos atrasado.
			if monto >= a.saldo_atrasado and a.saldo_atrasado > 0:
				#print "pagando %g atrazo del producto %s" % (a.saldo_atrasado, a.nombre)
				monto -= a.saldo_atrasado
				a.pagar(a.cuotas_atrasadas)

		
		while monto > 0:
			if monto >= b.cuota:
				for p in self.productos:
					if not p.esta_pagado:
						if monto >= p.cuota:
							#print "pagando %g por el producto %s por cuota nomal" % (p.cuota, p.nombre)
							monto -= p.cuota
							p.pagar()
			else:
				print "sobro %g" % monto
				self.resto += monto
				monto = 0

		# Si el resto alcanza para pagar la cuota mas barata.. la cobramos.
		if self.resto >= b.cuota:
			#print "lo que sobro del pago mas el resto %g alcanza para la cuota de %s" % ( self.resto, b.nombre)
			self.resto -= b.cuota
			b.pagar()



class Cobrador():
	
	def __init__(self, nombre):
		self.nombre = nombre;
		self.clientes = [];

class Producto(object):
	
	def __init__(self, nombre, precio, cuotas):
		self.nombre = nombre;
		self.precio = precio;
		self.cuotas = cuotas;
		self.cuotas_pagas = 0;
		self.dia_compra = datetime.date.today()

	@property
	def saldo_atrasado(self):
		return self.cuota * self.cuotas_atrasadas

	@property
	def cuotas_al_dia(self):

		hoy = datetime.date.today()
		delta = hoy - self.dia_compra
		dom = 0 # domingos dentro del delta
		d = datetime.timedelta(days=1)

		for i in xrange(delta.days):
			if (self.dia_compra + (d*i)).weekday() == 6:
				dom += 1

		margen = 1
		if hoy == self.dia_compra:
			margen = 0 # Margen es la espera hasta un dia despues para declarar un cliente atrazado

		return delta.days - dom - margen

	@property
	def al_dia(self):
		if cuotas_atrasadas == 0:
			return True
		else:
			return False

	@property
	def cuotas_atrasadas(self):
		if (self.cuotas_al_dia - self.cuotas_pagas) < self.cuotas:
			if (self.cuotas_al_dia - self.cuotas_pagas) >= 0:
				return (self.cuotas_al_dia - self.cuotas_pagas)
			else:
				return 0
		else:
			return self.cuotas - self.cuotas_pagas

	@property
	def cuota(self):
		return self.precio / self.cuotas

	@property
	def saldo(self):
		return self.precio - (self.cuota * self.cuotas_pagas)

	def pagar(self, nc = 1):
		self.cuotas_pagas += nc

	@property
	def esta_pagado(self):
		if self.cuotas <= self.cuotas_pagas:
			return True
		else:
			return False



class Pago():

	def __init__(self, fecha, cliente, monto):
		self.fecha = fecha;
		self.cliente = cliente;
		self.monto = monto;

class Data():
	"""Operaciones para guardar Datos y recuperarlos"""
	def __init__(self):
		self.file = "data.pkl"
		self.backup_file = "data.bak"
		self.objects = {"clientes":[], "cobradores":[], "pagos":[]}

	def save(self):
		backfile = open(self.backup_file, "w");
		try:
			infile = open(self.file, "r")
		except:
			infile = open(self.file, "w+")
		backfile.write(infile.read())
		backfile.close()
		infile.close()
		outfile = open(self.file, "w");
		p = pickle.Pickler(outfile)
		p.dump(self.objects)
		outfile.close()

	def backup(self, f): # f es la ruta donde se va a guardar el backup.
		"""crear un archivo de back up"""
		bf = open(f, 'w')
		bp = pickle.Pickler(bf)
		bp.dump(self.objects)
		bf.close()

	def load(self, backup=""):
		if backup != "":
			self.file = backup
		try:
			infile = open(self.file, "r");
		except:
			self.save()
		infile = open(self.file, "r");
		p = pickle.Unpickler(infile)
		self.objects = p.load()
		infile.close()
		if backup != "":
			self.file = 'data.pkl'
			self.save()
