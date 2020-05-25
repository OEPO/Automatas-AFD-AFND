import graphviz as gv

# Todos los parámetros son listas o tuplas
# donde:
#  * alfabeto:  es el alfabeto aceptado por el 
#               autómata.
#  * estados:   es una lista de estados aceptados
#               por el autómata.
#  * inicio:    Son los estados de inicio del fsm.
#  * trans:     Es una tupla de funciones de transición
#               con tres elementos que son: (a,b,c) donde
#               (a,b) son los estados de partida y llegada;
#               mientras que c es la letra que acepta.
#  * final      Son los estados finales del autómata.

def draw(alfabeto, estados, inicio, trans, final, nombre):
    print("inicio:", str(inicio))
    g = gv.Digraph(filename=nombre ,format='png')
    g.graph_attr['rankdir'] = 'LR'
    g.node('ini', shape="point")
    for e in estados:
        if e in final:
            g.node(e, shape="doublecircle")
        else:
            g.node(e)
        if e in inicio:
            g.edge('ini',e)

    for t in trans:
        if t[2] not in alfabeto:
            return 0
        g.edge(t[0], t[1], label=str(t[2]))
    g.render(nombre, view=True)


def graph (automata, nombre):
  nombre = nombre + '.sv'
  listaEstadosFinal=[]
  for a in automata.final_states:
    listaEstadosFinal.append(a)

  EstadoInicial = [automata.initial_state]

  listaEstados=[]
  for d in automata.states:
    listaEstados.append(d)

  listaSimbolo=[]
  for c in automata.input_symbols:
    listaSimbolo.append(c)

  listaTransicion = []
  for i in automata.transitions:
    for h in automata.input_symbols:
      listaTransicion.append((i,automata.transitions[i][h],h))

  draw(listaSimbolo, listaEstados, EstadoInicial, listaTransicion, listaEstadosFinal, nombre)
