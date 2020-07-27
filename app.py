from config import Config
from flask import Flask, render_template, request, redirect, url_for, send_file
from forms import Form, Transiciones, inputStrings, bcolors
from funciones import validar, crear, leer, AFNDtoAFD, AFDtoAFND, union, complemento, concatenacion, interseccion, imprimirAutomata, draw, validarInput, validarInter, simplificar, validarSimbolos

#Para graficar
import os
import base64

os.environ["PATH"] += os.pathsep + './grafos-venv/release/bin/'

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/formulario', methods = ['GET', 'POST'])
def index():
    
    trans = Transiciones()
    form = Form()
    global error0
    global error1
    global error2
    global message0
    global message1
    global message2
    global trans_message1
    global trans_message2
    
    alerta = 'alert-success'
    
    message0 = '' 
    message1 = ''
    message2 = ''
    error1 = ''
    error2 = ''
    
    global switch
    global automata1
    global automata2
    global states1
    global input_symbols1
    global final_states1
    global transitions1
    global states2
    global input_symbols2
    global final_states2
    global transitions2

    global color 

    global validacion1
    global validacion2

    global creacion

    global sets1
    global sets2

    if request.method == 'GET':
        
        switch = False
        
        validacion1 = False
        validacion2 = False

        creacion = False
        
        color = 'red'
        
        trans_message1 = ''
        trans_message2 = ''

        print(f'{bcolors.OKGREEN}Usuario detectado.{bcolors.ENDC}'+'\n')

    if request.method == 'POST' and request.form.get('submit', True) == ' Ingresar ' and form.cantidad1.data and form.cantidad2.data and validarSimbolos(form.simbolos1.data) == True and validarSimbolos(form.simbolos2.data) == True :
     
        switch = True
        
        global alfabeto1
        global est_finales1
        global AFND1
        global tipo1
        
        input_symbols1 = set(form.simbolos1.data.split(','))
        final_states1 = {}
        tipo1 = ''
        alfabeto1 = []
        alfabeto1.append('--')
        est_finales1 = []
        
        global alfabeto2
        global est_finales2
        global AFND2
        global tipo2
        
        input_symbols2 = set(form.simbolos2.data.split(','))
        final_states2 = {}
        tipo2 = ''
        alfabeto2 = []
        alfabeto2.append('--')
        est_finales2 = []
        
        if form.tipo1.data == False :
            
            tipo1 = 'AFD'
            AFND1 = False
            alfabeto1 = alfabeto1 + form.simbolos1.data.split(',')
            transitions1 = { '': { }}
            aux0 = []
            
            for i in range(form.cantidad1.data):
                
                transitions1.update( {'q'+str(i) : { '': '' } } )
                aux0.append('q'+str(i))
                
                for j in range(len(alfabeto1)-1):
                    
                    aux1 = transitions1.pop('q'+str(i))
                    aux1.pop('', -1)
                    aux1.update( { alfabeto1[j+1] : '' } )  
                    transitions1.update( {'q'+str(i) : aux1 } )
        
        else:
            
            tipo1 = 'AFND'
            AFND1 = True
            alfabeto1.append('ε')
            alfabeto1 = alfabeto1 + form.simbolos1.data.split(',')
            transitions1 = { '': {'' : { }}}
            aux0 = []
            
            for i in range(form.cantidad1.data):
                
                transitions1.update( { 'q'+str(i) : { '': { } } } )
                aux1 = transitions1.pop('q'+str(i))
                aux1.pop('',-1)
                transitions1.update( { 'q'+str(i) : aux1 } )
                aux0.append('q'+str(i))
        
        states1 = set(aux0)
        
        if form.tipo2.data == False:
            
            tipo2 = 'AFD'
            AFND2 = False
            alfabeto2 = alfabeto2 + form.simbolos2.data.split(',')
            transitions2 = { '': { }}
            aux0 = []
            
            for i in range(form.cantidad2.data):
                
                transitions2.update({'p'+str(i) : { '': ''} } )
                aux0.append('p'+str(i))
                
                for j in range(len(alfabeto2)-1):
                    
                    aux1 = transitions2.pop('p'+str(i))
                    aux1.pop('', -1)
                    aux1.update( { alfabeto2[j+1] : '' } )  
                    transitions2.update( {'p'+str(i) : aux1 } )
        
        else:
            
            tipo2 = 'AFND'
            AFND2 = True
            alfabeto2.append('ε')
            alfabeto2 = alfabeto2 + form.simbolos2.data.split(',')
            transitions2 = { '': {'' : { }}}
            aux0 = []
            
            for i in range(form.cantidad2.data):
                
                aux0.append('p'+str(i))
                transitions2.update( {'p'+str(i) : { '': { } } } )
                aux1 = transitions2.pop('p'+str(i))
                aux1.pop('',-1)
                transitions2.update( { 'p'+str(i) : aux1 } )
        
        states2 = set(aux0)
        
        transitions2.pop('', -1)
        transitions1.pop('', -1)
        
        print(f'{bcolors.OKGREEN}Estados automata 1 ['+tipo1+'] : ',str(states1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Estados automata 2 ['+tipo2+'] : ',str(states2)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Alfabeto del automata 1 : ', str(input_symbols1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Alfabeto del automata 2 : ', str(input_symbols2)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Transiciones automata 1 : ', str(transitions1)+bcolors.ENDC)
        print(f'{bcolors.OKGREEN}Transiciones automata 2 : ', str(transitions2)+bcolors.ENDC+'\n')
        
        trans_message1 = str(transitions1)
        trans_message2 = str(transitions2)
        message0 = 'Automata1 '+tipo1+' de '+str(form.cantidad1.data)+' estados y Automata2 '+tipo2+' de '+str(form.cantidad2.data)+' estados listos para obtener transiciones.'
    
    elif request.form.get('submit', True) == ' Ingresar ' :

        alerta = 'alert-danger'
            
        message0 = 'La cantidad o simbolos de ambos automatas no son válidos.'
        
        print(bcolors.FAIL+message0+bcolors.ENDC+'\n')

    if request.method == 'POST' and switch == True :

        trans.origen1.choices = [(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]   
        trans.input1.choices = [(alfabeto1[i],alfabeto1[i]) for i in range(len(alfabeto1))]
        trans.destino1.choices = [(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]
        trans.origen1.choices[0] = (0,'--')
        trans.destino1.choices[0] = (0,'--')
        trans.origen2.choices = [(i,'p'+str(i-1)) for i in range(len(transitions2)+1)]   
        trans.input2.choices = [(alfabeto2[i],alfabeto2[i]) for i in range(len(alfabeto2))]
        trans.destino2.choices = [(i,'p'+str(i-1)) for i in range(len(transitions2)+1)]
        trans.origen2.choices[0] = (0,'--')
        trans.destino2.choices[0] = (0,'--')
        
        if request.form.get('addtrans1', True) == 'Agregar transición' and request.form.get('crear', True) != 'Crear Automatas' :
            
            if trans.input1.data != '--' and trans.origen1.data != '0' and trans.destino1.data != '0' :
            
                if AFND1 == False:
                
                    aux = transitions1.pop('q'+str(int(trans.origen1.data)-1))
                    aux.update( { trans.input1.data : 'q'+str(int(trans.destino1.data)-1) } )
                    transitions1.update( { 'q'+str(int(trans.origen1.data)-1) : aux } )
            
                else:
                
                    if trans.input1.data == 'ε':

                        trans.input1.data = ''

                    aux = transitions1.pop('q'+str(int(trans.origen1.data)-1))
                
                    if trans.input1.data not in aux.keys() :
                    
                        aux.update( { trans.input1.data : { 'q'+str(int(trans.destino1.data)-1) } } )
                        transitions1.update( {'q'+str(int(trans.origen1.data)-1) : aux } )
                
                    else:
                    
                        aux0 = aux.pop(trans.input1.data)
                        aux1 = list(aux0)
                        aux1.append('q'+str(int(trans.destino1.data)-1))
                        aux1 = set(aux1)
                        aux.update( { trans.input1.data : aux1 } )
                        transitions1.update( {'q'+str(int(trans.origen1.data)-1) : aux } )
                    
                message1 = 'Transición (q'+str(int(trans.origen1.data)-1)+', '+'"'+trans.input1.data+'"'+', q'+str(int(trans.destino1.data)-1)+') en automata 1 ['+tipo1+'] agregada.'
            
                if trans.final1.data == True :
                
                    qf = 'q'+str(int(trans.destino1.data)-1)
                    est_finales1.append(qf)
                    final_states1 = set(est_finales1)

                    message1 = message1+' Estado final '+qf+' agregado en los estados finales.'
            
                trans_message1 = str(transitions1)+', finales = '+str(final_states1)
            
                print(bcolors.OKGREEN+message1+bcolors.ENDC+' '+bcolors.FAIL+error1+bcolors.ENDC+'\n'+bcolors.OKGREEN+trans_message1+bcolors.ENDC+'\n')
        
            elif trans.origen1.data == '0' or trans.destino1.data == '0' or trans.input1.data == '--' and request.form.get('submit', True) != 'Crear Automatas' :
            
                error1 = 'La transición del automata 1 es inválida.'
                
                print(bcolors.FAIL+error1+bcolors.ENDC+'\n')
        
        if request.form.get('addtrans2', True) == 'Agregar transición' and request.form.get('crear', True) != 'Crear Automatas':
        
            if  trans.input2.data != '--' and trans.origen2.data != '0' and trans.destino2.data != '0' :
            
                if AFND2 == False:
                
                    aux = transitions2.pop('p'+str(int(trans.origen2.data)-1))
                    aux.pop('',-1)
                    aux.update({trans.input2.data : 'p'+str(int(trans.destino2.data)-1) })
                    transitions2.update( {'p'+str(int(trans.origen2.data)-1) : aux } )
            
                else:
                
                    if trans.input2.data == 'ε':

                        trans.input2.data = ''

                    aux = transitions2.pop('p'+str(int(trans.origen2.data)-1))
                
                    if trans.input2.data not in aux.keys() :
                    
                        aux.update( { trans.input2.data : { 'p'+str(int(trans.destino2.data)-1) } } )
                        transitions2.update( { 'p'+str(int(trans.origen2.data)-1) : aux } )
                
                    else:
                    
                        aux0 = aux.pop(trans.input2.data)
                        aux1 = list(aux0)
                        aux1.append('p'+str(int(trans.destino2.data)-1))
                        aux1 = set(aux1)
                        aux.update( { trans.input2.data : aux1 } )
                        transitions2.update( { 'p'+str(int(trans.origen2.data)-1) : aux } )
            
                message2 = 'Transicion (p'+str(int(trans.origen2.data)-1)+', '+'"'+trans.input2.data+'"'+', p'+str(int(trans.destino2.data)-1)+') en automata 2 ['+tipo2+'] agregada.'
            
                if trans.final2.data == True :
                
                    qf = 'p'+str(int(trans.destino2.data)-1)
                    est_finales2.append(qf)
                    final_states2 = set(est_finales2)

                    message2 = message2+' Estado final '+qf+' agregado en los estados finales.'
                    
                trans_message2 = str(transitions2)+', finales = '+str(final_states2)
            
                print(bcolors.OKGREEN+message2+bcolors.ENDC+' '+bcolors.FAIL+error2+bcolors.ENDC+'\n'+bcolors.OKGREEN+trans_message2+bcolors.ENDC+'\n')

            elif trans.origen2.data == '0' or trans.destino2.data == '0' or trans.input2.data == '--' and request.form.get('crear', True) != 'Crear Automatas' :
            
                error2 = 'La transición del automata 2 es inválida.'
                
                print(bcolors.FAIL+error2+bcolors.ENDC+'\n')
        
        
        sets1 = [states1, input_symbols1, transitions1, 'q0', final_states1]
        sets2 = [states2, input_symbols2, transitions2, 'p0', final_states2]
    
        validacion1 = validar(sets1,AFND1)
        validacion2 = validar(sets2,AFND2)

        if validacion1 == True and validacion2 == True :

            if '✓' not in trans_message1 :
                
                trans_message1 = trans_message1 + ' ✓'
            
            if '✓' not in trans_message2 :
                
                trans_message2 = trans_message2 + ' ✓'
            
            creacion = True
            
            color = 'green'
        
        else:
            
            if validacion1 == True :
                
                if '✓' not in trans_message1 :
                
                    trans_message1 = trans_message1 + ' ✓'
            
            else:
                
                if '✓' in trans_message1 :
                    
                    trans_message1 = trans_message1.split(' ✓')
            
            if validacion2 == True :
                
                if '✓' not in trans_message2 :
                    
                    trans_message2 = trans_message2 + ' ✓'
            
            else:
                
                if '✓' in trans_message2 :
                    
                    trans_message2 = trans_message2.split(' ✓')

            color = 'red'

    if request.method == 'POST' and request.form.get('reset1', True) == 'Reiniciar transiciones del Automata 1' :
        
        validacion1 = False
        creacion = False
        color = 'red'
        
        final_states1 = {}
        est_finales1.clear()

        if AFND1 == False :
            
            transitions1 = { '': { }}
            aux0 = []
            
            for i in range(len(list(states1))) :
                
                transitions1.update( {'q'+str(i) : { '': '' } } )
                
                aux0.append('q'+str(i))
                
                for j in range(len(alfabeto1)-1):
                    
                    aux1 = transitions1.pop('q'+str(i))
                    aux1.pop('', -1)
                    aux1.update( { alfabeto1[j+1] : '' } )  
                    transitions1.update( {'q'+str(i) : aux1 } )
        
        else:
            
            transitions1 = { '': {'' : { }}}
            aux0 = []
            
            for i in range(len(list(states1))):
                
                transitions1.update( { 'q'+str(i) : { '': { } } } )
                aux1 = transitions1.pop('q'+str(i))
                aux1.pop('',-1)
                transitions1.update( { 'q'+str(i) : aux1 } )
                aux0.append('q'+str(i))

        transitions1.pop('', -1)
        
        message1 = 'Transiciones del automata 1 reiniciadas.'
        
        trans_message1 = str(transitions1)+', finales '+str(final_states1)
        
        print(bcolors.WARNING+message1+bcolors.ENDC+'\n')

    if request.method == 'POST' and request.form.get('reset2', True) == 'Reiniciar transiciones del Automata 2' :

        validacion2 = False
        creacion = False
        color = 'red'
        
        final_states2 = {}
        est_finales2.clear()

        if AFND2 == False :
            
            transitions2 = { '': { }}
            aux0 = []
            
            for i in range(len(list(states2))) :
                
                transitions2.update( {'p'+str(i) : { '': '' } } )
                
                aux0.append('p'+str(i))
                
                for j in range(len(alfabeto2)-1):
                    
                    aux1 = transitions2.pop('p'+str(i))
                    aux1.pop('', -1)
                    aux1.update( { alfabeto2[j+1] : '' } )  
                    transitions2.update( {'p'+str(i) : aux1 } )
        
        else:
            
            transitions2 = { '': {'' : { }}}
            aux0 = []
            
            for i in range(len(list(states2))):
                
                transitions2.update( { 'p'+str(i) : { '': { } } } )
                aux1 = transitions2.pop('p'+str(i))
                aux1.pop('',-1)
                transitions2.update( { 'p'+str(i) : aux1 } )
                aux0.append('p'+str(i))

        transitions2.pop('', -1)
        
        message2 = 'Transiciones del automata 2 reiniciadas.'
        
        trans_message2 = str(transitions2)+', finales '+str(final_states2)
        
        print(bcolors.WARNING+message2+bcolors.ENDC+'\n')
    
    if request.method == 'POST' and request.form.get('crear', True) == 'Crear Automatas' :
        
        if switch == True :
            
            if creacion == True :
                
                automata1 = crear(sets1, AFND1)
                automata2 = crear(sets2, AFND2)
                
                print(f'{bcolors.OKGREEN}Los automatas han sido creados satisfactoriamente.\n{bcolors.ENDC}')
                
                return redirect('automatas')
            
            else:
                
                if validacion1 == False :
                
                    error1 = 'El automata 1 ['+tipo1+'] ingresado no pudo ser creado debido a que no es válido.'
                    
                    print(bcolors.FAIL+error1+bcolors.ENDC+'\n')
    
                if validacion2 == False :

                    error2 = 'El automata 2 ['+tipo2+'] ingresado no pudo ser creado debido a que no es válido.'
                    
                    print(bcolors.FAIL+error2+bcolors.ENDC+'\n')
    
        else:
            
            error0 = 'No se ha determinado la cantidad de estados o alfabetos de los automatas.'
            
            print(bcolors.FAIL+error0+bcolors.ENDC+'\n')
    
    return render_template('form.html', form = form, trans = trans, trans_message1 = trans_message1, trans_message2 = trans_message2, message0 = message0, message1 = message1, message2 = message2, color = color, alerta = alerta)


@app.route('/automatas', methods = ['GET', 'POST']) 
def automatas() :
    
    if request.method == 'GET' and switch == False:

        print(f'{bcolors.FAIL}No se ha creado ningún automata aún.\n{bcolors.ENDC}')
        
        return redirect('/')

    message0 = ''
    message1 = ''
    message2 = ''
    inputs = inputStrings()

    alerta = 'alert-success'

    varGlobales = globals()
    
    if request.method == 'POST' :
        
        if inputs.inputString1.data :
            
            if validarInput(automata1, inputs.inputString1.data) == True : 
                
                message1 = leer(automata1, inputs.inputString1.data)
            
            else :

                alerta = 'alert-danger'
                
                message1 = 'La cadena "'+str(inputs.inputString1.data)+'" no es válida para el automata.'
    
        if inputs.inputString2.data :
            
            if validarInput(automata2, inputs.inputString2.data) == True : 
                
                message2 = leer(automata2, inputs.inputString2.data)
            
            else :

                alerta = 'alert-danger'

                message2 = 'La cadena "'+str(inputs.inputString2.data)+'" no es válida para el automata.'
    
        if request.form.get('AFNDtoAFD1', True) == 'AFND a su AFD mínimo' :

            if AFND1 == True : 

                varGlobales['automata1'] = AFNDtoAFD(automata1)
                
                varGlobales['AFND1'] = False
                
                message1 = 'El automata 1 ha sido convertido a su equivalente AFD y minimizado.'
                
                print(bcolors.OKGREEN+message1+bcolors.ENDC+'\n')
            
            else:
                
                alerta = 'alert-warning'
                
                message1 = 'El automata 1 ya es AFD, pero se ha simplificado.'
                
                print(bcolors.WARNING+message1+bcolors.ENDC+'\n')

            varGlobales['automata2'] = simplificar(automata2)
        
        if request.form.get('AFNDtoAFD2', True) == 'AFND a su AFD mínimo' :

            if AFND2 == True :
                
                varGlobales['automata2'] = AFNDtoAFD(automata2)

                varGlobales['AFND2'] = False

                message2 = 'El automata 2 ha sido convertido a su equivalente AFD y minimizado.'
                
                print(bcolors.OKGREEN+message2+bcolors.ENDC+'\n')
            
            else:

                alerta = 'alert-warning'
                
                message2 = 'El automata 2 ya es AFD, pero se ha simplificado.'
                
                print(bcolors.WARNING+message2+bcolors.ENDC+'\n')
        
            varGlobales['automata2'] = simplificar(automata2)
        
        if request.form.get('complemento1', True) == 'Complemento de automata 1' :

            if AFND1 == False :

                if len(list(automata1.final_states)) < len(list(automata1.states)) :
                
                    varGlobales['automata1'] = complemento(automata1)

                    message1 = 'Se ha obtenido el complemento del Automata 1.'

                else : 

                    alerta = 'alert-danger'
                    
                    message1 = 'El complemento del automata 1 no existe.'
            
            else :
               
                alerta = 'alert-danger'
                
                message1 = 'El Automata 1 es AFND.'

        if request.form.get('complemento2', True) == 'Complemento de automata 2' :

            if AFND2 == False :

                if len(list(automata2.final_states)) < len(list(automata2.states)) :
                
                    varGlobales['automata2'] = complemento(automata2)

                    message2 = 'Se ha obtenido el complemento del Automata 2.'

                else :

                    alerta = 'alert-danger'
                    
                    message2 = 'El complemento del automata 2 no existe.'
            
            else :

                alerta = 'alert-danger'
                
                message2 = 'El Automata 2 es AFND.'

        if request.form.get('union', True) == 'Unión entre 1 y 2' or inputs.inputUnion.data or request.form.get('AFNDtoAFDUnion', True) == 'AFND a su AFD mínimo' :

            global automataUnion
                
            global tipoUnion
            
            if request.form.get('union', True) == 'Unión entre 1 y 2' :
                
                automataUnion = union(automata1, AFND1, automata2, AFND2)

                tipoUnion = True
            
            if request.form.get('AFNDtoAFDUnion', True) == 'AFND a su AFD mínimo' and tipoUnion == True :

                automataUnion = AFNDtoAFD(automataUnion)

                tipoUnion = False

            elif tipoUnion == False :

                automataUnion = simplificar(automataUnion)
            
            if inputs.inputUnion.data : 
                
                if validarInput(automataUnion, inputs.inputUnion.data) == True : 

                    message0 = leer(automataUnion, inputs.inputUnion.data)

                else :
                    
                    alerta = 'alert-danger'
                
                    message0 = 'La cadena "'+str(inputs.inputUnion.data)+'" no es válida para el automata.'

            auU = base64.b64encode(draw(automataUnion,tipoUnion,'union')).decode('utf-8')
            
            imprimirAutomata(automataUnion,'AFND')
            
            return render_template('union.html', union = auU, message0 = message0, alerta = alerta, inputs = inputs)
        
        if request.form.get('concatenacion', True) == 'Concatenación entre 1 y 2' or inputs.inputCon.data or request.form.get('AFNDtoAFDCon', True) == 'AFND a su AFD mínimo' :

            global automataCon
                
            global tipoCon

            if request.form.get('concatenacion', True) == 'Concatenación entre 1 y 2' :
                
                automataCon = concatenacion(automata1, AFND1, automata2, AFND2)
            
                tipoCon = True
            
            if request.form.get('AFNDtoAFDCon', True) == 'AFND a su AFD mínimo' and tipoCon == True :

                automataCon = AFNDtoAFD(automataCon)

                tipoCon = False

            elif tipoCon == False :

                automataCon = simplificar(automataCon)
            
            if inputs.inputCon.data : 
                
                if validarInput(automataCon, inputs.inputCon.data) == True : 

                    message0 = leer(automataCon, inputs.inputCon.data)

                else :
                    
                    alerta = 'alert-danger'
                
                    message0 = 'La cadena "'+str(inputs.inputCon.data)+'" no es válida para el automata.'

            auC = base64.b64encode(draw(automataCon,tipoCon,'concatenacion')).decode('utf-8')
            
            imprimirAutomata(automataCon,'AFND')
            
            return render_template('concatenacion.html', concatenacion = auC, message0 = message0, alerta = alerta, inputs = inputs)

        if (request.form.get('interseccion', True) == 'Intersección entre 1 y 2' or inputs.inputInter.data or request.form.get('minifyInter', True) == 'AFND a AFD mínimo') and validarInter(automata1, automata2) == True :

            global automataInter

            global tipoInter
            
            if request.form.get('interseccion', True) == 'Intersección entre 1 y 2' :
                  
                automataInter = interseccion(automata1, AFND1, automata2, AFND2)

                tipoInter = False
                
                if len(list(automataInter.states)) == len(list(automata1.states)) :

                    tipoInter = AFND1

                if len(list(automataInter.states)) == len(list(automata2.states)) :

                    tipoInter = AFND2

            if inputs.inputInter.data : 

                if validarInput(automataInter, inputs.inputInter.data) == True : 

                    message0 = leer(automataInter, inputs.inputInter.data)

                else :
                    
                    alerta = 'alert-danger'
                
                    message0 = 'La cadena "'+str(inputs.inputInter.data)+'" no es válida para el automata.'
            
            if request.form.get('minifyInter', True) == 'AFND a AFD mínimo' : 

                if tipoInter == True :
                
                    automataInter = AFNDtoAFD(automataInter)

                    automataInter = simplificar(automataInter)
                
                    message0 = 'Se ha simplificado el automata a su AFND mínimo'
                
                else :
                    
                    automataInter = simplificar(automataInter)

                    message0 = 'El automata ya es AFD pero see ha simplificado a su equivalente mínimo'

            auI = base64.b64encode(draw(automataInter,tipoInter,'interseccion')).decode('utf-8')
            
            imprimirAutomata(automataInter,'AFD')
            
            return render_template('interseccion.html', interseccion = auI, message0 = message0, alerta = alerta, inputs = inputs)
        
        elif validarInter(automata1, automata2) == False and request.form.get('interseccion', True) == 'Intersección entre 1 y 2' :

            alerta = 'alert-danger'

            message0 = 'La intersección entre los dos automatas no existe, debido a que ninguno posee un lenguaje regular para su complemento.'

            print(bcolors.FAIL+message0+bcolors.ENDC)
    
    imprimirAutomata(automata1, tipo1)
    imprimirAutomata(automata2, tipo2)

    au1 = base64.b64encode(draw(automata1,AFND1,'automata1')).decode('utf-8')
    au2 = base64.b64encode(draw(automata2,AFND2,'automata2')).decode('utf-8')
    
    return render_template('automatas.html', inputs = inputs, message0 = message0, message1 = message1,  message2 = message2, automata1 = au1, automata2 = au2, alerta = alerta)


if __name__ == '__main__':
    app.run(debug=True)