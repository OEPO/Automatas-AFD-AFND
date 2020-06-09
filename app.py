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
    tipo1 = ''
    tipo2 = ''

    if request.method == 'GET':

        print(f'{bcolors.WARNING}usuario detectado{bcolors.ENDC}')

    if request.method == 'POST' and form.cantidad1.data and form.cantidad2.data:
        
        global alfabeto1
        global est_finales1
        global alfabeto2
        global est_finales2
        global transiciones1
        global transiciones2
        global AFND1
        global AFND2
        alfabeto1 = []
        est_finales1 = []
        alfabeto2 = []
        est_finales2 = []
        alfabeto1.append('--')
        alfabeto2.append('--')
        alfabeto1 = alfabeto1 + form.simbolos1.data.split(',')
        alfabeto2 = alfabeto2 + form.simbolos2.data.split(',')
        
        if form.tipo1.data == False:
            
            tipo1 = 'AFD'
            AFND1 = False
            transiciones1 = { '': { }}
            [transiciones1.update({'q'+str(i) : { '': ''}}) for i in range(form.cantidad1.data)]
        
        else:
            
            tipo1 = 'AFND'
            AFND1 = True
            transiciones1 = { '': {'' : { }}}
            [transiciones1.update({'q'+str(i) : { '': {} }}) for i in range(form.cantidad1.data)]
        
        if form.tipo2.data == False:
            
            tipo2 = 'AFD'
            AFND2 = False
            transiciones2 = { '': { }}
            [transiciones2.update({'q'+str(i) : { '': ''}}) for i in range(form.cantidad2.data)]
        
        else:
            
            tipo2 = 'AFND'
            AFND2 = True
            transiciones2 = { '': {'' : { }}}
            [transiciones2.update({'q'+str(i) : { '': {} }}) for i in range(form.cantidad2.data)]
        
        transiciones2.pop('', None)
        transiciones1.pop('', None)
        
        print(f'{bcolors.OKGREEN}cantidad de estados automata 1 ['+tipo1+'] : ',str(form.cantidad1.data)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}cantidad de estados automata 2 ['+tipo2+'] : ',str(form.cantidad2.data)+bcolors.ENDC)
        
        print(f'{bcolors.OKGREEN}alfabeto del automata 1 : ', str(alfabeto1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}alfabeto del automata 2 : ', str(alfabeto2)+bcolors.ENDC)
        
        print(f'{bcolors.OKGREEN}transiciones automata 1 : ', str(transiciones1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}transiciones automata 2 : ', str(transiciones2)+bcolors.ENDC)
    
        message0 = 'Automata1 '+tipo1+' y Automata2 '+tipo2+' creados.'
    
    if request.method == 'POST':
        
        trans.origen1.choices = [(i,'q'+str(i-1)) for i in range(len(transiciones1)+1)]   
        trans.input1.choices = [(alfabeto1[i],alfabeto1[i]) for i in range(len(alfabeto1))]
        trans.destino1.choices = [(i,'q'+str(i-1)) for i in range(len(transiciones1)+1)]
        trans.origen1.choices[0] = (0,'--')
        trans.destino1.choices[0] = (0,'--')
        
        trans.origen2.choices = [(i,'q'+str(i-1)) for i in range(len(transiciones2)+1)]   
        trans.input2.choices = [(alfabeto2[i],alfabeto2[i]) for i in range(len(alfabeto2))]
        trans.destino2.choices = [(i,'q'+str(i-1)) for i in range(len(transiciones2)+1)]
        trans.origen2.choices[0] = (0,'--')
        trans.destino2.choices[0] = (0,'--')
    
        if  trans.origen1.data != 'None' and trans.destino1.data != 'None' and trans.input1.data != 'None' and trans.input1.data != '--' and trans.origen1.data != '0' and trans.destino1.data != '0' and trans.input1.data != '0':
            
            if AFND1 == False:
                
                message1 = 'Transicion (q'+str(int(trans.origen1.data)-1)+', '+'"'+trans.input1.data+'"'+', q'+str(int(trans.destino1.data)-1)+') en automata 1 (AFD) agregada'
                
                aux = transiciones1.pop('q'+str(int(trans.origen1.data)-1))
                aux.pop('',-1)
                aux.update({trans.input1.data : 'q'+str(int(trans.destino1.data)-1) })
                transiciones1.update({'q'+str(int(trans.origen1.data)-1) : aux })
            
                print(bcolors.WARNING+message1+bcolors.ENDC)
                print(f'{bcolors.OKGREEN}transiciones automata 1 : ', str(transiciones1)+bcolors.ENDC)

            else:

                message1 = 'Transicion (q'+str(int(trans.origen1.data)-1)+', '+'"'+trans.input1.data+'"'+', q'+str(int(trans.destino1.data)-1)+') en automata 1 (AFND) agregada'

                aux = transiciones1.pop('q'+str(int(trans.origen1.data)-1))
                
                if trans.input1.data not in aux.keys():
                    
                    aux0 = aux.pop('')
                    aux0.update({ trans.input1.data : { 'q'+str(int(trans.destino1.data)-1) } })
                    aux0.pop('',-1)
                    transiciones1.update({'q'+str(int(trans.origen1.data)-1) : aux0 })
                
                else:
                    
                    aux0 = aux.pop(trans.input1.data)
                    aux1 = list(aux0) #
                    aux1.append('q'+str(int(trans.destino1.data)-1))
                    aux1 = set(aux1)
                    aux2 = {'': ''}
                    aux2.update({ trans.input1.data : aux1 })
                    aux2.pop('',-1)
                    transiciones1.update({'q'+str(int(trans.origen1.data)-1) : aux2 })
                
                print(bcolors.WARNING+message1+bcolors.ENDC)
                print(f'{bcolors.OKGREEN}transiciones automata 1 : ', str(transiciones1)+bcolors.ENDC)

            if trans.final1.data == True:
                
                qf = 'q'+str(int(trans.destino1.data)-1)
                est_finales1.append(qf)

                print(f'{bcolors.WARNING}Estado final '+qf+' agregado en automata 1'+bcolors.ENDC)
        
        else:
            
            print(f'{bcolors.FAIL}la transición del automata 1 es invalida'+bcolors.ENDC)
        
        if  trans.origen2.data != 'None' and trans.destino2.data != 'None' and trans.input2.data != 'None' and trans.input2.data != '--' and trans.origen2.data != '0' and trans.destino2.data != '0' and trans.input2.data != '0':
            
            if AFND2 == False:
                
                message2 = 'Transicion (q'+str(int(trans.origen2.data)-1)+', '+'"'+trans.input2.data+'"'+', q'+str(int(trans.destino2.data)-1)+') en automata 2 (AFD) agregada'

                aux = transiciones2.pop('q'+str(int(trans.origen2.data)-1))
                aux.pop('',-1)
                aux.update({trans.input2.data : 'q'+str(int(trans.destino2.data)-1) })
                transiciones2.update({'q'+str(int(trans.origen2.data)-1) : aux })
            
                print(bcolors.WARNING+message2+bcolors.ENDC)
                print(f'{bcolors.OKGREEN}transiciones automata 2 : ', str(transiciones1)+bcolors.ENDC)

            else:
                
                aux = transiciones2.pop('q'+str(int(trans.origen2.data)-1))
                
                if trans.input2.data not in aux.keys():
                    
                    aux0 = aux.pop('')
                    aux0.update({ trans.input2.data : { 'q'+str(int(trans.destino2.data)-1) } })
                    aux0.pop('',-1)
                    transiciones2.update({'q'+str(int(trans.origen2.data)-1) : aux0 })
                
                else:
                    
                    aux0 = aux.pop(trans.input2.data)
                    aux1 = list(aux0) #
                    aux1.append('q'+str(int(trans.destino2.data)-1))
                    aux1 = set(aux1)
                    aux2 = {'': ''}
                    aux2.update({ trans.input2.data : aux1 })
                    aux2.pop('',-1)
                    transiciones2.update({'q'+str(int(trans.origen2.data)-1) : aux2 })

            print(bcolors.WARNING+message2+bcolors.ENDC)
            print(f'{bcolors.OKGREEN}transiciones automata 2 : ', str(transiciones2)+bcolors.ENDC)
            
            if trans.final2.data == True:
                
                qf = 'q'+str(int(trans.destino2.data)-1)
                est_finales1.append(qf)

                print(f'{bcolors.WARNING}Estado final '+qf+' agregado en automata 2'+bcolors.ENDC)
        
        else:
            
            print(f'{bcolors.FAIL}la transición del automata 2 es invalida'+bcolors.ENDC)
    
    #if request.method != 'GET' and form.cantidad1.data != False or form.cantidad2.data != False:
        #print(f'{bcolors.FAIL}¡Faltan los estados de uno o de los dos automatas!{bcolors.ENDC}')
    
    return render_template('form.html', form = form, trans = trans, message0 = message0, message1 = message1, message2 = message2)

if __name__ == '__main__':
    app.run(debug=True)