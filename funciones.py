from automata.fa.dfa import DFA   #Libreria Automata
from automata.fa.nfa import NFA
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

# https://github.com/caleb531/automata

def union (automata1, tipo1, automata2, tipo2):
  # Crear un estado inicial y juntar 2 automatas
  simbolos = []
  for i in automata1.input_symbols:
    simbolos.append(i)
  for a in automata2.input_symbols:
    simbolos.append(a)
  simbolos.append('')
  
  estados = []
  for i in automata1.states:
    estados.append(i)
  for a in automata2.states:
    estados.append(a)
  estados.append('inicio')

  final = []
  for i in automata1.final_states:
    final.append(i)
  for a in automata2.final_states:
    final.append(a)

  dic1 = automata1.transitions.copy()
  dic2 = automata2.transitions.copy()
  dic1.update(dic2)

  if tipo1 == tipo2:
    if tipo1==True:
      #naf {}
      dic1['inicio'] = {'': {automata1.initial_state, automata2.initial_state}}

      automata = NFA(
        states=set(estados),
        input_symbols= set(simbolos),
        transitions=dic1,
        initial_state='inicio',
        final_states= set(final)
        )
      imprimirAutomata(automata)
      return automata, tipo1
        
# Formato dfa:  'q0': {'0': 'q0', '1': 'q1'},
    else:
      print('no se llama')
# Formato nfa:  'q1': {'0': {'q1'}, '1': {'q2'}},
  else:
    print ('error en union') 

def complemento (automata, tipo):  # Solo AFD
  #intercambiar estados finales por estados
  if tipo == False :
    
    fin = []
    final= automata.final_states
    estados = automata.states

    for i in estados:
      for l in final:
        if i != l:
          fin.append(i)
    
    finales = set(fin)

    automata = DFA(
      states=automata.states,
      input_symbols=automata.input_symbols,
      transitions=automata.transitions,
      initial_state=automata.initial_state,
      final_states= finales
    )
    print ('complemento ok ')
    return automata , tipo
  
  else: 
    print('No es AFD')
    ADF = NFA.from_dfa(automata)  #Crea un automata determinista a uno no determinista
    complemento(ADF,False)

def concatenacion (automata1, tipo1, automata2 , tipo2 ):  # entran 2 NFA y no se saca la chucha :)

  simbolos = []
  #Saca Los simbolos de el automata 1 y 2
  for i in automata1.input_symbols:
    simbolos.append(i)
  for a in automata2.input_symbols:
    simbolos.append(a)
  simbolos.append('')
  sim = set(simbolos)

  estados = []
  #Saca los estados de los automatas 1 y 2
  for i in automata1.states:
    estados.append(i)
  for a in automata2.states:
    estados.append(a)
  esta=set(estados)

  dic1 = automata1.transitions.copy()
  dic2 = automata2.transitions.copy()
  dic1.update(dic2)

  if tipo1 == tipo2:
    print ('aqui se supone que lo hace qweqwe ')
    if tipo1 == True:
      dic1[str(automata1.final_states)[2:4]][''] = {str(automata2.initial_state)}

      automata = NFA(
        states=esta,
        input_symbols= sim,
        transitions=dic1,
        initial_state=automata1.initial_state,
        final_states= set(automata2.final_states)
        )
      print ('aqui se supone que lo hace ')
      return automata, tipo1

    else:
      print('no se llama')
  else:
    return print('error')
    

def interseccion (automata1, tipo1, automata2, tipo2): # ingresan 2 automatas afd y salen 1 afnd 
  
  if tipo1 == tipo2:
    if tipo1 == False:
      automata1, tipo1 = complemento (automata1, tipo1)
      automata1 = NFA.from_dfa(automata1)
      tipo1 = True
      automata2, tipo2 = complemento (automata2, tipo2)
      automata2 = NFA.from_dfa(automata2)
      tipo2 = True
    else:
      print('no se llama la interseccion')
  else:
    return print('error: los automatas no son afd ')
  return union (automata1, tipo1, automata2, tipo2)
  

#Funciones para graficar automata
def imprimirAutomata(automata):

  print ('initial_state : ', automata.initial_state)
  print ('final_states : ', automata.final_states)
  print ('states : ', automata.states)  
  print ('input_symbols : ', automata.input_symbols)
  print ('transitions : ', automata.transitions)


def graph (automata, tipo, aux): # automata , bool 
  
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
  if tipo == False: #dfa
    nombre = 'dfa'
    for k,v in automata.transitions.items():
      for i in v:
        listaTransicion.append(( k, v[i], i))

  else:#nfa
    nombre = 'nfa'
    for k,v in automata.transitions.items():
      for i in v:
        for j in v[i]:
          listaTransicion.append(( k,j, i))

# q0:{'0':{q1,q0}}--> (q0,q1,0)(q0,q0,0)
  aux = aux + 1
  nombre = nombre + str(aux) + '.sv'
  draw(listaSimbolo, listaEstados, EstadoInicial, listaTransicion, listaEstadosFinal, nombre)
  return aux

def draw( simbolos, estados, inicio, trans, final, nombre):

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
        if t[2] not in simbolos:
            return 0
        g.edge(t[0], t[1], label=str(t[2]))
    g.render(nombre, view=True)