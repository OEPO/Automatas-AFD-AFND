from config import Config
from flask import Flask, render_template, request, redirect, url_for, send_file
from forms import Form, Transiciones, inputString, bcolors
from funciones import validar, crear, leer, AFNDtoAFD, AFDtoAFND, union, complemento, concatenacion, interseccion, imprimirAutomata, draw
#Para graficar
import os
os.environ["PATH"] += os.pathsep + './grafos-venv/release/bin/'
import base64

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
    
    message0 = '' 
    message1 = ''
    message2 = ''
    error0 = ''
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

    if request.method == 'POST' and form.cantidad1.data and form.cantidad2.data :
        
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
                
                transitions2.update({'r'+str(i) : { '': ''} } )
                aux0.append('r'+str(i))
                
                for j in range(len(alfabeto2)-1):
                    
                    aux1 = transitions2.pop('r'+str(i))
                    aux1.pop('', -1)
                    aux1.update( { alfabeto2[j+1] : '' } )  
                    transitions2.update( {'r'+str(i) : aux1 } )
        
        else:
            
            tipo2 = 'AFND'
            AFND2 = True
            alfabeto2.append('ε')
            alfabeto2 = alfabeto2 + form.simbolos2.data.split(',')
            transitions2 = { '': {'' : { }}}
            aux0 = []
            
            for i in range(form.cantidad2.data):
                
                aux0.append('r'+str(i))
                transitions2.update( {'r'+str(i) : { '': { } } } )
                aux1 = transitions2.pop('r'+str(i))
                aux1.pop('',-1)
                transitions2.update( { 'r'+str(i) : aux1 } )
        
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
    
    if request.method == 'POST' and switch == True :

        trans.origen1.choices = [(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]   
        trans.input1.choices = [(alfabeto1[i],alfabeto1[i]) for i in range(len(alfabeto1))]
        trans.destino1.choices = [(i,'q'+str(i-1)) for i in range(len(transitions1)+1)]
        trans.origen1.choices[0] = (0,'--')
        trans.destino1.choices[0] = (0,'--')
        trans.origen2.choices = [(i,'r'+str(i-1)) for i in range(len(transitions2)+1)]   
        trans.input2.choices = [(alfabeto2[i],alfabeto2[i]) for i in range(len(alfabeto2))]
        trans.destino2.choices = [(i,'r'+str(i-1)) for i in range(len(transitions2)+1)]
        trans.origen2.choices[0] = (0,'--')
        trans.destino2.choices[0] = (0,'--')
        
        if request.form.get('addtrans1', True) == 'Agregar transición' and request.form.get('crear', True) != 'Crear Automatas':
            
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
            
                trans_message1 = str(transitions1)+', finales '+str(final_states1)
            
                print(bcolors.OKGREEN+message1+bcolors.ENDC+' '+bcolors.FAIL+error1+bcolors.ENDC+'\n'+bcolors.OKGREEN+trans_message1+bcolors.ENDC+'\n')
        
            elif trans.origen1.data == '0' or trans.destino1.data == '0' or trans.input1.data == '--' and request.form.get('submit', True) != 'Crear Automatas' :
            
                error1 = 'La transición del automata 1 es inválida.'
                
                print(bcolors.FAIL+error1+bcolors.ENDC+'\n')
        
        if request.form.get('addtrans2', True) == 'Agregar transición' and request.form.get('crear', True) != 'Crear Automatas':
        
            if  trans.input2.data != '--' and trans.origen2.data != '0' and trans.destino2.data != '0' :
            
                if AFND2 == False:
                
                    aux = transitions2.pop('r'+str(int(trans.origen2.data)-1))
                    aux.pop('',-1)
                    aux.update({trans.input2.data : 'r'+str(int(trans.destino2.data)-1) })
                    transitions2.update( {'r'+str(int(trans.origen2.data)-1) : aux } )
            
                else:
                
                    if trans.input2.data == 'ε':

                        trans.input2.data = ''

                    aux = transitions2.pop('r'+str(int(trans.origen2.data)-1))
                
                    if trans.input2.data not in aux.keys() :
                    
                        aux.update( { trans.input2.data : { 'r'+str(int(trans.destino2.data)-1) } } )
                        transitions2.update( { 'r'+str(int(trans.origen2.data)-1) : aux } )
                
                    else:
                    
                        aux0 = aux.pop(trans.input2.data)
                        aux1 = list(aux0)
                        aux1.append('r'+str(int(trans.destino2.data)-1))
                        aux1 = set(aux1)
                        aux.update( { trans.input2.data : aux1 } )
                        transitions2.update( { 'r'+str(int(trans.origen2.data)-1) : aux } )
            
                message2 = 'Transicion (r'+str(int(trans.origen2.data)-1)+', '+'"'+trans.input2.data+'"'+', r'+str(int(trans.destino2.data)-1)+') en automata 2 ['+tipo2+'] agregada.'
            
                if trans.final2.data == True :
                
                    qf = 'r'+str(int(trans.destino2.data)-1)
                    est_finales2.append(qf)
                    final_states2 = set(est_finales2)

                    message2 = message2+' Estado final '+qf+' agregado en los estados finales.'
                    
                trans_message2 = str(transitions2)+', finales '+str(final_states2)
            
                print(bcolors.OKGREEN+message2+bcolors.ENDC+' '+bcolors.FAIL+error2+bcolors.ENDC+'\n'+bcolors.OKGREEN+trans_message2+bcolors.ENDC+'\n')

            elif trans.origen2.data == '0' or trans.destino2.data == '0' or trans.input2.data == '--' and request.form.get('crear', True) != 'Crear Automatas' :
            
                error2 = 'La transición del automata 2 es inválida.'
                
                print(bcolors.FAIL+error2+bcolors.ENDC+'\n')
        
        
        sets1 = [states1, input_symbols1, transitions1, 'q0', final_states1]
        sets2 = [states2, input_symbols2, transitions2, 'r0', final_states2]
    
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

    if request.method == 'POST' and request.form.get('reset1', True) == 'Reiniciar estados finales del Automata 1' :
        
        creacion = False
        validacion1 = False
        color = 'red'
        
        final_states1.clear()
        final_states1 = {}
        est_finales1.clear()
        
        message1 = 'Estados finales del automata 1 eliminados.'
        
        trans_message1 = str(transitions1)+', finales '+str(final_states1)
        
        print(bcolors.FAIL+message1+bcolors.ENDC+'\n')

    if request.method == 'POST' and request.form.get('reset2', True) == 'Reiniciar estados finales del Automata 2' :

        creacion = False
        validacion2 = False
        color = 'red'

        final_states2.clear()
        final_states2 = {}
        est_finales2.clear()
        
        message2 = 'Estados finales del automata 2 eliminados.'
        
        trans_message2 = str(transitions2)+', finales '+str(final_states2)
        
        print(bcolors.FAIL+message2+bcolors.ENDC+'\n')
    
    if request.method == 'POST' and request.form.get('crear', True) == 'Crear Automatas' :
        
        if switch == True :
            
            if creacion == True :
                
                automata1 = crear(sets1, AFND1)
                automata2 = crear(sets2, AFND2)
                
                print(f'{bcolors.OKGREEN}Los automatas han sido creados satisfactoriamente.{bcolors.ENDC}')
                
                return redirect('automatas')
            
            else:
                
                if validacion1 == False :
                
                    error1 = 'El automata 1 ingresado no pudo ser creado debido a que no es válido.'
                    
                    print(bcolors.FAIL+error1+bcolors.ENDC+'\n')
    
                if validacion2 == False :

                    error2 = 'El automata 2 ingresado no pudo ser creado debido a que no es válido.'
                    
                    print(bcolors.FAIL+error2+bcolors.ENDC+'\n')
    
        else:
            
            error0 = 'No se ha determinado la cantidad de estados o alfabetos de los automatas.'
            
            print(bcolors.FAIL+error0+bcolors.ENDC+'\n')
    
    return render_template('form.html', form = form, trans = trans, trans_message1 = trans_message1, trans_message2 = trans_message2, message0 = message0, message1 = message1, message2 = message2, error0 = error0, error1 = error1, error2 = error2, color = color)


@app.route('/automatas', methods = ['GET', 'POST']) 
def automatas() :
    
    if request.method == 'GET' and switch == False:

        print(f'{bcolors.FAIL}No se ha creado ningún automata aún.\n{bcolors.ENDC}')
        
        return redirect('/')

    message = ''
    output1 = ''
    output2 = ''
    inputs = inputString()
    imprimirAutomata(automata1, tipo1)
    imprimirAutomata(automata2, tipo2)
    
    au1 = base64.b64encode(draw(automata1,AFND1,'automata1')).decode('utf-8')
    au2 = base64.b64encode(draw(automata2,AFND2,'automata2')).decode('utf-8')

    automataUnion = []
    automata_complemento1D = complemento(automata1, AFND1)
    automata_complemento1 =  base64.b64encode(draw(automata_complemento1D[0],automata_complemento1D[1],'automata_complemento1')).decode('utf-8')

    automata_complemento2D = complemento(automata2, AFND2)
    automata_complemento2 = base64.b64encode(draw(automata_complemento2D[0],automata_complemento2D[1],'automata_complemento2')).decode('utf-8')

    automataUnionD = union(automata1, AFND1, automata2, AFND2)
    automataUnion = base64.b64encode(draw(automataUnionD[0],automataUnionD[1],'automataUnion')).decode('utf-8')

    automata_concatenacionD = concatenacion(automata1, AFND1, automata2, AFND2)
    automata_concatenacion = base64.b64encode(draw(automata_concatenacionD[0],automata_concatenacionD[1],'automata_concatenacion')).decode('utf-8')

    automata_interseccionD = interseccion(automata1, AFND1, automata2, AFND2)
    automata_interseccion = base64.b64encode(draw(automata_interseccionD[0],automata_interseccionD[1],'automata_interseccion')).decode('utf-8')
    
    if request.method == 'POST' :
        
        if inputs.inputString1.data :
            
            output1 = leer(automata1, inputs.inputString1.data)
    
        if inputs.inputString2.data :
            
            output2 = leer(automata2, inputs.inputString2.data)
    
            
    return render_template('automatas.html', inputs = inputs, output1 = output1, output2 = output2, message = message, automata1 = au1, automata2 = au2, automata_complemento1=automata_complemento1, automata_complemento2=automata_complemento2, automataUnion=automataUnion, automata_concatenacion=automata_concatenacion, automata_interseccion=automata_interseccion)



if __name__ == '__main__':
    app.run(debug=True)