from automata.fa.dfa import DFA   #Libreria Automata
from automata.fa.nfa import NFA
from graphviz import Digraph
from forms import bcolors

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

def validarSimbolos(simbolos) :

  if simbolos == '' :

    return False
  
  simbolos.replace(' ','')

  aux = simbolos.split(',')
  print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',simbolos.split(','))

  for s in list(simbolos.split(',')) :

    aux.remove(s)
    
    if len(s) > 1 or s in aux or s == '':

      return False
  
  return True


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

def validarInput(automata, entrada):
  
  if automata.accepts_input(entrada):
    
    return True
  
  else:
    
    return False

def leer(automata, cadena):
    
  return 'El automata responde a la cadena finalizando en el estado : '+str(automata.read_input(cadena))#+automata.read_input_stepwise(entrada)

def simplificar(automata) :

  return automata.minify()

def AFNDtoAFD(automata) :
  
  dfa = DFA.from_nfa(automata)
    
  return dfa

def AFDtoAFND(automata) :
  
  nfa = NFA.from_dfa(automata)

  return nfa
  
def union(automata1, tipo1, automata2, tipo2) :
  # Crear un estado inicial y juntar 2 automatas
  simbolos = []
  for i in list(automata1.input_symbols) :
    simbolos.append(i)
  for a in (automata2.input_symbols) :
    simbolos.append(a)
  estados = []
  for i in list(automata1.states) :
    estados.append(i)
  for a in list(automata2.states):
    estados.append(a)
  estados.append('inicio')
  final = []
  for i in list(automata1.final_states) :
    final.append(i)
  for a in list(automata2.final_states) :
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
      return automata
  # Formato dfa:  'q0': {'0': 'q0', '1': 'q1'}
  # Formato nfa:  'q1': {'0': {'q1'}, '1': {'q2'}}
    else:
      automata2 = AFDtoAFND(automata2)
      automata1 = AFDtoAFND(automata1)
      return union(automata1, True, automata2, True)
  else:
    if tipo1:
      automata2 = AFDtoAFND(automata2)
      return union(automata1, True, automata2, True)
    if tipo2:
      automata1 = AFDtoAFND(automata1)
      return union(automata1, True, automata2, True)

def complemento(automata):  
  
  newFinales = []
  finales = list(automata.final_states)
  estados = list(automata.states)
  
  for i in estados :
      
    if i not in finales :
        
      newFinales.append(i)
    
  newFinales = set(newFinales)
    
  CDFA = [set(automata.states),set(automata.input_symbols),automata.transitions.copy(),automata.initial_state,newFinales]
    
  if validar(CDFA, False) == True :

    return crear(CDFA, False)
    
  else :
      
    return automata

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
    
def validarInter(automata1, automata2) :

  if len(list(automata1.final_states)) < len(list(automata1.states)) and len(list(automata2.final_states)) < len(list(automata2.states)) :

    return True
  
  else : 

    return False

def interseccion (automata1, tipo1, automata2, tipo2) : 
  
  if tipo1 == False and tipo2 == False :

    automata1 = complemento(automata1)
    automata2 = complemento(automata2)

    aux = union(automata1, False, automata2, False)
    
    interseccion = complemento(AFNDtoAFD(aux))
      
    return interseccion
    
  else :

    if tipo1 == True :

      automata1 = AFNDtoAFD(automata1)
      automata1 = complemento(automata1)
    
    if tipo2 == True :

      automata2 = AFNDtoAFD(automata2)
      automata2 = complemento(automata2)

    aux = union(automata1, False, automata2, False)
    
    interseccion = complemento(AFNDtoAFD(aux))
 
    if validar(interseccion, False) == True :

      return interseccion

    else :

      return automata1 # caso muy extremo en que la intersección no sea válida


#return print('en progreso')
  
#Funciones para graficar automata
def imprimirAutomata(automata, tipo):
  
  print (f'{bcolors.OKGREEN}Tipo ['+tipo+']'+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Estado inicial : ', str(automata.initial_state)+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Estados Finales : ', str(automata.final_states)+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Estados : ', str(automata.states)+bcolors.ENDC)  
  print (f'{bcolors.OKGREEN}Símbolos de Entrada : ', str(automata.input_symbols)+bcolors.ENDC)
  print (f'{bcolors.OKGREEN}Transiciones : ', str(automata.transitions)+bcolors.ENDC+'\n')


def draw(automata, tipo, nombre):

  g = Digraph(filename=nombre, format='png')
  g.graph_attr['rankdir'] = 'LR'
  g.node('ini', shape="point")

  for e in list(automata.states):
    
    if e in list(automata.final_states) : 
      
      g.node(e, shape="doublecircle") 
        
    if e in [automata.initial_state] : 
          
        g.edge('ini', e)

  if tipo == False :
      
    for k, d in automata.transitions.items() :
          
      v = list(d.values())
          
      inputs = list(d.keys())
          
      for i in range(len(inputs)) :
        
        g.edge(k, v[i], label=str(inputs[i]))
    
  else:

    for k1, d1 in automata.transitions.items() :

      for k2, d2 in d1.items() :
        
        v = list(d2)

        aux = k2
        
        if k2 == '' :
          aux = 'ε'
        
        for i in range(len(v)):

          g.edge(k1, v[i], label=aux)
  
  return g.pipe(format='png')
