class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar(valor, self.raiz)

    def _insertar(self, valor, nodo):
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar(valor, nodo.izq)
        else:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar(valor, nodo.der)

    def buscar(self, nodo, dato):
        if nodo == None:
            return False
        else:
            if nodo.valor == dato:
                return True
            else:
                if nodo.valor > dato:
                    return self.buscar(nodo.izq, dato)
                else:
                    return self.buscar(nodo.der, dato)            
    
    def pre_orden(self, nodo):
        if nodo:
            print(nodo.valor, end=" ")
            self.pre_orden(nodo.izq)
            self.pre_orden(nodo.der)

    def en_orden(self, nodo):
        if nodo:
            self.en_orden(nodo.izq)
            print(nodo.valor, end=" ")
            self.en_orden(nodo.der)

    def pos_orden(self, nodo):
        if nodo:
            self.pos_orden(nodo.izq)
            self.pos_orden(nodo.der)    
            print(nodo.valor, end=" ")        

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            # Caso 1: Nodo sin hijos o con un hijo
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            # Caso 2: Nodo con dos hijos
            nodo.valor = self._min_valor(nodo.der)
            nodo.der = self._eliminar(nodo.der, nodo.valor)

        return nodo

    def _min_valor(self, nodo):
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual.valor

    def imprimir_por_niveles(self):
            if self.raiz is None:
                return

            cola = [self.raiz]  # Usamos una lista como cola

            while cola:
                nodo_actual = cola.pop(0)  # Sacamos el primer elemento
                print(nodo_actual.valor, end=" ")

                if nodo_actual.izq:
                    cola.append(nodo_actual.izq)
                if nodo_actual.der:
                    cola.append(nodo_actual.der)

    def imprimir_por_niveles2(self):
        if self.raiz is None:
            return

        cola = [self.raiz]  # Usamos una lista como cola

        while cola:
            nivel_nodos = len(cola)  # Número de nodos en el nivel actual
            nivel = []  # Lista para almacenar los nodos del nivel actual

            while nivel_nodos > 0:
                nodo_actual = cola.pop(0)
                nivel.append(str(nodo_actual.valor))  # Agregamos el nodo a la lista del nivel

                if nodo_actual.izq:
                    cola.append(nodo_actual.izq)
                if nodo_actual.der:
                    cola.append(nodo_actual.der)
                
                nivel_nodos -= 1

            # Imprimir los nodos del nivel actual separados por un delimitador (por ejemplo, " | ")
            print(" | ".join(nivel))
            print("-" * 20)  # Separador visual entre niveles


"""
arbol = ABB()

valores = [7, 3, 10, 1, 5, 9, 12]
for valor in valores:
    arbol.insertar(valor)

print("Recorrido en orden antes de eliminar:")
arbol.en_orden(arbol.raiz)
print('\n')

arbol.eliminar(10)  # Eliminar un nodo con dos hijos

print("Recorrido en orden después de eliminar 10:")
arbol.en_orden(arbol.raiz)
print('\n')

print("Recorrido por niveles:")
arbol.imprimir_por_niveles2()
print(arbol.buscar(arbol.raiz, 7))

print('\n')
"""