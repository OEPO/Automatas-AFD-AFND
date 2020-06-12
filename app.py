from config import Config
from flask import Flask, render_template, request, redirect, url_for
from forms import Form, Transiciones, bcolors

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods = ['GET', 'POST'])
def index():
    
    trans = Transiciones()
    form = Form()
    
    message0 = '' 
    message1 = ''
    message2 = ''

    if request.method == 'GET':

        print(f'{bcolors.WARNING}usuario detectado{bcolors.ENDC}')

    if request.method == 'POST' and form.cantidad1.data and form.cantidad2.data:
        
        global states1
        global input_symbols1
        global final_states1
        global transitions1
        global alfabeto1
        global est_finales1
        global AFND1
        global tipo1
        states1 = {}
        input_symbols1 = set(form.simbolos1.data.split(','))
        final_states1 = {}
        
        tipo1 = ''
        alfabeto1 = []
        alfabeto1.append('--')
        est_finales1 = []
        
        
        global states2
        global input_symbols2
        global final_states2
        global transitions2
        global alfabeto2
        global est_finales2
        global AFND2
        global tipo2
        states2 = {}
        input_symbols2 = set(form.simbolos2.data.split(','))
        final_states2 = {}
        
        tipo2 = ''
        alfabeto2 = []
        alfabeto2.append('--')
        est_finales2 = []
        
        
        if form.tipo1.data == False:
            
            tipo1 = 'AFD'
            AFND1 = False
            alfabeto1 = alfabeto1 + form.simbolos1.data.split(',')
            transitions1 = { '': { }}
            aux = []
            
            for i in range(form.cantidad1.data):
                
                transitions1.update({'q'+str(i) : { '': ''} } )
                aux.append('q'+str(i))
            
        else:
            
            tipo1 = 'AFND'
            AFND1 = True
            alfabeto1.append('')
            alfabeto1 = alfabeto1 + form.simbolos1.data.split(',')
            transitions1 = { '': {'' : { }}}
            aux = []
            
            for i in range(form.cantidad1.data):
                
                transitions1.update({'q'+str(i) : { '': { } } } ) 
                aux.append('q'+str(i))
        
        states1 = set(aux)

        if form.tipo2.data == False:
            
            tipo2 = 'AFD'
            AFND2 = False
            alfabeto2 = alfabeto2 + form.simbolos2.data.split(',')
            transitions2 = { '': { }}
            aux = []
            
            for i in range(form.cantidad2.data):
                
                transitions2.update({'q'+str(i) : { '': ''} } )
                aux.append('q'+str(i))
        
        else:
            
            tipo2 = 'AFND'
            AFND2 = True
            alfabeto2.append('')
            alfabeto2 = alfabeto2 + form.simbolos2.data.split(',')
            transitions2 = { '': {'' : { }}}
            aux = []
            
            for i in range(form.cantidad2.data):
                
                transitions2.update({'q'+str(i) : { '': { } } } ) 
                aux.append('q'+str(i))
        
        states2 = set(aux)

        transitions2.pop('', None)
        transitions1.pop('', None)
        
        print(f'{bcolors.OKGREEN}Estados automata 1 ['+tipo1+'] : ',str(states1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Estados automata 2 ['+tipo2+'] : ',str(states2)+bcolors.ENDC)
        
        print(f'{bcolors.OKGREEN}Alfabeto del automata 1 : ', str(input_symbols1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Alfabeto del automata 2 : ', str(input_symbols2)+bcolors.ENDC)
        
        print(f'{bcolors.OKGREEN}Transiciones automata 1 : ', str(transitions1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Transiciones automata 2 : ', str(transitions2)+bcolors.ENDC)
    
        message0 = 'Automata1 '+tipo1+' de '+str(form.cantidad1.data)+' estados y Automata2 '+tipo2+' de '+str(form.cantidad2.data)+' estados listos para ser creados.'
    
    if request.method == 'POST':
        
        trans.origen1.choices = [(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]   
        trans.input1.choices = [(alfabeto1[i],alfabeto1[i]) for i in range(len(alfabeto1))]
        trans.destino1.choices = [(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]
        trans.origen1.choices[0] = (0,'--')
        trans.destino1.choices[0] = (0,'--')
        
        trans.origen2.choices = [(i,'q'+str(i-1)) for i in range(len(transitions2)+1)]   
        trans.input2.choices = [(alfabeto2[i],alfabeto2[i]) for i in range(len(alfabeto2))]
        trans.destino2.choices = [(i,'q'+str(i-1)) for i in range(len(transitions2)+1)]
        trans.origen2.choices[0] = (0,'--')
        trans.destino2.choices[0] = (0,'--')
    
        if  trans.origen1.data != 'None' and trans.destino1.data != 'None' and trans.input1.data != 'None' and trans.input1.data != '--' and trans.origen1.data != '0' and trans.destino1.data != '0':
            
            if AFND1 == False:
                
                aux = transitions1.pop('q'+str(int(trans.origen1.data)-1))
                aux.pop('',-1)
                aux.update({trans.input1.data : 'q'+str(int(trans.destino1.data)-1) })
                transitions1.update( {'q'+str(int(trans.origen1.data)-1) : aux } )

            else:

                aux = transitions1.pop('q'+str(int(trans.origen1.data)-1))
                
                if trans.input1.data not in aux.keys():
                    
                    aux.update( { trans.input1.data : { 'q'+str(int(trans.destino1.data)-1) } } )
                    aux.pop('',-1)
                    transitions1.update( {'q'+str(int(trans.origen1.data)-1) : aux } )

                else:
                    
                    aux0 = aux.pop(trans.input1.data)
                    aux1 = list(aux0)
                    aux1.append('q'+str(int(trans.destino1.data)-1))
                    aux1 = set(aux1)
                    aux.update( { trans.input1.data : aux1 } )
                    transitions1.update( {'q'+str(int(trans.origen1.data)-1) : aux } )
                    
            message1 = 'Transicion (q'+str(int(trans.origen1.data)-1)+', '+'"'+trans.input1.data+'"'+', q'+str(int(trans.destino1.data)-1)+') en automata 1 ['+tipo1+'] agregada'
                
            print(bcolors.WARNING+message1+bcolors.ENDC)
            print(f'{bcolors.OKGREEN}transiciones automata 1 : ', str(transitions1)+bcolors.ENDC)

            if trans.final1.data == True:
                
                qf = 'q'+str(int(trans.destino1.data)-1)
                est_finales1.append(qf)
                final_states1 = set(est_finales1)

                print(f'{bcolors.WARNING}Estado final '+qf+' agregado en los estados finales '+str(final_states1)+' del automata 1'+bcolors.ENDC)
        
        else:
            
            print(f'{bcolors.FAIL}la transición del automata 1 es invalida'+bcolors.ENDC)
        
        if  trans.origen2.data != 'None' and trans.destino2.data != 'None' and trans.input2.data != 'None' and trans.input2.data != '--' and trans.origen2.data != '0' and trans.destino2.data != '0':
            
            if AFND2 == False:

                aux = transitions2.pop('q'+str(int(trans.origen2.data)-1))
                aux.pop('',-1)
                aux.update({trans.input2.data : 'q'+str(int(trans.destino2.data)-1) })
                transitions2.update( {'q'+str(int(trans.origen2.data)-1) : aux } )
            
            else:
                
                aux = transitions2.pop('q'+str(int(trans.origen2.data)-1))
                
                if trans.input2.data not in aux.keys():
                    
                    aux.update( { trans.input2.data : { 'q'+str(int(trans.destino2.data)-1) } } )
                    aux.pop('',-1)
                    transitions2.update( { 'q'+str(int(trans.origen2.data)-1) : aux } )
                
                else:
                    
                    aux0 = aux.pop(trans.input2.data)
                    aux1 = list(aux0)
                    aux1.append('q'+str(int(trans.destino2.data)-1))
                    aux1 = set(aux1)
                    aux.update( { trans.input2.data : aux1 } )
                    transitions2.update( { 'q'+str(int(trans.origen2.data)-1) : aux } )

            message2 = 'Transicion (q'+str(int(trans.origen2.data)-1)+', '+'"'+trans.input2.data+'"'+', q'+str(int(trans.destino2.data)-1)+') en automata 2 ['+tipo2+'] agregada'

            print(bcolors.WARNING+message2+bcolors.ENDC)
            print(f'{bcolors.OKGREEN}transiciones automata 2 : ', str(transitions2)+bcolors.ENDC)
            
            if trans.final2.data == True:
                
                qf = 'q'+str(int(trans.destino2.data)-1)
                est_finales2.append(qf)
                final_states2 = set()

                print(f'{bcolors.WARNING}Estado final '+qf+' agregado en los estados finales '+str(final_states2)+' del automata 2'+bcolors.ENDC)
        
        else:
            
            print(f'{bcolors.FAIL}la transición del automata 2 es invalida'+bcolors.ENDC)
    
    #if request.method != 'GET' and form.cantidad1.data != False or form.cantidad2.data != False:
        #print(f'{bcolors.FAIL}¡Faltan los estados de uno o de los dos automatas!{bcolors.ENDC}')
    
    return render_template('form.html', form = form, trans = trans, message0 = message0, message1 = message1, message2 = message2)

if __name__ == '__main__':
    app.run(debug=True)