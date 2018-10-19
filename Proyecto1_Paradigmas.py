#Daniel Zamora García
#Esteban Montero Fonseca
#Jeferson Moreno Zuñiga

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
    reemplazos = []
    s = 0
    v = 0
    m = 0
    for reobj in re.finditer(regularExpression, entrada):
        if s == 0:
            if bool(reobj.group('symbols')):
                symbols = reobj.group('symbols')[9:]
                if (symbols != ""):
                    s += 1
        if v == 0:
            if bool(reobj.group('vars')):
                var = reobj.group('vars')[6:]
                if (var != ""):
                    v += 1
        if m == 0:
            if bool(reobj.group('markers')):
                markers = reobj.group('markers')[9:]
                if (markers != ""):
                    m += 1
        if reobj.group('rule'):
            if (reobj.group('label')):
                remp = sepPatron(reobj.group('remp'))
                lbl = getLbl(reobj.group('remp'))
                if "Λ" in remp:
                    remp = remp.replace("Λ", "", 1)
                reemplazos.append((reobj.group('label'), reobj.group('patron'), remp, bool(reobj.group('term')), lbl))
            else:
                remp = reobj.group('remp')
                if "Λ" in remp:
                    remp = remp.replace("Λ", "", 1)
                reemplazos.append(("", reobj.group('patron'), reobj.group('remp'), bool(reobj.group('term')), ""))
    if (s == 0):
        symbols = "abcdefghijklmnopqrstuvwxyz0123456789"
    if (v == 0):
        var = "wxyz"
    if (m == 0):
        markers = "αβγδ"
    reemplazos.append(symbols)
    reemplazos.append(var)
    reemplazos.append(markers)
    return reemplazos

#Reemplaza la entrada por cada de cada regla
def markovStepped(text, reemplazos):
    writeOnText("Entrada: " + text + "\n\n", textBot)
    symbols = reemplazos [len(reemplazos) - 3]
    var = reemplazos [len(reemplazos) - 2]
    markers = reemplazos [len(reemplazos) - 1]
    if checkSymbols(text, symbols, markers) == 1:
        while True:
            i = 0
            while i < len(reemplazos) - 3:
                label = reemplazos[i][0]
                patron = reemplazos[i][1]
                remp = reemplazos[i][2]
                term = reemplazos[i][3]
                lbl = reemplazos[i][4][1:]
                lbl = lbl[:len(lbl) - 1]
                if lbl == "":
                    if patron in text:
                        text = text.replace(patron, remp, 1)
                        writeOnText("\t->" + text, textBot)
                        writeOnText("\t\t\t(Aplicando " + label[1:] + patron + "->" + remp + lbl + ")", textBot)
                        writeOnText("\n", textBot)
                        if term:
                            return text
                        break
                else:
                    for x in range (0, (len(reemplazos)) - 3):
                        if patron in text:
                            text = text.replace(patron, remp, 1)
                            writeOnText("\t->" + text, textBot)
                            writeOnText("\t\t\t(Aplicando " + label[1:] + " " + patron + "->" + remp + " " + "(" + lbl[1:] + "))", textBot)
                            writeOnText("\n", textBot)
                            if term:
                                return text
                            break
                        if reemplazos[x][0][:len(reemplazos[x][0]) - 1] == lbl:
                            label = reemplazos[x][0][:len(reemplazos[x][0]) - 1]
                            patron = reemplazos[x][1]
                            remp = reemplazos[x][2]
                            term = reemplazos[x][3]
                            lbl = reemplazos[x][4][1:]
                            lbl = lbl[:len(lbl) - 1]
                            i = x
                            if patron in text:
                                text = text.replace(patron, remp, 1)
                                writeOnText("\t->" + text, textBot)
                                writeOnText("\t\t\t(Aplicando " + label[1:] + " " + patron + "->" + remp + " " + "(" + lbl[1:] + "))", textBot)
                                writeOnText("\n", textBot)
                                if term:
                                    return text
                                break
                i += 1
            else:
                writeOnText("\nSalida: " + text + "\n", textBot)
                return text
    else:
        popup("No coincide el alfabeto!!".upper())
        #writeOnText("\n\nNo coincide el alfabeto!!".upper(), textBot)

def markovDirecto(text, reemplazos):
    writeOnText("Entrada: " + text + "\n", textBot)
    symbols = reemplazos [len(reemplazos) - 3]
    var = reemplazos [len(reemplazos) - 2]
    markers = reemplazos [len(reemplazos) - 1]
    if checkSymbols(text, symbols, markers) == 1:
        while True:
            i = 0
            while i < len(reemplazos) - 3:
                label = reemplazos[i][0]
                patron = reemplazos[i][1]
                remp = reemplazos[i][2]
                term = reemplazos[i][3]
                lbl = reemplazos[i][4][1:]
                lbl = lbl[:len(lbl) - 1]
                i += 1
                if lbl == "":
                    if patron in text:
                        text = text.replace(patron, remp, 1)
                        if term:
                            return text
                        break
                else:
                    for x in range (0, (len(reemplazos)) - 3):
                        if patron in text:
                            text = text.replace(patron, remp, 1)
                            writeOnText("\t->" + text, textBot)
                            writeOnText("\t\t\t(Aplicando " + label[1:] + " " + patron + "->" + remp + " " + "(" + lbl[1:] + "))", textBot)
                            writeOnText("\n", textBot)
                            if term:
                                return text
                            break
                        if reemplazos[x][0][:len(reemplazos[x][0]) - 1] == lbl:
                            label = reemplazos[x][0][:len(reemplazos[x][0]) - 1]
                            patron = reemplazos[x][1]
                            remp = reemplazos[x][2]
                            term = reemplazos[x][3]
                            lbl = reemplazos[x][4][1:]
                            lbl = lbl[:len(lbl) - 1]
                            i = x
                            if patron in text:
                                text = text.replace(patron, remp, 1)
                                i += 1
                                if term:
                                    return text
                                break
            else:
                writeOnText("Salida: " + text + "\n", textBot)
                return text
    else:
        popup("No coincide el alfabeto!!".upper())

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

def exeMarkovS():
    global algoritmoMarkov
    algoritmoMarkov = retrieveInput(textTop)
    entrada = retrieveInput(textBot)
    textBot.delete('1.0', END)
    textBot.update()
    if entrada != "":
        if algoritmoMarkov != "":
            markovStepped(entrada, getReemplazos(algoritmoMarkov))
        else:
            popup("NO SE HA INTRODUCIDO UN ALGORITMO!")
    else:
        popup("NO SE HA INTRODUCIDO UNA HILERA DE ENTRADA!!")

def exeMarkovD():
    global algoritmoMarkov
    algoritmoMarkov = retrieveInput(textTop)
    entrada = retrieveInput(textBot)
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
            writeOnText(subelem.text + "\n", textTop)
        writeOnText("\n", textTop)

#Leer archivos txt y mostrarlos en pantalla
def readTXT(path):
    file = open(path, "r")
    textTop.delete('1.0', END)
    textTop.update()
    for line in file:
        writeOnText(line, textTop) 

#Crear y guarddar archivos xml (ver e implementar el formato del los xml)
def writeXML(path):    
    markov = ET.Element('markov')
    text = retrieveInput(textTop)
    comments = ET.SubElement(markov, 'comments')
    symbols = ET.SubElement(markov, 'symbols')
    markers = ET.SubElement(markov, 'markers')
    vars1 = ET.SubElement(markov, 'vars')
    rules = ET.SubElement(markov, 'rules')
    i = 0
    strg = ""
    
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
            symbols.text = strg
        elif i < len(text) and text[i] == "#" and text[i + 1] == "m":
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            markers.text = strg
        elif i < len(text) and text[i] == "#" and text[i + 1] == "v":
            x = i
            while i < len(text) and text[i] != "\n":
                i += 1
            strg = text[x:i]
            vars1.text = strg
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
    file = open(path,"w")
    file.write(retrieveInput(textTop))
    file.close() 

def donothing():
    filewin = TopLevel(root)
    button = Button(filewin, text="Do nothin button")
    button.pack()

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

def hilerasPruebaTXT():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo de prueba", filetypes = (("Text file","*.txt"), (("Text files","*.txt"))))
    realizaPruebasHileras(path)
    
def realizaPruebasHileras(path):
    file = open(path, "r")
    textBot.delete('1.0', END)
    textBot.update()
    algoritmoMarkov = retrieveInput(textTop)
    if algoritmoMarkov != "":
        for line in file:
            markovDirecto(line, getReemplazos(algoritmoMarkov))
    else:
        popup( "NO SE HA INTRODUCIDO UN ALGORITMO!")

def hilerasPruebaTXTStepped():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo de prueba", filetypes = (("Text file","*.txt"), (("Text files","*.txt"))))
    realizaPruebasHilerasStepped(path)
    
def realizaPruebasHilerasStepped(path):
    file = open(path, "r")
    textBot.delete('1.0', END)
    textBot.update()
    algoritmoMarkov = retrieveInput(textTop)
    if algoritmoMarkov != "":
        for line in file:
            markovStepped(line, getReemplazos(algoritmoMarkov))
    else:
        popup("NO SE HA INTRODUCIDO UN ALGORITMO!")

def popup(msg):
    LARGE_FONT= ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)
    popup = Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
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

    #submenu ayuda
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Indice de Ayuda", command=donothing)
    helpmenu.add_command(label="Acerca de...", command=donothing)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)
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
    root.title("IDE")
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

