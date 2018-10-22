#Daniel Zamora García
#Esteban Montero Fonseca
#Jeferson Moreno Zúñiga

#Proyecto #1 de Paradigmas de Programación

#interfaz
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import xml.etree.ElementTree as ET 
import re
#===============================================================Seccion de metodos=========================================================================
textTop = 0 #Guarda el text superior para usarlo en otras funciones
textBot = 0 #Guarda el text innferior para usarlo en otras funciones
pathFile = "" #Guarda la dirección del archivo que se abre

algoritmoMarkov = "" #Guarda los parametros del algoritmo al "ejecutarlo"
textFinal = "" #Guarda el resultado de aplicar todas las reglas de sustitucion
regularExpression = r"""(?mx)
^(?: 
  (?: (?P<comment> \% .*)) |
  (?: (?P<blank> \s*) (?: \n | $)) |
  (?: (?P<symbols> \#symbols .+)) |
  (?: (?P<vars> \#vars .+)) |
  (?: (?P<markers> \#markers .+)) |
  (?: (?P<rule> (?P<label> \_.+\:)? (?P<patron> .+?) \s+ -> \s+ (?P<term> \.)? (?P<remp> .+)))
 )$
""" #Formato con el que se ejecuta el algoritmo

#Devuelve cada regla del algoritmo ingresado
def getReemplazos(entrada):
    reemplazos = []     #Guardar los parametros del algoritmo de markov
    s = 0               #Para saber si ya se guardo el alfabeto del algoritmo
    v = 0               #Para saber si ya se guardaron las variables del algoritmo
    m = 0               #Para saber si ya se guardaron los markers del algoritmo
    var = ""
    for reobj in re.finditer(regularExpression, entrada): #Devuelve un iterador conteniendo los parametros y lo guarda en reobj
        if s == 0:
            if bool(reobj.group('symbols')): #Si el alfabeto esta en reobj
                symbols = reobj.group('symbols')[9:] #asigna el alfabeto desde la posicion 9 del string
                if (symbols != ""): 
                    s += 1 #Para saber que ya se guardo el alfabeto
        if v == 0:
            if bool(reobj.group('vars')):    #Si las variables estan en reobj
                var = reobj.group('vars')[6:] #asigna variables desde la posicion 6 del string
                if (var != ""):
                    v += 1  #Para saber que ya se guardo las variables
        if m == 0:
            if bool(reobj.group('markers')): #Si los markers estan en reobj
                markers = reobj.group('markers')[9:] #asigna markers desde la posicion 9 del string
                if (markers != ""):
                    m += 1 #Para saber que ya se guardo los markers
        if reobj.group('rule'): #Si reobj contiene reglas de sustitucion
            remp = sepPatron(reobj.group('remp')) #Asigna el remplazo a remp
            pat = reobj.group('patron')
            if "Λ" in pat:
                pat = pat.replace("Λ", "", 1) #Sustituye Λ por la hilera vacia
            if "Λ" in remp:
                remp = remp.replace("Λ", "", 1) #Sustituye Λ por la hilera vacia
            if (reobj.group('label')): #Si reobj contiene nombre ->P1:
                lbl = getLbl(reobj.group('remp')) #Asigna la etiqueta a lbl
                if "." in remp:
                    reemplazos.append((reobj.group('label'), pat, remp, True, lbl))
                    #Asigna vector con reglas al vector reemplazos
                else:
                    reemplazos.append((reobj.group('label'), pat, remp, bool(reobj.group('term')), lbl))
            else:
                if "." in remp:
                    reemplazos.append(("", pat, remp, True, ""))
                    #Asigna vector con reglas al vector reemplazos
                else:
                    reemplazos.append(("", pat, remp, bool(reobj.group('term')), ""))
    if (s == 0): #El algoritmo no especificaba el alfabeto
        symbols = "abcdefghijklmnopqrstuvwxyz0123456789" #Alfabeto por defecto
    if (m == 0):  #El algoritmo no especificaba merkers
        markers = "αβγδ" #Markers por defecto
    reemplazos.append(symbols) #
    reemplazos.append(var) #Asigna el alfabeto, variables y markers al vector reemplazos
    reemplazos.append(markers) #
    return reemplazos #retorna el vector con todos los parametros del algoritmo

def sustitucionMarkovStepped(text, reemplazos):
    w = 0
    while w < len(reemplazos) + 3:
        i = 0
        z = 0
        while i < len(reemplazos) - 3:
            if checkvars(reemplazos[i][1], reemplazos [len(reemplazos) - 2])!= "" and getMarkerIndex(text, getMarker(reemplazos[i][1], reemplazos [len(reemplazos) - 1])) == len(text) - 1:   
            #el marcador esta al final de la hilera de entrada
                i += 1 #Se pasa a la siguiente regla
                z = getMarkerIndex(text, getMarker(reemplazos[i][1], reemplazos [len(reemplazos) - 1])) #Guarda la pos del marcador en el texto de entrada
                z = z - 1 #Se pasa a la izq del marcador
            elif checkvars(reemplazos[i][1], reemplazos [len(reemplazos) - 2]) != "":
                z = getMarkerIndex(text, getMarker(reemplazos[i][1], reemplazos [len(reemplazos) - 1])) #Guarda la pos del marcador en el texto de entrada
                z = z + 1 #Se pasa a la derecha de marcador
            label = reemplazos[i][0] #Asigna el nombre de la regla (vector de vectores)
            patron = reemplazos[i][1] #Asigna el patron de la regla
            if patron == "":
                text = insertaEspacio(text)
            remp = reemplazos[i][2] #Asigna el remplazo de la regla
            term = reemplazos[i][3] #Si la regla es terminal asigna true, sino false
            lbl = reemplazos[i][4][1:] #Asigna la etiqueta de la regla, eliminando el parentesis abierto (
            lbl = lbl[:len(lbl) - 1] #Elimina el parentesis cerrado ) de la etiqueta
            var = reemplazos [len(reemplazos) - 2] #Guarda variables del vector reemplazos en symbols
            patronVar = checkvars(patron, var) #Guarda la variable del patron (si hay)
            varT = getMarker(patron, reemplazos [len(reemplazos) - 1]) #Guarda el marcador del patron (si hay)
            aux = patronVar #Guarda la variable del patron (si hay)
            rempVar = checkvars(remp, var) #Guarda la variable del reemplazo (si hay)
            if patronVar != "": #Si hay variable en el patron
                if z < len(text):
                    patronVar = patron.replace(patronVar, text[z], 1) #Reemplaza el patron con el caracter de la entrada en la pos z
                    if rempVar != "": #Si hay variable en el reemplazo
                        rempVar = remp.replace(rempVar, text[z], 1) #Reemplaza el remp con el caracter de la entrada en la pos z
                        rempVar = eliminaEspacios(rempVar) #Elimina espacios del reemplazo (si hay)
                        if patronVar in text: #Si el texto contiene el patron de reemplazo
                            text = text.replace(patronVar, rempVar, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                            writeOnText("\t->" + text, textBot)
                            if lbl == "": #Si la regla contiene etiqueta (para formato)
                                writeOnText("\t\t(Aplicando " + label[1:] + patronVar + "->" + rempVar + lbl + ")", textBot)
                            else:
                                writeOnText("\t\t(Aplicando " + label[1:] + patronVar + "->" + rempVar + " " + "(" + lbl[1:] + "))", textBot)
                            writeOnText("\n", textBot)
                            if term: #Si la regla es terminal
                                return text #Retorna, y sale del metodo
                            if lbl == "": #Si la regla contiene etiqueta
                                z = z + 1
                                i = i + 1
                            else:
                                z = z + 1
                                i = aumentador(reemplazos, lbl)
                        else:#El patron no esta en la hilera de entrada
                            i = i + 1
                            w = w + 1
                    else: #no hay variable en el reemplazo
                        if patronVar in text: #Si el texto contiene el patron de reemplazo
                            text = text.replace(patronVar, remp, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                            writeOnText("\t->" + text, textBot)
                            if lbl == "": #Si la regla contiene etiqueta (para formato)
                                writeOnText("\t\t(Aplicando " + label[1:] + patronVar + "->" + remp + lbl + ")", textBot)
                            else:
                                writeOnText("\t\t(Aplicando " + label[1:] + patronVar + "->" + remp + " " + "(" + lbl[1:] + "))", textBot)
                            writeOnText("\n", textBot)
                            if term: #Si la regla es terminal
                                return text #Retorna, y sale del metodo
                            if lbl == "": #Si la regla contiene etiqueta
                                z = z + 1
                                i = i + 1
                            else:
                                z = z + 1
                                i = aumentador(reemplazos, lbl)
                        else: #El patron no esta en la hilera de entrada
                            i = i + 1
                            w = w + 1
                else:
                    return text
            elif rempVar != "": #No hay variable en el patron, si hay variable en el reemplazo 
                rempVar = remp.replace(rempVar, text[z], 1) #Reemplaza el remp con el caracter de la entrada en la pos z
                rempVar = eliminaEspacios(rempVar) #Elimina espacios del reemplazo (si hay)
                if patron in text: #Si el texto contiene el patron de reemplazo
                    text = text.replace(patron, rempVar, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                    writeOnText("\t->" + text, textBot)
                    if lbl == "": #Si la regla contiene etiqueta (para formato)
                        writeOnText("\t\t(Aplicando " + label[1:] + patron + "->" + rempVar + lbl + ")", textBot)
                    else:
                        writeOnText("\t\t(Aplicando " + label[1:] + patron + "->" + rempVar + " " + "(" + lbl[1:] + "))", textBot)
                    writeOnText("\n", textBot)
                    if term: #Si la regla es terminal
                        return text #Retorna, y sale del metodo
                    if lbl == "": #Si la regla contiene etiqueta
                        z = z + 1
                        i = i + 1
                    else:
                        z = z + 1
                        i = aumentador(reemplazos, lbl)
                else: #El patron no esta en la hilera de entrada
                    i = i + 1
                    w = w + 1
            else: #No hay variable en el patron ni en el reemplazo
                if patron in text: #Si la regla es terminal
                    text = text.replace(patron, remp, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                    writeOnText("\t->" + text, textBot)
                    if lbl == "": #Si la regla contiene etiqueta (para formato)
                        writeOnText("\t\t(Aplicando " + label[1:] + patron + "->" + remp + lbl + ")", textBot)
                    else:
                        writeOnText("\t\t(Aplicando " + label[1:] + patron + "->" + remp + " " + "(" + lbl[1:] + "))", textBot)
                    writeOnText("\n", textBot)
                    if term: #Si la regla es terminal
                        return text #Retorna, y sale del metodo
                    if lbl == "": #Si la regla contiene etiqueta
                        i = i + 1
                    else:
                        i = aumentador(reemplazos, lbl)
                else: #El patron no esta en la hilera de entrada
                    i = i + 1
                    w = w + 1
    else:
        return text

#Aumenta el contador para acceder a las reglas
def aumentador(reemplazos, lbl):
    i = 0
    while i < (len(reemplazos) - 3):
        if reemplazos[i][0][:len(reemplazos[i][0]) - 1] == lbl:
            break
        i += 1
    return i

#Inserta un espacio vacio al inicio de la hilera de entrada
def insertaEspacio(text):
    return text.replace(text[0], "" + text[0], 1)

#Devuelve la posicion del marcador en la hilera de prueba, si no hay devuelve -1
def getMarkerIndex(entrada, marker):
    i = 0
    x = 0
    if marker != "":
        while i < len(entrada):
            if entrada[i] == marker:
                return i
            i += 1
    return -1

#Elimina espacios en blanco
def eliminaEspacios(reemp):
    i = 0
    while i < len(reemp):
        if reemp[i] == " ":
            break
        i += 1
    return reemp[:i]

#Elimina saltos de linea en las hileras de prueba
def eliminaSaltos(entrada):
    i = 0
    while i < len(entrada):
        if entrada[i] == "\n":
            break
        i += 1
    return entrada[:i]

#Devuelve la variable del patron o reemplazo, si no hay devuelve ""
def checkvars(entrada, vars1):
    i = 0
    x = 0
    while x < len(entrada):
        i = 0
        while i < len(vars1):
            if entrada[x] == vars1[i]:
                return vars1[i]
            i += 1
        x += 1
    return ""

#Devuelve el marcador del patron o reemplazo, si no hay devuelve ""
def getMarker(entrada, markers):
    i = 0
    x = 0
    while x < len(entrada):
        i = 0
        while i < len(markers):
            if entrada[x] == markers[i]:
                return markers[i]
            i += 1
        x += 1
    return ""

#Algoritmo de Markov directo
def sustitucionMarkovD(text, reemplazos):
    w = 0
    while w < len(reemplazos) + 1:
        i = 0
        z = 0
        while i < len(reemplazos) - 3:
            if checkvars(reemplazos[i][1], reemplazos [len(reemplazos) - 2])!= "" and getMarkerIndex(text, getMarker(reemplazos[i][1], reemplazos [len(reemplazos) - 1])) == len(text) - 1: #el marcador esta al final de la hilera de entrada
                i += 1 #Se pasa a la siguiente regla
                z = getMarkerIndex(text, getMarker(reemplazos[i][1], reemplazos [len(reemplazos) - 1])) #Guarda la pos del marcador en el texto de entrada
                z = z - 1 #Se pasa a la izq del marcador
            elif checkvars(reemplazos[i][1], reemplazos [len(reemplazos) - 2])!= "":
                z = getMarkerIndex(text, getMarker(reemplazos[i][1], reemplazos [len(reemplazos) - 1])) #Guarda la pos del marcador en el texto de entrada
                z = z + 1 #Se pasa a la derecha de marcador
            label = reemplazos[i][0] #Asigna el nombre de la regla (vector de vectores)
            patron = reemplazos[i][1] #Asigna el patron de la regla
            remp = reemplazos[i][2] #Asigna el remplazo de la regla
            term = reemplazos[i][3] #Si la regla es terminal asigna true, sino false
            lbl = reemplazos[i][4][1:] #Asigna la etiqueta de la regla, eliminando el parentesis abierto (
            lbl = lbl[:len(lbl) - 1] #Elimina el parentesis cerrado ) de la etiqueta
            var = reemplazos [len(reemplazos) - 2] #Guarda variables del vector reemplazos en symbols
            patronVar = checkvars(patron, var) #Guarda la variable del patron (si hay)
            varT = getMarker(patron, reemplazos [len(reemplazos) - 1]) #Guarda el marcador del patron (si hay)
            aux = patronVar #Guarda la variable del patron (si hay)
            rempVar = checkvars(remp, var) #Guarda la variable del reemplazo (si hay)
            if patronVar != "": #Si hay variable en el patron
                if z < len(text):
                    patronVar = patron.replace(patronVar, text[z], 1) #Reemplaza el patron con el caracter de la entrada en la pos z
                    if rempVar != "": #Si hay variable en el reemplazo
                        rempVar = remp.replace(rempVar, text[z], 1) #Reemplaza el remp con el caracter de la entrada en la pos z
                        rempVar = eliminaEspacios(rempVar) #Elimina espacios del reemplazo (si hay)
                        if patronVar in text: #Si el texto contiene el patron de reemplazo
                            text = text.replace(patronVar, rempVar, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                            if term: #Si la regla es terminal
                                return text #Retorna, y sale del metodo
                            if lbl == "": #Si la regla contiene etiqueta
                                z = z + 1
                                i = i + 1
                            else:
                                z = z + 1
                                i = aumentador(reemplazos, lbl)
                        else:#El patron no esta en la hilera de entrada
                            i = i + 1
                            w = w + 1
                    else: #no hay variable en el reemplazo
                        if patronVar in text: #Si el texto contiene el patron de reemplazo
                            text = text.replace(patronVar, remp, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                            if term: #Si la regla es terminal
                                return text #Retorna, y sale del metodo
                            if lbl == "": #Si la regla contiene etiqueta
                                z = z + 1
                                i = i + 1
                            else:
                                z = z + 1
                                i = aumentador(reemplazos, lbl)
                        else: #El patron no esta en la hilera de entrada
                            i = i + 1
                            w = w + 1
                else:
                    return text
            elif rempVar != "": #No hay variable en el patron, si hay variable en el reemplazo 
                rempVar = remp.replace(rempVar, text[z], 1) #Reemplaza el remp con el caracter de la entrada en la pos z
                rempVar = eliminaEspacios(rempVar) #Elimina espacios del reemplazo (si hay)
                if patron in text: #Si el texto contiene el patron de reemplazo
                    text = text.replace(patron, rempVar, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                    if term: #Si la regla es terminal
                        return text #Retorna, y sale del metodo
                    if lbl == "": #Si la regla contiene etiqueta
                        z = z + 1
                        i = i + 1
                    else:
                        z = z + 1
                        i = aumentador(reemplazos, lbl)
                else: #El patron no esta en la hilera de entrada
                    i = i + 1
                    w = w + 1
            else: #No hay variable en el patron ni en el reemplazo
                if patron in text: #Si la regla es terminal
                    text = text.replace(patron, remp, 1) #Reemplaza el texto con el reemplazo de la regla y lo asigna a text
                    if term: #Si la regla es terminal
                        return text #Retorna, y sale del metodo
                    if lbl == "": #Si la regla contiene etiqueta
                        i = i + 1
                    else:
                        i = aumentador(reemplazos, lbl)
                else: #El patron no esta en la hilera de entrada
                    i = i + 1
                    w = w + 1 
    else:
        return text

#Llama al metodo sustitucionMarkov
def markovStepped(text, reemplazos):
    writeOnText("Entrada: " + text + "\n\n", textBot)
    symbols = reemplazos [len(reemplazos) - 3] #Guarda el alfabeto del vector reemplazos en symbols
    var = reemplazos [len(reemplazos) - 2] #Guarda variables del vector reemplazos en symbols
    markers = reemplazos [len(reemplazos) - 1] #Guarda markers del vector reemplazos en symbols
    if checkSymbols(text, symbols, markers) == 1:
        writeOnText("No se pueden aplicar mas reglas\n\nSalida: " + sustitucionMarkovStepped(text, reemplazos) + "\n", textBot)#Llamada al metodo que realiza la sustitucion
    else:
        popup("No coincide el alfabeto!!".upper())

#Llama al metodo sustitucionMarkov Directo
def markovDirecto(text, reemplazos):
    writeOnText("Entrada: " + text + "\n", textBot)
    symbols = reemplazos [len(reemplazos) - 3] #Guarda el alfabeto del vector reemplazos en symbols
    var = reemplazos [len(reemplazos) - 2] #Guarda variables del vector reemplazos en symbols
    markers = reemplazos [len(reemplazos) - 1] #Guarda markers del vector reemplazos en symbols
    if checkSymbols(text, symbols, markers) == 1:
        writeOnText("Salida: " + sustitucionMarkovD(text, reemplazos) + "\n", textBot)#Llamada al metodo que realiza la sustitucion
    else:
        popup("No coincide el alfabeto!!".upper())

#Revisa si la entrada no contiene elementos del alfabeto
def checkSymbols(text, symbols, markers):
    result = 1
    for x in text:
        if x in markers:
            result = 1
        elif x.lower() in symbols:
            result = 1
        elif x != " " and x != "." and x != "\n":
            result = 0
            break
    return result

#Separa la etiqueta de la regla de reemplazo (remp) y la retorna
def getLbl(remp):
    i = 0
    r = ""
    if "(_" in remp:
        while i < len(remp):
            if remp[i] == "(" and remp[i + 1] == "_" :
                break
            else:
                i += 1
        r = remp[i:]
    return r

#Separa el patron de la etiqueta y lo retorna
def sepPatron(remp):
    i = 0
    r = ""
    while i < len(remp):
        if remp[i] == "(" and remp[i + 1] == "_" :
            break
        else:
            i += 1
    r = remp[:i]
    return r

#Ejecuta el algoritmo Paso por Paso
def exeMarkovS():
    global algoritmoMarkov
    algoritmoMarkov = retrieveInput(textTop)
    entrada = retrieveInput(textBot)
    entrada = eliminaSaltos(entrada)
    textBot.delete('1.0', END)
    textBot.update()
    if entrada != "":
        if algoritmoMarkov != "":
            markovStepped(entrada, getReemplazos(algoritmoMarkov))
        else:
            popup("NO SE HA INTRODUCIDO UN ALGORITMO!")
    else:
        popup("NO SE HA INTRODUCIDO UNA HILERA DE ENTRADA!!")

#Ejecuta el algoritmo directo
def exeMarkovD():
    global algoritmoMarkov
    algoritmoMarkov = retrieveInput(textTop)
    entrada = retrieveInput(textBot)
    entrada = eliminaSaltos(entrada)
    textBot.delete('1.0', END)
    textBot.update()
    if entrada != "":
        if algoritmoMarkov != "":
            markovDirecto(entrada, getReemplazos(algoritmoMarkov))
        else:
            popup("NO SE HA INTRODUCIDO UN ALGORITMO!")
    else:
        popup("NO SE HA INTRODUCIDO UNA HILERA DE ENTRADA!!")
    

#Funcion para mostrar datos en el TextArea
def writeOnText(inpt, text):
    text.insert(END, inpt)

#Fncion para obtener el input del Text
def retrieveInput(text):
    inpt = text.get("1.0",'end-1c')
    return inpt

#Leer archivos xml y mostrarlos en pantalla
def readXML(path):
    tree = ET.parse(path)  
    root = tree.getroot()
    for elem in root:  
        for subelem in elem:
            writeOnText(subelem.text, textTop)
            writeOnText("\n", textTop)
        writeOnText("\n", textTop)

#Leer archivos txt y mostrarlos en pantalla
def readTXT(path):
    file = open(path, "r", encoding='utf8')
    textTop.delete('1.0', END)
    textTop.update()
    for line in file:
        writeOnText(line, textTop) 

#Crear y guarddar archivos xml (ver e implementar el formato del los xml)
def writeXML(path):    
    markov = ET.Element('markov')
    text = retrieveInput(textTop)
    comments = ET.SubElement(markov, 'comments')
    rules = ET.SubElement(markov, 'rules')
    i = 0
    strg = ""
    symbols = ET.SubElement(markov, 'symbols')
    markers = ET.SubElement(markov, 'markers')
    vars1 = ET.SubElement(markov, 'vars')
    while i < len(text):
        if i < len(text) and text[i] == "%":
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            comment = ET.SubElement(comments, 'comment')
            comment.text = strg
        elif i < len(text) and text[i] == "#" and text[i + 1] == "s":
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            symbol = ET.SubElement(symbols, 'symbol')
            symbol.text = strg
        elif i < len(text) and text[i] == "#" and text[i + 1] == "m":
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            marker = ET.SubElement(markers, 'marker')
            marker.text = strg
        elif i < len(text) and text[i] == "#" and text[i + 1] == "v":
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            var = ET.SubElement(vars1, 'var')
            var.text = strg
        else:
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            rule = ET.SubElement(rules, 'rule')
            rule.text = strg
        i += 1
    # crea un nuevo archivo XML con los resultados 
    myfile = open(path, "wb")  
    myfile.write(ET.tostring(markov))

#Crear y guardar archivos txt
def writeTXT(path):
    encoding = 'utf8'
    file = open(path,"w", encoding=encoding)
    file.write(retrieveInput(textTop))
    file.close() 

#abre el explorador de archivos
def abrirArchivo():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo",filetypes = (("Text file","*.txt"),("XML file","*.xml")))
    textBot.delete('1.0', END)
    textBot.update()
    global pathFile
    pathFile = path
    if (path.endswith('.xml')):
        readXML(path)
    else:
        readTXT(path)
   
#guardar el archivo como
def guardarArchivo():
    path = filedialog.asksaveasfilename(initialdir = "/",title = "Guardar archivo",filetypes = (("Text files","*.txt"),("XML files","*.xml")))
    pathFile = path
    if (path.endswith('.xml')):
        writeXML(path)
    elif (path.endswith('.txt')):
        writeTXT(path)
    else:
        path = path + ".txt"
        writeTXT(path)

#Opcion guardar en el menu
def modificarArchivo():
    if pathFile != "":
        if (pathFile.endswith('.xml')):
            writeXML(pathFile)
        else:
            writeTXT(pathFile)
    else:
        guardarArchivo()

#Abre explorador de archivos para elegir el archivo con hileras de prueba (Directo)
def hilerasPruebaTXT():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo de prueba", filetypes = (("Text file","*.txt"), (("Text files","*.txt"))))
    realizaPruebasHileras(path)

#Realiza la prueba sobre las hileras del texto abierto (Directo)
def realizaPruebasHileras(path):
    file = open(path, "r")
    textBot.delete('1.0', END)
    textBot.update()
    algoritmoMarkov = retrieveInput(textTop)
    if algoritmoMarkov != "":
        for line in file:
            markovDirecto(eliminaSaltos(line), getReemplazos(algoritmoMarkov))
    else:
        popup( "NO SE HA INTRODUCIDO UN ALGORITMO!")

#Abre explorador de archivos para elegir el archivo con hileras de prueba (Paso por paso)
def hilerasPruebaTXTStepped():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo de prueba", filetypes = (("Text file","*.txt"), (("Text files","*.txt"))))
    realizaPruebasHilerasStepped(path)

#Realiza la prueba sobre las hileras del texto abierto (Paso por paso)
def realizaPruebasHilerasStepped(path):
    file = open(path, "r")
    textBot.delete('1.0', END)
    textBot.update()
    algoritmoMarkov = retrieveInput(textTop)
    if algoritmoMarkov != "":
        for line in file:
            markovStepped(eliminaSaltos(line), getReemplazos(algoritmoMarkov))
    else:
        popup("NO SE HA INTRODUCIDO UN ALGORITMO!")

#Muestra un pop up mostrando el mensaje recibido
def popup(msg):
    LARGE_FONT= ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)
    popup = Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Aceptar", command = popup.destroy)
    B1.pack()
    popup.mainloop()

#Mostrar el textArea en la pantalla
def textArea(root):
    scroll = Scrollbar(root)
    textarea = Text(root, undo=True)
    textarea.focus_set()
    scroll.pack(side=RIGHT, fill=Y)
    textarea.pack(side=TOP, fill=X)
    scroll.config(command=textarea.yview)
    textarea.config(yscrollcommand=scroll.set)
    return textarea

#Metodos del menú editar para el TextTop
def copy():
    textTop.clipboard_clear()
    text = textTop.get("sel.first", "sel.last")
    textTop.clipboard_append(text)

def cut():
    copy()
    textTop.delete("sel.first", "sel.last")

def paste():
    text=textTop.selection_get(selection='CLIPBOARD')
    textTop.insert('insert', text)

def selectAll():
    textTop.tag_add("sel", '1.0', 'end')
    return

def deselectAll():
    textTop.tag_remove("sel", '1.0', 'end')
    return

def undo():
    textTop.edit_undo()

def redo():
    textTop.edit_redo()

#Mostrar el menu en la pantalla
def menu(root):
    #barra menu
    menubar = Menu(root)

    #submenu archivo
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Nuevo", command=pantallaPrincipal)
    filemenu.add_command(label="Abrir", command=abrirArchivo)
    filemenu.add_separator()
    filemenu.add_command(label="Guardar", command=modificarArchivo)
    filemenu.add_command(label="Guardar como...", command=guardarArchivo)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.destroy)
    menubar.add_cascade(label="Archivo", menu=filemenu)

    #submenu editar
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Deshacer", command=undo)
    editmenu.add_command(label="Rehacer", command=redo)
    editmenu.add_separator()
    editmenu.add_command(label="Cortar", command=cut)
    editmenu.add_command(label="Copiar", command=copy)
    editmenu.add_command(label="Pegar", command=paste)
    editmenu.add_command(label="Seleccionar todo", command=selectAll)
    editmenu.add_command(label="Deseleccionar todo", command=deselectAll)
    menubar.add_cascade(label="Editar", menu=editmenu)

    #submenu depurar
    runmenu = Menu(menubar, tearoff=0)
    runmenu.add_command(label="Ejecutar paso a paso", command=exeMarkovS)
    runmenu.add_command(label="Ejecutar directo", command=exeMarkovD)
    runmenu.add_command(label="Ejecutar con archivo de hileras de prueba (Directo)", command=hilerasPruebaTXT)
    runmenu.add_command(label="Ejecutar con archivo de hileras de prueba (Paso a paso)", command=hilerasPruebaTXTStepped)
    menubar.add_cascade(label="Depurar", menu=runmenu)

    root.config(menu=menubar)

    

def alpha():
    textTop.insert(END, "α")

def beta():
    textTop.insert(END, "β")

def gamma():
    textTop.insert(END, "γ")

def delta():
    textTop.insert(END, "δ")

def epsilon():
    textTop.insert(END, "ε")

def zeta():
    textTop.insert(END, "ζ")

def eta():
    textTop.insert(END, "η")

def theta():
    textTop.insert(END, "θ")

def iota():
    textTop.insert(END, "ι")

def kappa():
    textTop.insert(END, "κ")

def lamda():
    textTop.insert(END, "λ")

def lamdaM():
    textTop.insert(END, "Λ")

def mu():
    textTop.insert(END, "μ")

def nu():
    textTop.insert(END, "ν")

def xi():
    textTop.insert(END, "ξ")

def omicron():
    textTop.insert(END, "ο")

def pi():
    textTop.insert(END, "π")

def rho():
    textTop.insert(END, "ρ")

def sigma():
    textTop.insert(END, "σ")

def tau():
    textTop.insert(END, "τ")

def upsilon():
    textTop.insert(END, "υ")

def phi():
    textTop.insert(END, "φ")

def chi():
    textTop.insert(END, "χ")

def psi():
    textTop.insert(END, "ψ")

def omega():
    textTop.insert(END, "ω")

def toolbar(root):
   mb = Menubutton(root, text="Caracteres especiales")
   mb.menu = Menu(mb)
   mb["menu"] = mb.menu

   mb.menu.add_command(label="α (alpha)", command=alpha)
   mb.menu.add_command(label="β (beta)", command=beta)
   mb.menu.add_command(label="γ (gamma)", command=gamma)
   mb.menu.add_command(label="δ (delta)", command=delta)
   mb.menu.add_command(label="ζ (zeta)", command=zeta)
   mb.menu.add_command(label="η (eta)", command=eta)
   mb.menu.add_command(label="θ (theta)", command=theta)
   mb.menu.add_command(label="κ (kappa)", command=kappa)
   mb.menu.add_command(label="λ (lambda)", command=lamda)
   mb.menu.add_command(label="Λ (lambda Mayuscula)", command=lamdaM)
   mb.menu.add_command(label="μ (mu)", command=mu)
   mb.menu.add_command(label="ν (nu)", command=nu)
   mb.menu.add_command(label="ξ (xi)", command=xi)
   mb.menu.add_command(label="ο (omicron)", command=omicron)
   mb.menu.add_command(label="π (pi)", command=pi)
   mb.menu.add_command(label="ρ (rho)", command=rho)
   mb.menu.add_command(label="σ (sigma)", command=sigma)
   mb.menu.add_command(label="τ (tau)", command=tau)
   mb.menu.add_command(label="υ (upsilon)", command=upsilon)
   mb.menu.add_command(label="φ (phi)", command=phi)
   mb.menu.add_command(label="χ (chi)", command=chi)
   mb.menu.add_command(label="ψ (psi)", command=psi)
   mb.menu.add_command(label="ω (omega)", command=omega)
   mb.pack()

    

#Mostrar la pantalla principal
def pantallaPrincipal():
    root = Tk()
    root.title("Proyecto1-(IDLE)-Jefferson Moreno Zuniga, Esteban Montero Fonseca y Daniel Zamora Garcia")
    root.state('zoomed')
    #menu principal y submenus
    menu(root)
    toolbar(root)
    #area de texto y scroll
    global textTop
    global textBot
    textTop = textArea(root)
    textBot = textArea(root)
    root.mainloop()

#==========================================================================================================================================================

#==============================================================Pantalla principal==========================================================================
pantallaPrincipal()



#==========================================================================================================================================================

