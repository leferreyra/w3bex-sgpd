	# Sistema de Gestion de pagos Diarios, Por Leonardo Ferreyra w3bex.com

import cPickle as pickle, datetime

class Cliente(object):
	
	def __init__(self, id):
		self.id = id
		self.productos = [];
		self.direccion = ""
		self.telefono = ""
		self.comentarios = ""
		self.fecha_creacion = datetime.date.today()

	@property
	def saldo(self):
		x = 0
		for i in self.productos:
			x += i.saldo
		return x

	def esMoroso(self):
		return True


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
	def cuota(self):
		return self.precio / self.cuotas

	@property
	def saldo(self):
		return self.precio - (self.cuota * self.cuotas_pagas)

	def pagar(self, nc = 1):
		self.cuotas_pagas += nc


class Pago():

	def __init__(self, fecha, cliente, monto, cuotas):
		self.fecha = fecha;
		self.cliente = cliente;
		self.monto = monto;
		self.cuotas = cuotas

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

	def load(self):
		try:
			infile = open(self.file, "r");
		except:
			self.save()
		infile = open(self.file, "r");
		p = pickle.Unpickler(infile)
		self.objects = p.load()
		infile.close()