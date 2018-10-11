#Daniel Zamora García
#Esteban Montero Fonseca
#Jeferson Moreno Zuñiga

#Proyecto #1 de Paradigmas de Programación

#interfaz
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET 

#===============================================================Seccion de metodos=========================================================================
textTop = 0 #Guarda el text superior para usarlo en otras funciones
textBot = 0 #Guarda el text innferior para usarlo en otras funciones
pathFile = "" #Guarda la dirección del archivo que se abre

#Funcion para mostrar datos en el TextArea
def writeOnText(inpt):
    textTop.insert(END, inpt)

#Fncion para obtener el input del Text
def retrieveInput():
    inpt = textTop.get("1.0",'end-1c')
    print(inpt)
    return inpt

#Leer archivos xml y mostrarlos en pantalla
def readXML(path):
    tree = ET.parse(path)  
    root = tree.getroot()
    # atributos de un item
    #print('Item #2 attribute:')  
    #print(root[0][1].attrib)
    # atributos de toddos los items
    #print('\nAll attributes:')  
    for elem in root:  
        for subelem in elem:
            print(subelem.attrib)
    # dato de un item especifico
    #print('\nItem #2 data:')  
    #print(root[0][1].text)
    # datos de todos los items
    #print('\nAll item data:')  
    for elem in root:  
        for subelem in elem:
            writeOnText(subelem.text)
        writeOnText("\n")

#Leer archivos txt y mostrarlos en pantalla
def readTXT(path):
    file = open(path, "r")
    textTop.delete('1.0', END)
    textTop.update()
    for line in file:
        writeOnText(line) 

#Crear y guarddar archivos xml (ver e implementar el formato del los xml)
def writeXML(path):
    data = ET.Element('data')  
    items = ET.SubElement(data, 'items')  
    item1 = ET.SubElement(items, 'item')  
    item2 = ET.SubElement(items, 'item')  
    item1.set('name','item1')  
    item2.set('name','item2')  
    item1.text = 'item1abc'  
    item2.text = 'item2abc'
    # crea un nuevo archivo XML con los resultados 
    myfile = open(path, "wb")  
    myfile.write(ET.tostring(data))

#Crear y guardar archivos txt
def writeTXT(path):
    file = open(path,"w")
    file.write(retrieveInput())
    file.close() 

def donothing():
    filewin = TopLevel(root)
    button = Button(filewin, text="Do nothin button")
    button.pack()

#abre el explorador de archivos
def abrirArchivo():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo",filetypes = (("Text file","*.txt"),("XML file","*.xml")))
    global pathFile
    pathFile = path
    if (path.endswith('.xml')):
        readXML(path)
    elif (path.endswith('.txt')):
        readTXT(path)
   
#guardar el archivo como
def guardarArchivo():
    path = filedialog.asksaveasfilename(initialdir = "/",title = "Guardar archivo",filetypes = (("Text files","*.txt"),("XML files","*.xml")))
    if (path.endswith('.xml')):
        writeXML(path)
    elif (path.endswith('.txt')):
        writeTXT(path)

#Opcion guardar en el menu
def modificarArchivo():
    print(pathFile)
    if pathFile != "":
        if (pathFile.endswith('.xml')):
            writeXML(pathFile)
        elif (pathFile.endswith('.txt')):
            writeTXT(pathFile)
    else:
        guardarArchivo()
    

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

def lamda3():
    textTop.insert(END, "Λ^3")

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
   mb.menu.add_command(label="Λ^3 (lambda^3)", command=lamda3)
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
    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()
    #root.geometry('%sx%s' % (screen_width, screen_height))
    #root.attributes('-fullscreen', True)
    root.state('zoomed')
    #menu principal y submenus
    menu(root)
    toolbar(root)
    #area de texto y scroll
    global textTop, textBot
    textTop = textArea(root)
    textBot = textArea(root)
    root.mainloop()

#==========================================================================================================================================================

#==============================================================Pantalla principal==========================================================================
pantallaPrincipal()



#==========================================================================================================================================================

