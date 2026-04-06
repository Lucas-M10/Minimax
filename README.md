# Descripción
Este proyecto implementa un juego en el que un raton debe escapar de un gato y llegar a la puerta de salida con cierto numero de intentos dentro
de un tablero.
El raton es controlado por el usuario y mientras que el gato utiliza un algoritmo **Minimax** para la toma de decisiones optimas.

# Tecnica de programacion 
Para este proyecto se utilizó **Programación Orientada a Objetos (POO)**, ya que permite organizar mejor el código, separar responsabilidades entre clases y facilitar la reutilización de funciones.

# Generacion del tablero.
Para la la generacion del tablero se utilizo una grilla te tamaño nxn, 
Las posiciones iniciales del ratón, el gato y la salida se generan de forma aleatoria en una funcion, asegurando que:
- No coincidan entre si.
- Mantengan una distancia minima para evitar posiciones iniciales desfavorables.

# Algoritmo Utilizado 
El algoritmo utilizado fue minimax que es un algoritmo recursivo de toma de desiciones el cual simula los movimientos posibles en base al estado del juego hasta cierta 
profundidad dada y evalua los resultados considerando ambos jugadores:

- Raton(MAX): busca maximizar su ventaja contra el gato.
- Gato (MIN): busca minimazar la ventaja del raton o las posibilidades.

# Heuristica
Se utiliza una funcion de evaluacion basada en la **Distancia Manhattan**. Esta calcula la suma de la diferencia absolta de las cordenadas de los personajes y devolver un valor numerico que representa que tan bueno es el estado del juego para el algoritmo o para el usuario: 

- Si el gato está lejos y la salida cerca → mejor para el ratón 
- Si el gato está cerca y la salida lejos → mejor para el gato Además: 
- +999 → gana el ratón 
- -999 → gana el gato

# Posibles mejoras
- Agregar obstaculos en el tablero que nos hagan perder turno.
- Implementar sistema de puntaje (por ejemplo: estrellas según desempeño)   
- Implementar diferentes niveles de dificultad.
- Mejorar la interzas grafica.