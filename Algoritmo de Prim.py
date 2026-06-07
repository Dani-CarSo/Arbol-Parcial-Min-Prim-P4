import matplotlib.pyplot as plt
import networkx as nx
import time

def algoritmo_prim_animado(vertices, aristas, nodo_inicio=0):
    
    # 1. Crear el grafo completo usando NetworkX
    G = nx.Graph()
    for u, v, w in aristas:
        G.add_edge(u, v, weight=w)
        
    # Inicialización de estructuras para Prim
    visitados = {nodo_inicio}
    aristas_mst = []
    costo_total = 0
    
    # Para guardar los "frames" de la animación
    pasos_graficos = []
    # Guardamos el estado inicial (solo el nodo de inicio visitado)
    pasos_graficos.append((set(visitados), list(aristas_mst)))

    print("=" * 50)
    print(# Al utilizar LaTeX para representar conjuntos matemáticos complejos, se encierra entre signos de dólar:
f"Iniciando Algoritmo de Prim desde el Nodo: {nodo_inicio}")
    print("=" * 50)

    # El MST debe tener exactamente V - 1 aristas
    while len(visitados) < len(vertices):
        min_arista = None
        min_peso = float('inf')
        
        # Buscar la arista con el menor peso que conecte el MST con un nodo no visitado
        for u, v, data in G.edges(data=True):
            w = data['weight']
            # Un extremo debe estar visitado y el otro no
            if u in visitados and v not in visitados:
                if w < min_peso:
                    min_peso, min_arista = w, (u, v)
            elif v in visitados and u not in visitados:
                if w < min_peso:
                    min_peso, min_arista = w, (v, u)

        if min_arista:
            u, v = min_arista
            visitados.add(v)
            aristas_mst.append((u, v, min_peso))
            costo_total += min_peso
            
            # Guardar estado para la animación
            pasos_graficos.append((set(visitados), list(aristas_mst)))
            
            # Paso a paso en consola
            print(f"-> Añadida arista ({u} - {v}) con peso {min_peso}")
            print(f"   Nodos visitados actualmente: {sorted(list(visitados))}\n")
        else:
            print("El grafo no es conexo. No se puede formar un MST completo.")
            break

    print("=" * 50)
    print(f"¡MST Completado! Costo Total: {costo_total}")
    print("=" * 50)
    
    # --- PARTE GRÁFICA ANIMADA ---
    print("\n[Abriendo interfaz gráfica... Cierra la ventana del grafo para terminar]")
    
    # Fijar las posiciones de los nodos para que no se muevan entre pasos
    pos = nx.spring_layout(G, seed=42) 
    
    # Habilitar modo interactivo de matplotlib
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for i, (vis, aristas_actuales) in enumerate(pasos_graficos):
        ax.clear()
        ax.set_title(f"Algoritmo de Prim - Paso {i}\nNodos en MST: {sorted(list(vis))}", fontsize=14)
        
        # 1. Dibujar todos los nodos (Gris por defecto)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightgray', node_size=700)
        # Resaltar los nodos que ya pertenecen al MST (Azul)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=list(vis), node_color='skyblue', node_size=700)
        
        # 2. Dibujar todas las aristas del grafo original (Gris claro)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gainsboro', width=1.5)
        
        # Resaltar las aristas que ya forman parte del MST (Rojo grueso)
        if aristas_actuales:
            edges_mst = [(u, v) for u, v, w in aristas_actuales]
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges_mst, edge_color='crimson', width=3.5)
            
        # 3. Etiquetas de los nodos y pesos de las aristas
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_family='sans-serif')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10, ax=ax)
        
        plt.draw()
        plt.pause(1.5)  # Pausa de 1.5 segundos por paso para apreciar el cambio
        
    plt.ioff() # Desactivar modo interactivo al terminar
    plt.show()

# --- DATOS DE PRUEBA ---
# Lista de vértices
nodos = [0, 1, 2, 3, 4]

# Lista de aristas en formato (nodo_origen, nodo_destino, peso)
conexiones = [
    (0, 1, 4),
    (0, 2, 2),
    (1, 2, 3),
    (1, 3, 2),
    (1, 4, 3),
    (2, 3, 4),
    (3, 4, 1)
]

# Ejecutar el algoritmo
algoritmo_prim_animado(nodos, conexiones, nodo_inicio=0)