# Ambos ejercicios estan en el mismo código marcado con mensajes :)
import bisect


class NodoIngrediente:
    """Representa un nodo de la lista simplemente enlazada de ingredientes."""

    def __init__(self, nombre: str):
        self.nombre = nombre.strip().capitalize()
        self.siguiente = None  # Equivalente a NIL en el diagrama


class Postre:
    """Representa una celda del arreglo POSTRES (Nombre + Puntero a la lista)."""

    def __init__(self, nombre: str):
        self.nombre = nombre.strip().capitalize()
        self.cabeza_ingredientes = None  # NIL por defecto (lista vacía)

    # Permite mantener el arreglo ordenado alfabéticamente con bisect
    def __lt__(self, otro):
        return self.nombre.lower() < otro.nombre.lower()


class EstructuraPostres:

    def __init__(self):
        self.postres = []  # Arreglo principal POSTRES

    def _buscar_indice_postre(self, nombre_postre: str) -> int:
        """Búsqueda binaria para localizar un postre de manera eficiente O(log n)."""
        nombre_limpio = nombre_postre.strip().capitalize()
        izquierda, derecha = 0, len(self.postres) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            actual = self.postres[medio].nombre
            if actual.lower() == nombre_limpio.lower():
                return medio
            elif actual.lower() < nombre_limpio.lower():
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return -1

    # ==========================================
    # a. Imprimir la lista de ingredientes
    # ==========================================
    def imprimir_ingredientes(self, nombre_postre: str):
        if not self.postres:
            print("[!] Caso: El arreglo POSTRES está completamente vacío.")
            return

        idx = self._buscar_indice_postre(nombre_postre)
        if idx == -1:
            print(
                f"[!] Caso: El postre '{nombre_postre}' no existe en el arreglo."
            )
            return

        postre = self.postres[idx]
        actual = postre.cabeza_ingredientes

        if actual is None:
            print(
                f"[*] Postre '{postre.nombre}': Su lista de ingredientes está vacía ( -> NIL )."
            )
            return

        cadena_nodos = []
        while actual is not None:
            cadena_nodos.append(f"[{actual.nombre}]")
            actual = actual.siguiente

        print(
            f"[*] Ingredientes de '{postre.nombre}': "
            + " -> ".join(cadena_nodos)
            + " -> NIL"
        )

    # ==========================================
    # b. Insertar nuevos ingredientes a su lista
    # ==========================================
    def insertar_ingredientes(
        self,
        nombre_postre: str,
        lista_nuevos: list,
        permitir_duplicados: bool = False,
    ):
        if not self.postres:
            print(
                "[!] Caso: El arreglo POSTRES está vacío. Dé de alta un postre primero."
            )
            return

        idx = self._buscar_indice_postre(nombre_postre)
        if idx == -1:
            print(
                f"[!] Caso: No se pueden insertar ingredientes porque '{nombre_postre}' no existe."
            )
            return

        if not lista_nuevos:
            print("[!] Caso: No se proporcionaron ingredientes para insertar.")
            return

        postre = self.postres[idx]

        for ing in lista_nuevos:
            ing_limpio = ing.strip().capitalize()
            if not ing_limpio:
                continue

            nuevo_nodo = NodoIngrediente(ing_limpio)

            # Caso 1: La lista del postre apunta a NIL (está vacía)
            if postre.cabeza_ingredientes is None:
                postre.cabeza_ingredientes = nuevo_nodo
                print(
                    f"[+] '{ing_limpio}' insertado como primer nodo (cabeza) en '{postre.nombre}'."
                )
            else:
                # Caso 2: Recorrer hasta el final verificando si ya existe
                actual = postre.cabeza_ingredientes
                duplicado = False
                while True:
                    if (
                        actual.nombre.lower() == ing_limpio.lower()
                        and not permitir_duplicados
                    ):
                        print(
                            f"[!] Caso: El ingrediente '{ing_limpio}' ya existe en '{postre.nombre}'. Se omite."
                        )
                        duplicado = True
                        break
                    if actual.siguiente is None:
                        break
                    actual = actual.siguiente

                if not duplicado:
                    actual.siguiente = nuevo_nodo
                    print(
                        f"[+] '{ing_limpio}' enlazado al final de la lista de '{postre.nombre}'."
                    )

    # ==========================================
    # c. Eliminar alguno de sus ingredientes
    # ==========================================
    def eliminar_ingrediente(
        self, nombre_postre: str, nombre_ingrediente: str
    ):
        if not self.postres:
            print("[!] Caso: El arreglo POSTRES está vacío.")
            return

        idx = self._buscar_indice_postre(nombre_postre)
        if idx == -1:
            print(f"[!] Caso: El postre '{nombre_postre}' no está registrado.")
            return

        postre = self.postres[idx]
        actual = postre.cabeza_ingredientes

        # Caso 1: Lista de ingredientes vacía (NIL)
        if actual is None:
            print(
                f"[!] Caso: '{postre.nombre}' no tiene ingredientes registrados (apunta a NIL)."
            )
            return

        ing_limpio = nombre_ingrediente.strip().capitalize()

        # Caso 2: El ingrediente a eliminar está en la cabeza (primer nodo)
        if actual.nombre.lower() == ing_limpio.lower():
            postre.cabeza_ingredientes = actual.siguiente
            actual.siguiente = None  # Desvincular nodo
            print(
                f"[-] Ingrediente '{ing_limpio}' eliminado (era la cabeza de la lista de '{postre.nombre}')."
            )
            return

        # Caso 3: El ingrediente está en un nodo intermedio o al final
        anterior = actual
        actual = actual.siguiente
        while actual is not None:
            if actual.nombre.lower() == ing_limpio.lower():
                anterior.siguiente = actual.siguiente
                actual.siguiente = None
                print(
                    f"[-] Ingrediente '{ing_limpio}' eliminado de la lista de '{postre.nombre}'."
                )
                return
            anterior = actual
            actual = actual.siguiente

        # Caso 4: Se recorrió toda la lista hasta NIL y no se encontró
        print(
            f"[!] Caso: El ingrediente '{ing_limpio}' no pertenece a '{postre.nombre}'."
        )

    # ==========================================
    # d. Dar de alta un postre con sus ingredientes
    # ==========================================
    def alta_postre(
        self,
        nombre_postre: str,
        ingredientes: list,
        forzar_duplicado: bool = False,
    ):
        nombre_limpio = nombre_postre.strip().capitalize()
        if not nombre_limpio:
            print("[!] Caso: El nombre del postre no puede estar vacío.")
            return

        idx = self._buscar_indice_postre(nombre_limpio)
        if idx != -1 and not forzar_duplicado:
            print(
                f"[!] Caso: El postre '{nombre_limpio}' ya existe en el arreglo. Use la opción de insertar ingredientes."
            )
            return

        nuevo_postre = Postre(nombre_limpio)
        # Inserción manteniendo estricto orden alfabético en el arreglo
        bisect.insort(self.postres, nuevo_postre)
        print(
            f"[+] Postre '{nombre_limpio}' dado de alta en orden alfabético."
        )

        if ingredientes:
            # Si se forzó un duplicado para probar el Ejercicio 2, apuntamos a la instancia recién creada
            for p in self.postres:
                if (
                    p is nuevo_postre
                    and ingredientes
                ):
                    for ing in ingredientes:
                        ing_limpio = ing.strip().capitalize()
                        if not ing_limpio:
                            continue
                        nuevo_nodo = NodoIngrediente(ing_limpio)
                        if p.cabeza_ingredientes is None:
                            p.cabeza_ingredientes = nuevo_nodo
                        else:
                            act = p.cabeza_ingredientes
                            while act.siguiente is not None:
                                act = act.siguiente
                            act.siguiente = nuevo_nodo
        else:
            print(
                f"[*] Nota: '{nombre_limpio}' se registró sin ingredientes (puntero -> NIL)."
            )

    # ==========================================
    # e. Dar de baja un postre con sus ingredientes
    # ==========================================
    def baja_postre(self, nombre_postre: str):
        if not self.postres:
            print("[!] Caso: El arreglo POSTRES está vacío; nada que eliminar.")
            return

        idx = self._buscar_indice_postre(nombre_postre)
        if idx == -1:
            print(
                f"[!] Caso: No se puede dar de baja '{nombre_postre}' porque no existe."
            )
            return

        postre_eliminado = self.postres[idx]

        # Desvinculación explícita de los nodos de su lista enlazada (buena práctica en Estructuras de Datos)
        actual = postre_eliminado.cabeza_ingredientes
        while actual is not None:
            temp = actual.siguiente
            actual.siguiente = None
            actual = temp
        postre_eliminado.cabeza_ingredientes = None

        # Eliminación del elemento en el arreglo
        self.postres.pop(idx)
        print(
            f"[-] El postre '{postre_eliminado.nombre}' y toda su lista de ingredientes fueron dados de baja."
        )

    # =========================================================================
    # EJERCICIO 2: Subprograma para eliminar automáticamente elementos repetidos
    # =========================================================================
    def eliminar_repetidos_automatico(self):
        """Elimina tanto postres repetidos en el arreglo POSTRES (fusionando o liberando sus listas)

        como nodos de ingredientes repetidos dentro de cada lista enlazada.
        """
        if not self.postres:
            print("[!] Caso: Estructura vacía, no hay repetidos por eliminar.")
            return

        postres_eliminados = 0
        ingredientes_eliminados = 0

        # 1. Eliminar postres repetidos en el arreglo (aprovechando que está ordenado alfabéticamente)
        i = 0
        while i < len(self.postres) - 1:
            actual = self.postres[i]
            siguiente = self.postres[i + 1]

            if actual.nombre.lower() == siguiente.nombre.lower():
                # Fusionamos los ingredientes del postre repetido hacia el original antes de borrarlo
                # para no perder información de la segunda lista enlazada
                nodo_dup = siguiente.cabeza_ingredientes
                if actual.cabeza_ingredientes is None:
                    actual.cabeza_ingredientes = nodo_dup
                else:
                    cola = actual.cabeza_ingredientes
                    while cola.siguiente is not None:
                        cola = cola.siguiente
                    cola.siguiente = nodo_dup

                # Desvinculamos el puntero del registro repetido y lo sacamos del arreglo
                siguiente.cabeza_ingredientes = None
                self.postres.pop(i + 1)
                postres_eliminados += 1
            else:
                i += 1

        # 2. Eliminar nodos de ingredientes repetidos dentro de la lista enlazada de cada postre
        for postre in self.postres:
            vistos = set()
            nodo_actual = postre.cabeza_ingredientes
            nodo_anterior = None

            while nodo_actual is not None:
                clave = nodo_actual.nombre.lower()
                if clave in vistos:
                    # El ingrediente está repetido: puenteamos el puntero del nodo anterior
                    nodo_anterior.siguiente = nodo_actual.siguiente
                    temp = nodo_actual
                    nodo_actual = nodo_actual.siguiente
                    temp.siguiente = None  # Liberar referencia del nodo eliminado
                    ingredientes_eliminados += 1
                else:
                    vistos.add(clave)
                    nodo_anterior = nodo_actual
                    nodo_actual = nodo_actual.siguiente

        print(
            f"[✓] Depuración completada: {postres_eliminados} postre(s) repetido(s) y "
            f"{ingredientes_eliminados} ingrediente(s) repetido(s) eliminados."
        )

    def mostrar_estructura_completa(self):
        print("\n================ ESTRUCTURA POSTRES ================")
        if not self.postres:
            print("  [ Arreglo Vacío ]")
        for i, postre in enumerate(self.postres):
            actual = postre.cabeza_ingredientes
            nodos = []
            while actual is not None:
                nodos.append(f"[{actual.nombre}]")
                actual = actual.siguiente
            lista_str = " -> ".join(nodos) + " -> NIL" if nodos else "NIL"
            print(f"  [{i}] {postre.nombre:<15} | -> {lista_str}")
        print("====================================================\n")


# ==========================================
# Bloque de prueba y menú interactivo
# ==========================================
if __name__ == "__main__":
    sistema = EstructuraPostres()

    # Carga de demostración inicial (incluyendo casos límite y repetidos para el Ejercicio 2)
    print("--- EJECUTANDO PRUEBAS DE CASOS Y DEMOSTRACIÓN ---")
    sistema.alta_postre("Flan", ["Leche", "Huevo", "Azúcar", "Vainilla"])
    sistema.alta_postre("Arroz con leche", ["Arroz", "Leche", "Canela"])
    sistema.alta_postre("Gelatina", [])  # Caso: Postre con puntero directo a NIL
    sistema.mostrar_estructura_completa()

    # Prueba de inserción y eliminación de ingredientes
    sistema.insertar_ingredientes("Gelatina", ["Agua", "Grenetina"])
    sistema.eliminar_ingrediente("Flan", "Leche")  # Eliminando la cabeza
    sistema.eliminar_ingrediente("Flan", "Chocolate")  # Caso: Ingrediente que no existe

    # Forzando elementos repetidos para demostrar el Ejercicio 2
    print("\n--- INSERTANDO ELEMENTOS REPETIDOS PARA EL EJERCICIO 2 ---")
    sistema.alta_postre("Flan", ["Caramelo", "Huevo"], forzar_duplicado=True)
    sistema.insertar_ingredientes(
        "Arroz con leche", ["Canela", "Pasas"], permitir_duplicados=True
    )
    sistema.mostrar_estructura_completa()

    print("--- EJECUTANDO SUBPROGRAMA DE ELIMINACIÓN DE REPETIDOS (EJERCICIO 2) ---")
    sistema.eliminar_repetidos_automatico()
    sistema.mostrar_estructura_completa()