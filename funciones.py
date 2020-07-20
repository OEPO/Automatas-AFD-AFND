from automata.fa.dfa import DFA   #Libreria Automata
from automata.fa.nfa import NFA
import graphviz as gv
from graphviz import Digraph
from forms import bcolors
from flask import url_for

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

def crear(sets, tipo):
  if tipo == False :
    automata = DFA(states = sets[0],
                  input_symbols = sets[1],
                  transitions = sets[2],
                  initial_state = sets[3],
                  final_states = sets[4]
    )
  
  else:
    automata = NFA(states = sets[0],
                  input_symbols = sets[1],
                  transitions = sets[2],
                  initial_state = sets[3],
                  final_states = sets[4]
    )
  return automata

def validar(sets, tipo):
  if tipo == False: 
    aux = list(sets[2].values())
    for i in range(len(sets[0])):
      if '' in aux[i].values() or not sets[4] :
        return False
    automata = DFA(states = sets[0],
                  input_symbols = sets[1],
                  transitions = sets[2],
                  initial_state = sets[3],
                  final_states = sets[4]
    )
  else: 
    if sets[4]:
      automata = NFA(states = sets[0],
                  input_symbols = sets[1],
                  transitions = sets[2],
                  initial_state = sets[3],
                  final_states = sets[4]
      )
    else:
      return False
  if automata.validate() :
    del automata
    return True
  else:
    del automata
    return False

def leer(automata, entrada):
  if automata.accepts_input(entrada):
    return 'El automata responde al string finalizando en el estado : '+automata.read_input(entrada)#+automata.read_input_stepwise(entrada)
  else:
    return 'La cadena ingresada no es válida para el automata.'

def AFNDtoAFD (automata, tipo):
  if tipo:
    dfa = DFA.from_nfa(automata) 
    minimal_dfa = dfa.minify()
    return minimal_dfa
  else: 
    return automata

def AFDtoAFND (automata, tipo):
  if tipo==False:
    nfa = NFA.from_dfa(automata) 
    return nfa, True
  else: 
    return automata, tipo 
    
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
  if tipo1 == tipo2: # acepta 2 afnd 
    if tipo1:
      dic1['inicio'] = {'': {automata1.initial_state, automata2.initial_state}}
      automata = NFA(
        states=set(estados),
        input_symbols= set(simbolos),
        transitions=dic1,
        initial_state='inicio',
        final_states= set(final)
        )
      return automata, tipo1
  # Formato dfa:  'q0': {'0': 'q0', '1': 'q1'},
  # Formato nfa:  'q1': {'0': {'q1'}, '1': {'q2'}},
    else:
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      return union (automata1, tipo1, automata2, tipo2)
  else:
    if tipo1:
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      return union (automata1, tipo1, automata2, tipo2)
    if tipo2:
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      return union (automata1, tipo1, automata2, tipo2)

def complemento (automata, tipo):  
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
    return automata , tipo
  else: 
    ADF = NFA.from_dfa(automata)
    complemento(ADF,False)

def concatenacion(automata1, tipo1, automata2, tipo2):  # entran 2 NFA y no se saca la chucha :)
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
  esta2=set(estados)
  dic1 = automata1.transitions.copy()
  dic2 = automata2.transitions.copy()
  dic1.update(dic2)
  if tipo1 == tipo2:
    if tipo1:
      dic1[str(automata1.final_states)[2:4]][''] = {str(automata2.initial_state)}
      automata = NFA(
        states=esta2,
        input_symbols= sim,
        transitions=dic1,
        initial_state=automata1.initial_state,
        final_states= set(automata2.final_states)
        )
      return automata, tipo1
    else:
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      return concatenacion(automata1, tipo1, automata2, tipo2)
  else:
    if tipo1:
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      return concatenacion(automata1, tipo1, automata2, tipo2)
    if tipo2:
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      return concatenacion(automata1, tipo1, automata2, tipo2)
    
def interseccion (automata1, tipo1, automata2, tipo2): # ingresan 2 automatas afd y salen 1 afnd 
  if tipo1 == tipo2:
    if tipo1 == False:
      automata1, tipo1 = complemento (automata1, tipo1)
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      automata2, tipo2 = complemento (automata2, tipo2)
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      automata3, tipo3 = union (automata1, tipo1, automata2, tipo2)
      automata3, tipo3 = AFNDtoAFD (automata3, tipo3)
      automata3, tipo3 = complemento (automata3, tipo3)
      return automata3, tipo3
    else:
      automata1, tipo1 = AFNDtoAFD (automata1, tipo1)
      automata2, tipo2 = AFNDtoAFD (automata2, tipo2)
      return interseccion (automata1, tipo1, automata2, tipo2)
  else:
    if tipo1:
      automata2, tipo2 = AFNDtoAFD (automata2, tipo2)
      return interseccion (automata1, tipo1, automata2, tipo2)
      
    if tipo2:
      automata1, tipo1 = AFNDtoAFD (automata1, tipo1)
      return interseccion (automata1, tipo1, automata2, tipo2)
  
#Funciones para graficar automata
def imprimirAutomata(automata, tipo):
  
  print (f'{bcolors.OKGREEN}Tipo ['+tipo+']'+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Estados iniciales : ', str(automata.initial_state)+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Estados Finales : ', str(automata.final_states)+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Estados : ', str(automata.states)+bcolors.ENDC)  
  print (f'{bcolors.OKGREEN}Símbolos de Entrada : ', str(automata.input_symbols)+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Transiciones : ', str(automata.transitions)+bcolors.ENDC+'\n')


def draw(automata, tipo, nombre):

    nombre = nombre+'.sv'

    trans = []
    
    if tipo == False: #dfa
        
        #nombre = 'dfa'
    
        for k,v in automata.transitions.items():
      
            for i in v:
                trans.append(( k, v[i], i))

    else:  #nfa
        
        #nombre = 'nfa'
        
        for k,v in automata.transitions.items():
            for i in v:
                for j in v[i]:
                    trans.append(( k,j, i))
    
    g = Digraph(filename=nombre, format='png')
    g.graph_attr['rankdir'] = 'LR'
    g.node('ini', shape="point")

    for e in list(automata.states):
        if e in list(automata.final_states):     
            g.node(e, shape="doublecircle")
        else:   
            g.node(e)
        if e in [automata.initial_state]:
            g.edge('ini',e)

    for t in trans:
        if t[2] not in list(automata.input_symbols):
            return 0
        else:
          if(t[1] != "q"):
            g.edge(t[0], "q"+t[1], label=str(t[2])) ##CHANGE

    g.render(nombre, view=False,directory="static/")
