"""
Copyright 2020 Facundo Erbin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
ubject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES 
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Nombre: E-Wallet
@autor: Facundo Erbin
curso: Fundamentos de Programacion en Python
version: 1.0
fecha: 20/02/2020
"""

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from os import system, name 
import json
import time


class Cliente(object):
	"""
	Clase representativa de los usuarios del sistema E-Wallet
	contiene informacion respecto al código y saldos del usuario.
	"""

	#Constructor de clase
	def __init__(self, codUsuario):
		super(Cliente, self).__init__()
		self.codUsuario = codUsuario
		self.m1=0.0
		self.m2=0.0
		self.m3=0.0
		self.m4=0.0
		self.m5=0.0
		self.m6=0.0
		self.m7=0.0
		self.m8=0.0
		self.saldoMoneda = {	#diccionario con los saldos de las billeteras
			moneda(1):self.m1,
			moneda(2):self.m2,
			moneda(3):self.m3,
			moneda(4):self.m4,
			moneda(5):self.m5,
			moneda(6):self.m6,
			moneda(7):self.m7,
			moneda(8):self.m8,
		}
		Cliente.usuario = self

	def getSaldo(self, moneda):
		return self.saldoMoneda.get(moneda)

	def setSaldo(self, moneda, monto):	#Establece el saldo de alguna moneda
		self.saldoMoneda[moneda] = float(monto)

	def aumentarSaldo(self, moneda, monto):
		self.saldoMoneda[moneda] = float(self.saldoMoneda.get(moneda)) + monto
		return self.saldoMoneda.get(moneda)

class Transaccion(object):
	"""
	Clase representativa de las Transaccines que realiza
	el sistema E-Wallet
	"""
	listaTransacciones = []	#lista que contendrá todas las transacciones realizadas
	
	#Metodo constructor de clase
	def __init__(self, remitente, destinatario, moneda, monto, operacion):
		super(Transaccion, self).__init__()
		self.codTrans = CodigoTransaccion()	#Codigo autogenerado
		self.fecha = datetime.now()			#fecha actual
		self.remitente = remitente
		self.destinatario = destinatario
		self.moneda = moneda
		self.monto = monto
		self.operacion = operacion 			#RECIBIDO o TRANSFERENCIA
		Transaccion.listaTransacciones.append(self)	#agrega el nuevo objeto a la lista

class CodigoTransaccion():
	"""
	Clase representativa que generara los codigos de las transacciones de forma secuencial
	"""
	ultimoCodigo=0								#valor a partir del cual inician los codigos
	
	def __init__(self):
		super(CodigoTransaccion, self).__init__()
		CodigoTransaccion.ultimoCodigo+=1		#aumenta el codigo a partir del anterior
		self.codigo = CodigoTransaccion.ultimoCodigo
	
	def getCodigo(self):						#devuelve el codigo del objeto			
		return (self.codigo)

def main():				#Metodo principal
  	limpiarPantalla()
  	print("--------------------------------------------------------------------------------------------------------------------------------")
  	#ASCII art, usar pantalla completa :)
  	print("""######                                                                    #######       #     #                                   
#     # # ###### #    # #    # ###### #    # # #####   ####       ##      #             #  #  #   ##   #      #      ###### ##### 
#     # # #      ##   # #    # #      ##   # # #    # #    #     #  #     #             #  #  #  #  #  #      #      #        #   
######  # #####  # #  # #    # #####  # #  # # #    # #    #    #    #    #####   ##### #  #  # #    # #      #      #####    #   
#     # # #      #  # # #    # #      #  # # # #    # #    #    ######    #             #  #  # ###### #      #      #        #   
#     # # #      #   ##  #  #  #      #   ## # #    # #    #    #    #    #             #  #  # #    # #      #      #        #   
######  # ###### #    #   ##   ###### #    # # #####   ####     #    #    #######        ## ##  #    # ###### ###### ######   #   """)
  	print("--------------------------------------------------------------------------------------------------------------------------------")
  	codUsuario=comprobarCodigo(input("Ingrese su cóodigo de identificación de 8 dígitos:\n"))
  	if (codUsuario==0):
  		return main()
  	usuario = Cliente(codUsuario)	#se crea el usuario con su codigo
  	menu(usuario)

def menu(usuario):			#metodo que exibe el menu de opciones
	def switch(opcion):		#metodo despachador de metodos
		if opcion==1:
			recibirCantidad(usuario)
		elif opcion==2:
			transferirMonto(usuario)
		elif opcion==3:
			mostrarBalance(usuario)
		elif opcion==4:
			mostrarBalanceGral(usuario)
		elif opcion==5:
			historico(usuario)
		else:
			terminarOperacion()

	select=0
	while (select>5 or select<1):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("USUARIO NRO: ")
		print("1- RECIBIR CANTIDAD")
		print("2- TRANSFERIR MONTO")
		print("3- MOSTRAR BALANCE DE UNA MONEDA")
		print("4- MOSTRAR BALANCE GENERAL")
		print("5- MOSTRAR HISTORICO DE TRANSACCIONES")
		print("\n9- SALIR")
		print("--------------------------------------------------------------------------------------------------------------------------------")
		select=validarInt(input("Ingrese el numero que corresponda a la operacion deseada..."))
		if (select == 9):
			terminarOperacion()
	switch(select)

def moneda(opcion):	#metodo encargado de almacenar y mostrar las monedas
	if opcion==1:
		return("Bitcoin (BTC)")
	elif opcion==2:
		return("Ethereum (ETH)")
	elif opcion==3:
		return("XRP")
	elif opcion==4:
		return("Bitcoin Cash (BCH)")
	elif opcion==5:
		return("Litecoin (LTC)")
	elif opcion==6:
		return("EOS")
	elif opcion==7:
		return("Binance Coin (BNB)")
	elif opcion==8:
		return("Tezos (XTZ)")	
	else:
		return("")

def limpiarPantalla(): 	#metodo para limpiar la pantalla del sistema
    if name == 'nt': 	# para windows
        _ = system('cls') 
    else: 				# para posix
        _ = system('clear') 

def validarInt(arg): #Valida que el dato ingresado es un entero
    try:
        int(arg)
        return int(arg)
    except:
        print("Ingreso un dato de tipo incorrecto...")
        return (0)

def formatFloat(arg):#Da formato a kis fkitantes con 2 cifras decimal
	try:
		float(arg)
		return ("%.2f" % float(arg))
	except:
		print("Ingreso un dato de tipo incorrecto...")
		return (0)

def comprobarCodigo(num):#verfica que los valores de codigo ingresados sean correctos
	cod=(validarInt(num))
	if (0<cod<100000000):	#máximo 8 cifras enteras
		return (cod)
	else:
		return(0)

def formatCod(cod):		#da formato al codigo, mostrandolo con 8 cifras
	return (format(cod, '08'))

def recibirCantidad(usuario):	#Permite recibir una cantidad de una criptomoneda y almacenarla
	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("RECIBIR CANTIDAD:\n")
	print("MONEDA A RECIBIR:")
	for x in range(1, 8):
		print(str(x) + "- "+ moneda(x))
	print("9- VOLVER...")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	select=validarInt(input("Ingrese el numero que corresponda a la moneda deseada..."))
	if (select==9):
		return (menu(usuario))
	if (not (0<select<9)):
		return (recibirCantidad(usuario))

	cantidad = 0
	while (cantidad==0):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("RECIBIR CANTIDAD:\n")
		print("Usted selecciono \nMONEDA: "+ moneda(select)+ "\n")
		print("--------------------------------------------------------------------------------------------------------------------------------")
		cantidad=formatFloat(input("Ingrese la cantidad que va a recibir:\nUse el punto (.) para separar decimales\n"))

	remitente=0
	while (remitente==0):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("RECIBIR CANTIDAD:\n")
		print("Usted selecciono \nMONEDA: "+ moneda(select))
		print("CANTIDAD: "+ cantidad)
		print("--------------------------------------------------------------------------------------------------------------------------------")
		remitente=comprobarCodigo(input("Ingrese el código de 8 digitos de identificación del remitente: "))

	confirma=""
	while (confirma!="S" and confirma!="s"):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("RECIBIR CANTIDAD:\n")
		print("Usted selecciono \nMONEDA: "+ moneda(select))
		print("CANTIDAD: "+ cantidad)
		print("REMITENTE: "+ formatCod(remitente))
		print("--------------------------------------------------------------------------------------------------------------------------------")
		confirma=input("Por favor confirme la operación (S/n)...")
		if (confirma=="N" or confirma=="n"):
			return menu(usuario)
	
	usuario.aumentarSaldo(moneda(select), float(cantidad))	#actualiza el saldo de la bulletera
	Transaccion(remitente, usuario.codUsuario, moneda(select), cantidad, 'RECIBIDO')#crea el objeto de la transaccion realizada

	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("SU OPERACIÓN FUE REALIZADA CON ÉXITO")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	input("Presione ENTER para continuar...")
	return menu(usuario)

def transferirMonto(usuario):	#permite transferir dinero a otra cuenta
	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("TRANSFERIR MONTO:\n")
	print("MONEDA A TRANSFERIR:")
	for x in range(1, 8):
		monto= float(usuario.getSaldo(moneda(x)))
		if (monto!=0.0):
			print(str(x) + "- "+ moneda(x) + "\t" + str(monto))
	print("9- VOLVER...")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	select=validarInt(input("Ingrese el numero que corresponda a la moneda deseada..."))
	if (select==9):
		return (menu(usuario))
	if (not (0<select<9) or (usuario.getSaldo(moneda(select))==0)): #verifica que la seleccion sea valida
		return (transferirMonto(usuario))

	cotizacion = obtenerCotizacion(moneda(select))	#cotizacion actualde la moneda seleccionada
	monto= float(usuario.getSaldo(moneda(select)))	#saldo actual de la moneda seleccionada
	saldo= monto * float(cotizacion)				#monto en USD de la moneda seleccionada

	cantidad = 0
	while (cantidad==0):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("TRANSFERIR MONTO:\n")
		print("Usted selecciono \nMONEDA: "+ moneda(select))
		print("Su saldo de " + moneda(select) + " en USD es: \t$ " + str(saldo))		
		print("--------------------------------------------------------------------------------------------------------------------------------")
		cantidad=formatFloat(input("Ingrese la cantidad en USD que va a transferir:\nUse el punto (.) para separar decimales\n"))
		if (saldo< float(cantidad)):	#verifica que no se pretenda transferir montos inexistentes
			cantidad= 0
			print("\nUsted no posee fondos suficientes...")
			time.sleep(1)
			return(transferirMonto(usuario))

	destinatario=0
	while (destinatario==0):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("TRANSFERIR MONTO:\n")
		print("Usted selecciono \nMONEDA: "+ moneda(select))
		print("Su saldo de " + moneda(select) + " en USD es: \t$ " + str(saldo))	
		print("Usted va a transferir: \t $ " + str(cantidad) + "USD")
		print("--------------------------------------------------------------------------------------------------------------------------------")
		destinatario=comprobarCodigo(input("Ingrese el código de 8 digitos de identificación del destinatario: "))

	confirma=""
	while (confirma!="S" and confirma!="s"):
		limpiarPantalla()
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("TRANSFERIR MONTO:\n")
		print("Usted selecciono \nMONEDA: "+ moneda(select))
		print("Su saldo de " + moneda(select) + " en USD es: \t$ " + str(saldo))	
		print("Usted va a transferir: \t $ " + str(cantidad) + "USD")
		print("DESTINATARIO: "+ formatCod(destinatario))
		print("--------------------------------------------------------------------------------------------------------------------------------")
		confirma=input("Por favor confirme la operación (S/n)...")
		if (confirma=="N" or confirma=="n"):
			return menu(usuario)

	newSaldo= monto -(float(cantidad)/cotizacion)	#saldo tras la transaccion
	usuario.setSaldo(moneda(select), newSaldo)		#actualiza saldo
	Transaccion(usuario.codUsuario, destinatario, moneda(select), (float(cantidad)/cotizacion), 'TRANSFERENCIA')#objeto correspondiente a la nueva transaccion

	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("SU OPERACIÓN FUE REALIZADA CON ÉXITO")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	input("Presione ENTER para continuar...")
	return menu(usuario)

def mostrarBalance(usuario):	#Muestra el saldo de una moneda seleccionada
	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("MOSTRAR BALANCE:\n")
	print("MONEDA:")
	print("1- "+ moneda(1))
	print("2- "+ moneda(2))
	print("3- "+ moneda(3))
	print("4- "+ moneda(4))
	print("5- "+ moneda(5))
	print("6- "+ moneda(6))
	print("7- "+ moneda(7))
	print("8- "+ moneda(8))
	print("9- VOLVER...")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	
	select=validarInt(input("Ingrese el numero que corresponda a la moneda deseada..."))
	if (select==9):
		return (menu(usuario))
	if (not (0<select<9)):
		return (mostrarBalance(usuario))
	
	monto= formatFloat(usuario.getSaldo(moneda(select)))	#monto actual de la billetera seleccionada
	cotizacion = obtenerCotizacion(moneda(select))			#cotizacion actual de la moneda
	saldo = float(monto) * float(cotizacion)				#saldo actual de la billetera
	
	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("MOSTRAR BALANCE:\n")
	print("Usted tiene: \t" + str(monto) + "\t" + str(moneda(select)) + "\n")
	print("Cotización actual: \t$" + str(cotizacion) + " USD por " + moneda(select) + "\n")
	print("Su SALDO actual es: \t$" + str(formatFloat(saldo)) + " USD")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	input("Presione ENTER para continuar...")
	return menu(usuario)

def mostrarBalanceGral(usuario):#muestra el saldo de todas la billeteras disponibles
	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("MOSTRAR BALANCE:\n")
	total=0.0	#variable para la sumatoria de todas las billeteras
	for x in range(1, 8):
		monto= formatFloat(usuario.getSaldo(moneda(x)))
		cotizacion = obtenerCotizacion(moneda(x))
		saldo = float(monto) * float(cotizacion)
		total= total + saldo
		print("--------------------------------------------------")
		print(str(x) + "-\t" + moneda(x) + ":")
		print("\tCANTIDAD:\t" + str(monto) )
		print("\tCOTIZACIÓN actual (USD):\t$" + str(cotizacion))
		print("\tTOTAL:\t$" + str(formatFloat(saldo))+ "USD")
	print("--------------------------------------------------")
	print("\nSU TOTAL EN USD: \t$" + str(formatFloat(total)) + "\n")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	input("Presione ENTER para continuar...")
	return(menu(usuario))

def historico(usuario):	#muestra todas las transacciones realizadas
	limpiarPantalla()
	print("--------------------------------------------------")
	for trans in Transaccion.listaTransacciones:
		print("\nTRANSACCIÓN NÚMERO: \t" + formatCod(trans.codTrans.getCodigo()))		
		print("\nFECHA: \t\t" + str(trans.fecha))
		print("\nOPERACION: \t" + str(trans.operacion))
		print("\nREMITENTE: \t" + formatCod(trans.remitente))
		print("\nDESTINATARIO: \t" + formatCod(trans.destinatario))
		print("\nMONTO: \t\t" + str(trans.monto))
		print("\nMONEDA: \t" + str(trans.moneda))
		print("--------------------------------------------------")
	input("Presione ENTER para continuar...")
	return(menu(usuario))

def terminarOperacion():	#finaliza la ejecucion del sistema
	limpiarPantalla()
	print("--------------------------------------------------------------------------------------------------------------------------------")
	print("GRACIAS POR OPERAR CON E-WALLET")
	print("--------------------------------------------------------------------------------------------------------------------------------")
	time.sleep(2)
	limpiarPantalla()
	quit()

def obtenerCotizacion(crypto):	#metodo para buscar la cotizacion de las monedas con la API de coin market cap
	url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
	parameters = {
		'Bitcoin (BTC)':{'amount':'1',
  		'symbol':'BTC',
  		'convert':'USD'},
  		'Ethereum (ETH)':{'amount':'1',
  		'symbol':'ETH',
  		'convert':'USD'},
  		'XRP':{'amount':'1',
  		'symbol':'XRP',
  		'convert':'USD'}, 
   		'Bitcoin Cash (BCH)':{'amount':'1',
  		'symbol':'BCH',
  		'convert':'USD'}, 	
   		'Litecoin (LTC)':{'amount':'1',
  		'symbol':'LTC',
  		'convert':'USD'}, 
   		'EOS':{'amount':'1',
  		'symbol':'EOS',
  		'convert':'USD'},
    	'Binance Coin (BNB)':{'amount':'1',
  		'symbol':'BNB',
  		'convert':'USD'},
    	'Tezos (XTZ)':{'amount':'1',
  		'symbol':'XTZ',
  		'convert':'USD'},
  		}
	headers = {
  		'Accepts': 'application/json',
  		'X-CMC_PRO_API_KEY': 'b834956f-b66d-4321-8ab1-bb13913477f7',
  		}

	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(url, params=parameters[crypto])
		data = json.loads(response.text)
		return(float(data['data']['quote']['USD']['price'])) #devuelve la cotizacion de la amoneda seleccionada
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		limpiarPantalla()
		print(e)
		print("--------------------------------------------------------------------------------------------------------------------------------")
		print("ERROR: verifique su conexión a internet...")
		print("--------------------------------------------------------------------------------------------------------------------------------")
		time.sleep(3)
		return(0)

main()		#Llamada al metodo principal