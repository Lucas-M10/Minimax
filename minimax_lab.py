import random

#Esta clase representa el estado del juego en un instante entonce estan todo lo que se veria en el tablro y cuando turno queda 
class Estado :
    def __init__(self, raton:tuple, gato:tuple, turno: str, salida:tuple, turno_res:int):

        self.raton = raton              #Posicion del raton
        self.gato = gato                #Posion del gato
        self.turno = turno              #El turno alcual de los jugadores
        self.salida = salida            #Posicion de la casilla de salida
        self.turno_res = turno_res      #Los turnos restantes del juego

    def copiar (self):
        return Estado(self.raton, self.gato, self.turno, self.salida, self.turno_res)
    
#esta clase se encarga del cuerpo del juego donde haremos validacion y generaremos cosas seria el cuerpo a diferencia del main que es el que manda que hacer con el cuerpo 
class Juego : 

    #este es el contructor de la clase juego que es en donde le pasaremos la dimension del tablero 
    #le paso una dimanesion porque sera una matriz cuadrada de n*n 
    def __init__(self, columna, fila ):
        self.columna = columna
        self.fila = fila

    #genera el tablero 
    def generar_tablero (self, estado:Estado):
        tablero = []

        for i in range(self.fila):
            aux = []

            for x in range (self.columna):
                aux.append (' [] ')
            
            tablero.append(aux)

        x_raton, y_raton = estado.raton
        x_gato, y_gato = estado.gato
        x_salida, y_salida = estado.salida

        tablero[x_raton][y_raton] = ' 🐭 '
        tablero[x_gato][y_gato] = ' 🐱 '
        tablero[x_salida][y_salida] = ' 🚪 '

        return tablero
       

    #en esta funcion validamos si el movimiento es decir si se puede mover a esa direccion o no 
    def validar_move (self, posicion_actual:tuple, new_posicion:tuple):
        x, y = posicion_actual
        new_x, new_y = new_posicion

        #Verificamos si la nueva posicion es valida para realizar el movimiento
        #Si no esta adentro del tablero nos retorna false
        if not (0<= new_x < self.fila and 0<= new_y < self.columna):
            return False        
        
        #Si pasa todas las validaciones de errores que hicimos entonces nos da True
        return True
    
        
    #En esta funcion aplicamos el movimiento llamamos a la funcion 
    def aplicar_move (self, estado_actual:Estado, new_posicion:tuple):

        #Realizamos una copia del estado del juego actual para no modificar el original
        copia_estado = estado_actual.copiar()

        #Con este if verificamos el turno del estado_actual del juego si es raton entonces se modifica la posicion del raton y modificamos el turno del juego actual
        if estado_actual.turno == "raton":
            copia_estado.raton = new_posicion
            copia_estado.turno = "gato"

        else:
            copia_estado.gato = new_posicion
            copia_estado.turno = "raton"

        #retornamos la variable que sera ahora el estado actual
        return copia_estado
    

    #Aca verificamos si el juego ya termino si el gato atrapo al raton o si el raton ya llego a la salida o si el turno termino
    def estado_juego (self, estado_actual:Estado):#Caso base 

        #Aca verificamos si la posicion del raton y del gato son iguales para ver si el juego termino 
        if estado_actual.raton == estado_actual.gato:
            return 'gato'
        
        #Aca verificamos si la posicion del raton es igual a la posicion de la salida entonces T
        if estado_actual.raton == estado_actual.salida:
            return 'raton'
        
        #Aca verificamos si hay turnos disponibles por jugar
        if estado_actual.turno_res <=0 :
            return 'tiempo'
        
        return None
    
    #Aca se verifica el estado del juego en base a un valor numerico que refleja que tan bueno o malo es la posicion actual
    def evaluar (self, estado: Estado):

        #Gana el gato 
        if estado.gato == estado.raton:
            return -999
        
        #Gana el raton
        if estado.raton == estado.salida:
            return 999
        
        #Se termino el tiempo pierde el raton
        if estado.turno_res <=0:
            return -999
        
        #Ahora calculamos la distancia:
        #coordenadas de gato
        x_gato, y_gato = estado.gato

        #Sacamos coordenadas del raton
        x_raton, y_raton = estado.raton

        #Sacamos coordenadas de la salida 
        x_salida, y_salida = estado.salida

        #sacamos la distancia que esta el raton del gato
        #Concepto aplicado de distancia Manhattan 
        distancia_gato = abs (x_gato - x_raton) + abs (y_gato - y_raton) 

        #Calculamos la distancia que se encontra el rato de la salida
        distancia_salida = abs (x_raton - x_salida) + abs (y_raton - y_salida)

        return distancia_gato - distancia_salida
    
    #Esta funcion analiza todos los movimientos posibles y devuelve solo los movimientos validados 
    def movimientos_validos (self, pos_actual:tuple):

        x, y = pos_actual
        validos = []

        posibles = [ (x+1, y),
                     (x, y+1),
                     (x-1, y),
                     (x, y-1)
                    ]

        for  nuevas_pos in posibles:
            if self.validar_move(pos_actual, nuevas_pos ) :
                validos.append (nuevas_pos)

        return validos

    #este seria el algoritmo que se encarga de devorlver el valor en base a los movimientos generados
    def minimax (self, estado:Estado, profundidad:int, turno_raton:bool):
        #Estado sera la copia actual del estado del juego
        #profundidad: cuantos turnos tiene por delante #MEJORAR EL CONCEPTO
        #turno_raton: True:turno del raton y False: Turno del gato

        resultado = self.estado_juego (estado)


        #Aca se verifica si el  estado del juego si gano o perdio el raton
        if resultado is None or profundidad==0:
            return self.evaluar(estado)

        #Verifica si es el turno del raton #MAX
        if turno_raton:
            mejor_valor = float ('-inf')

            for new_move in self.movimientos_validos (estado.raton):     # Itera en las posibilidades de movimientos 
                nuevo = self.aplicar_move (estado, new_move)             # Simula el movimiento el estado siguiente despues del movimiento
                valor = self.minimax (nuevo, profundidad-1, False)       # aca se realiza la recursividad ss encarga de cambiar el turno y mandar la nueva posicion
                mejor_valor = max (mejor_valor, valor)                   # Aca compara el mejor valor posible y elije el mejor
                                
            return mejor_valor
            
        #Si no es el turno del raton entonces el del gato #MIN
        else:
            mejor_valor = float ('inf')

            for new_move in self.movimientos_validos(estado.gato):
                nuevo = self.aplicar_move (estado, new_move)
                valor = self.minimax (nuevo, profundidad-1, True)
                mejor_valor = min (mejor_valor, valor)

            return mejor_valor

        
def generar_posiciones (columna, fila):

    while True:
        raton = (
            random.randint (0, fila -1),
            random.randint (0, columna -1)
        )

        gato = (
            random.randint (0, fila -1),
            random.randint (0, columna -1)
        )

        salida = (
            random.randint (0, fila -1),
            random.randint (0, columna -1)
        )

        if raton==gato or raton == salida or gato == salida:
            continue

        distancia = abs (raton[0]-gato[0]) + abs (raton[1]-gato[1])

        distancia_salida = abs (raton[0]- salida[0])+ abs(raton[1]-salida[1])

        if distancia >= 4 and distancia_salida >= 5:
            return raton, gato, salida
        

def main():
    
    columna = 10
    fila = 10
    # tablero = (columna, fila)
    juego  = Juego (columna, fila)
    
    #se genera las posiciones
    raton, gato, salida = generar_posiciones (columna, fila)

    #Estado inicial del juego 
    estado = Estado(raton, gato, "raton", salida, 30)

    #Que profundidad va a tener nuestro algoritmo 
    profundidad = 5

    print ('''
🐭 Escapa del gato antes de que te atrape.
Muévete una celda por turno.
Llega a la salida para ganar.
Cuidado: el gato cuando esta bien despierto es un cazador experto 🐱
''')

    while True:

        tablero = juego.generar_tablero (estado)

        for fila in tablero:
            print (' '.join(fila))


        resultado = juego.estado_juego (estado)

        if not resultado is None:
            break
        
        #TURNO DEL RATON 🐭
        if estado.turno == 'raton':
            
            print ("\n Turno del 🐭")
            cargar_movimiento = input ('selecciona el movimiento arriba(w) abajo (s) izquierda (a) derecha (d): ').lower().strip ()
            x, y = estado.raton

            if cargar_movimiento == 'w':
                nueva_pos = (x-1, y)

            elif cargar_movimiento == 's':
                nueva_pos = (x+1, y)

            elif cargar_movimiento == 'a':
                nueva_pos = (x, y-1)
            
            elif cargar_movimiento == 'd':
                nueva_pos = (x, y+1)

            else:
                print ("Error! valor incorrecto ")
                continue
        
            if juego.validar_move(estado.raton, nueva_pos):
                estado = juego.aplicar_move(estado, nueva_pos)
        
            else:
                print ('Error! Posicion invalida')
                continue

        #TURNO DEL GATO 🐱
        else:
            print ("Truno del 🐱")
            
            movimientos = juego.movimientos_validos(estado.gato)

            #Se aplica minimax para el gato 
            if estado.turno_res < 24: 
                print ("EL GATO YA SE DESPERTO POR COMPLETO CUIDADO")

                mejor_valor = float ('inf')
                mejor_move = None

                for mov in movimientos:                  #analiza las posibilidades de movimientos 
                
                    nuevo_estado = juego.aplicar_move (estado, mov)                 #Simula el movimiento 
                    valor = juego.minimax (nuevo_estado, profundidad-1, True)       

                    if valor < mejor_valor:                                         #Verificamos si el valor que paso la funcion minimax es mejor 
                        mejor_valor = valor
                        mejor_move = mov
            
            else:
                mejor_move = random.choice (movimientos)
            
            estado = juego.aplicar_move (estado, mejor_move)

        
        estado.turno_res -= 1

        print (f'''Gato: {estado.gato}  Raton: {estado.raton}   Turnos restantes: {estado.turno_res}''')

    
    resultado = juego.estado_juego (estado)

    if resultado == 'gato':
        print ("GAME OVER: El gato te encontro")

    elif resultado == 'raton':
        print ('!WINNER: Lograste escapar del gato')

    elif resultado == 'tiempo':
        print ('GAME OVER: Se termino el tiempo')


if __name__ == '__main__':
    main()
        