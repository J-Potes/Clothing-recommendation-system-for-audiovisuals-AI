"""
Clothing Recommendation system for audiovisuals. Using genetic algorithm
- Juan Jose Potes Gomez
- Gelen Adriana Sastoque
"""

import xlrd
import random
import copy
import tkinter
from tkinter import *
from PIL import ImageTk, Image

caract = []

conjf = [None, None, None]
puntua_f = [None, None, None]
# conjf = [[1,4,10,2,5,6], [1,4,12,2,8,6], [1,4,10,100,20,6]]

CANT_POB = 800
P_MUTACION = 3
MAX_GEN = 100
nombres_c = ["Hombre", "Mujer", "Accion", "Terror", "Comedia", "Drama", "Western", 
             "Moderna", "80s", "50s", "20s", "Dorada", "Frio", "Calor", "Templado", "Infante",
             "Joven", "Adulto", "Anciano", "Formal", "Casual"]

l_sombreros = []
l_camisas = []
l_pant = []
l_abrigos = []
l_calzado = []
l_accesorios = []

# Clase prenda
class prenda:
    def __init__ (self, ident, tipo, foto, puntajes):
        self.id = ident
        self.tipo = tipo
        self.foto = foto
        self.puntajes = puntajes
        self.prom = 0
    
    def calc_prom(self, lista_caract):
        suma = 0
        for i in range(0, len(lista_caract)):
            suma += self.puntajes[lista_caract[i]]
        self.prom = suma/len(lista_caract)


# Clase conjunto
class conjunto:
    def __init__ (self, prendas):
        self.prendas = prendas
        self.fit = 0
        self.fitness()
    
    def fitness(self):
        suma = 0
        for i in range(0, len(self.prendas)):
            suma += self.prendas[i].prom
        self.fit = suma/len(self.prendas)
    
    def mostrar_consola(self):
        print("- Puntuacion: ",round(self.fit,3), "    IDs: [",self.prendas[0].id,", ",self.prendas[1].id,", "
              ,self.prendas[2].id,", ",self.prendas[3].id,", ",self.prendas[4].id,", ",self.prendas[5].id,"]")

    def getIDs(self):
        listaids = []
        for i in range(0,len(self.prendas)):
            listaids.append(self.prendas[i].id)
        return listaids
    
    def comparar(self, c2):
        iguales = True
        for i in range(0, len(self.prendas)):
            if(self.prendas[i].id != c2.prendas[i].id):
                iguales = False
                break
        return iguales
    
# Funcion para cruzar dos conjuntos padres de manera aleatoria y retornar una lista con el resultado
def cruzar(c1, c2):
    nuevo_hijo = []
    # Se recorre cada prenda y se da una probabilidad 50/50 para que herede la prenda un padre u otro
    for i in range(0, len(c1.prendas)):
        aleat = random.randint(1, 10)
        if(aleat <= 5):
            nuevo_hijo.append(c1.prendas[i])
        else:
            nuevo_hijo.append(c2.prendas[i])
    
    # En caso de haber vestido, se le pone el mismo tanto en camisa como en pantalon
    if(nuevo_hijo[1].tipo == "Vestido"):
        nuevo_hijo[2] = nuevo_hijo[1]
    
    if(nuevo_hijo[2].tipo == "Vestido"):
        nuevo_hijo[1] = nuevo_hijo[2]
    
    return nuevo_hijo

# Funcion para mutar una prenda aleatoria de un conjunto
def mutar(conj):
    global l_sombreros, l_camisas, l_pant, l_abrigos, l_calzado, l_accesorios
    
    valido = False
    while(valido == False):
        vesti = False
        tprend = random.randint(0, len(conj.prendas)-1)
        if(tprend == 1 or tprend == 2):
            if(conj.prendas[1].tipo == "Vestido" or conj.prendas[2].tipo == "Vestido"):
                vesti = True
                valido = False
                continue
        
        # Se muta el sombrero
        if(tprend == 0):
            valid2 = False
            while(valid2 == False):
                ale = random.randint(0, len(l_sombreros)-1)
                if(conj.prendas[0].id != l_sombreros[ale].id):
                    valid2 = True
                    conj.prendas[0] = l_sombreros[ale]
                    valido = True
                else:
                    valid2 = False
        
        # Se muta la camisa
        if(tprend == 1 and vesti == False):
            valid2 = False
            while(valid2 == False):
                ale = random.randint(0, len(l_camisas)-1)
                if((conj.prendas[1].id == l_camisas[ale].id) or (l_camisas[ale].tipo == "Vestido")):
                    valid2 = False
                    continue
                else:
                    valid2 = True
                    conj.prendas[1] = l_camisas[ale]
                    valido = True
        
        # Se muta el pantalon o falda
        if(tprend == 2 and vesti == False):
            valid2 = False
            while(valid2 == False):
                ale = random.randint(0, len(l_pant)-1)
                if(conj.prendas[2].id != l_pant[ale].id):
                    valid2 = True
                    conj.prendas[2] = l_pant[ale]
                    valido = True
                else:
                    valid2 = False
        
        # Se muta el abrigo
        if(tprend == 3):
            valid2 = False
            while(valid2 == False):
                ale = random.randint(0, len(l_abrigos)-1)
                if(conj.prendas[3].id != l_abrigos[ale].id):
                    valid2 = True
                    conj.prendas[3] = l_abrigos[ale]
                    valido = True
                else:
                    valid2 = False
        
        # Se muta el calzado
        if(tprend == 4):
            valid2 = False
            while(valid2 == False):
                ale = random.randint(0, len(l_calzado)-1)
                if(conj.prendas[4].id != l_calzado[ale].id):
                    valid2 = True
                    conj.prendas[4] = l_calzado[ale]
                    valido = True
                else:
                    valid2 = False
        
        # Se muta el accesorio
        if(tprend == 5):
            valid2 = False
            while(valid2 == False):
                ale = random.randint(0, len(l_accesorios)-1)
                if(conj.prendas[5].id != l_accesorios[ale].id):
                    valid2 = True
                    conj.prendas[5] = l_accesorios[ale]
                    valido = True
                else:
                    valid2 = False

# Funcion para mostrar en consola las caracteristicas que selecciono el usuario
def mostrar_caract(l_car):
    c = "  Caracteristicas: "
    for i in range(0, len(l_car)):
        c += nombres_c[l_car[i]]
        if(i < len(l_car)-1):
            c += ", "
        else:
            c += ".\n"
    print(c)
    
archivo = "Base de datos proyecto.xls"
Abrir = xlrd.open_workbook(archivo)
Hoja = Abrir.sheet_by_name("Datos")

listaprendas = []

for i in range(4,Hoja.nrows):
    id_aux = 0
    tipo_aux = ""
    punt_aux = []
    id_aux = Hoja.cell_value(i,0)
    tipo_aux = Hoja.cell_value(i,1)
    for j in range(3,Hoja.ncols):
        punt_aux.append(Hoja.cell_value(i,j))
    listaprendas.append(prenda(int(id_aux), tipo_aux, None, punt_aux))

prendasfil = []

def borrar_rep():
    global ranking_pob
            
    conta = 1
    
    while(conta < len(ranking_pob)):
        repe = False
        conta2 = 1
        while((conta-conta2) >= 0):
            if(ranking_pob[conta][1].comparar(ranking_pob[conta-conta2][1]) == True):
                repe = True
                break
            else:
                conta2 += 1
        if(repe == True):
            ranking_pob.pop(conta)
        else:
            conta += 1

def backend():
    global caract, conjf, puntua_f, ranking_pob, l_sombreros, l_camisas, l_pant, l_abrigos, l_calzado, listaprendas, prendasfil
    print("EJECUTADO")
    caract.sort()
    
    # Realizar filtro de prendas por genero del personaje

    prendasfil.clear()

    if(caract[0] == 0 or caract[0] == 1):
        
        for i in range(0, len(listaprendas)):
            
            if(listaprendas[i].puntajes[caract[0]] >= 5):
                listaprendas[i].calc_prom(caract)
                prendasfil.append(listaprendas[i])
                
    else:
        for i in range(0, len(listaprendas)):
            listaprendas[i].calc_prom(caract)
            prendasfil.append(listaprendas[i])

    
    l_sombreros.clear()
    l_camisas.clear()
    l_pant.clear()
    l_abrigos.clear()
    l_calzado.clear()
    l_accesorios.clear()
    
    # Separar las prendas en listas por tipo de prenda

    for i in range(0, len(prendasfil)):
        if(prendasfil[i].tipo == "Sombrero"):
            l_sombreros.append(prendasfil[i])
        elif(prendasfil[i].tipo == "Camisa" or prendasfil[i].tipo == "Vestido"):
            l_camisas.append(prendasfil[i])
        elif(prendasfil[i].tipo == "Abajo"):
            l_pant.append(prendasfil[i])
        elif(prendasfil[i].tipo == "Abrigo"):
            l_abrigos.append(prendasfil[i])
        elif(prendasfil[i].tipo == "Calzado"):
            l_calzado.append(prendasfil[i])
        elif(prendasfil[i].tipo == "Accesorio"):
            l_accesorios.append(prendasfil[i])


    # Generar poblacion inicial de conjuntos con prendas aleatorias en una lista

    poblacion = []

    for i in range (0, CANT_POB):
        conj_aux = []
        vestido = False
        
        # Sombrero aleatorio
        prend_aux = l_sombreros[random.randint(0, len(l_sombreros)-1)]
        conj_aux.append(prend_aux)
        
        # Camisa aleatoria o vestido
        prend_aux = l_camisas[random.randint(0, len(l_camisas)-1)]
        conj_aux.append(prend_aux)
        
        if(prend_aux.tipo == "Vestido"):
            vestido = True
        
        # Si es vestido, se omite el pantalon y se pone en su lugar el mismo vestido
        if(vestido == True):
            conj_aux.append(prend_aux)
        else:
            # Pantalon o falda aleatoria
            prend_aux = l_pant[random.randint(0, len(l_pant)-1)]
            conj_aux.append(prend_aux)
        
        # Abrigo aleatorio
        prend_aux = l_abrigos[random.randint(0, len(l_abrigos)-1)]
        conj_aux.append(prend_aux)
        
        # Calzado aleatorio
        prend_aux = l_calzado[random.randint(0, len(l_calzado)-1)]
        conj_aux.append(prend_aux)
        
        # Accesorio aleatorio
        prend_aux = l_accesorios[random.randint(0, len(l_accesorios)-1)]
        conj_aux.append(prend_aux)
        
        # Se agrega el conjunto aleatorio a la lista de poblacion, se calcula el valor fitness al crear el objeto
        poblacion.append(conjunto(conj_aux))
            

    # Hacer loop en donde al azar se van escogiendo 2 conjuntos y se combinan para ir generando la nueva generacion

    final = False
    gen = 1
    while(gen <= MAX_GEN and final == False):
        
        # Se ordena la lista de conjuntos de acuerdo a su valor fitness
        ranking_pob = []
        for c in poblacion:
            ranking_pob.append((float(copy.deepcopy(c.fit)),c))
        ranking_pob.sort(key=lambda x: x[0])
        ranking_pob.reverse()
        
        print("\n---------- Generacion ", gen," ----------")
        ranking_pob[0][1].mostrar_consola()
        
        if(ranking_pob[0][0] > 9.8):
            final = True
            break
        
        if(gen < MAX_GEN):
            # Generar pool de seleccion
            total = 0
            for i in range(0, len(ranking_pob)):
                total += ranking_pob[i][0]
            pool = []
            for i in range(0, len(ranking_pob)):
                n = round(ranking_pob[i][0] * (1000/total))
                if(n != 0):
                    for j in range (0, n):
                        pool.append(ranking_pob[i][1])
            
            # Realiza los cruces para la nueva generacion
            nueva_gen = []
            for i in range (0, CANT_POB):
                padre1 = random.randint(0, len(pool)-1)
                padre2 = random.randint(0, len(pool)-1)
                nueva_gen.append(conjunto(cruzar(pool[padre1], pool[padre2])))
            
            # Se mutan los conjuntos segun la probabilidad de mutacion
            for i in range(0, len(nueva_gen)):
                probmut = random.uniform(1.0, 1000.0)
                if(probmut <= P_MUTACION):
                    mutar(nueva_gen[i])
            
            for i in range(0, len(nueva_gen)):
                nueva_gen[i].fitness()
            
            poblacion = nueva_gen
        gen += 1

    if(gen > MAX_GEN):
        final = True

    # Se muestran los 10 mejores resultados de la ultima generacion en consola
    if(final == True):
        if(gen > MAX_GEN):
            gen = MAX_GEN
        
        print("\n\n________________RESULTADOS_______________")
        print("              Generacion ", gen)
        print("")
        mostrar_caract(caract)
        
        borrar_rep()
        
        for i in range(0, 10):
            ranking_pob[i][1].mostrar_consola()
            if(i<3):
                conjf[i] = ranking_pob[i][1].getIDs()
                puntua_f[i] = ranking_pob[i][0]
        
        for i in range(0,3):
            print(conjf[i])

# ---------------------------------------------------------------------------

# PARTE GRAFICA

ancho = 1120
alto = 630

v_actual = 1

fuente1 = ("Candara", 12, "bold")
fuente2 = ("Candara", 12)
fuente3 = ("Candara", 18, "bold")
clr_header = "#A17AA9"
clr_fondo = "#FCF1FF"
clr_inter = "#E0CCE5"
clr_texto1 = "white"

s_inputs = []


# Crear ventana
ventana = tkinter.Tk(className='Proyecto - Recomendador de prendas para audiovisuales')

# Redimensionar ventana
ventana.geometry("1120x630")

ventana.configure(bg="#FCF1FF")

p1 = tkinter.Frame(ventana, width = ancho, height = alto, bg=clr_fondo)
p2 = tkinter.Frame(ventana, width = ancho, height = alto, bg=clr_fondo)

p1.pack(fill = "both", expand = 1)

s_edad = StringVar()
s_genero = StringVar()
s_estilo = StringVar()
s_clima = StringVar()
s_generocine = StringVar()
s_epoca = StringVar()


l_img = [[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None]]
imgstk = [[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None]]
im = [[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None]]


def numero_op(nom):
    if(nom == "Seleccione"):
        return None
    elif(nom == "Hombre"):
        return 0
    elif(nom == "Mujer"):
        return 1
    elif(nom == "Accion"):
        return 2
    elif(nom == "Terror"):
        return 3
    elif(nom == "Comedia"):
        return 4
    elif(nom == "Drama"):
        return 5
    elif(nom == "Western"):
        return 6
    elif(nom == "Moderna"):
        return 7
    elif(nom == "80s"):
        return 8
    elif(nom == "50s"):
        return 9
    elif(nom == "20s"):
        return 10
    elif(nom == "Dorada"):
        return 11
    elif(nom == "Frio"):
        return 12
    elif(nom == "Calor"):
        return 13
    elif(nom == "Templado"):
        return 14
    elif(nom == "Infante"):
        return 15
    elif(nom == "Joven"):
        return 16
    elif(nom == "Adulto"):
        return 17
    elif(nom == "Anciano"):
        return 18
    elif(nom == "Formal"):
        return 19
    elif(nom == "Casual"):
        return 20

def abrir_v1():
    p1.pack(fill = "both", expand = 1)
    b_generar.config(text="Generar")
    p2.forget()

def abrir_v2():
    p2.pack(fill = "both", expand = 1)
    p1.forget()
    
def ejecutar():
    global caract, b_generar
    caract = []
    
    aux = s_genero.get()
    if(numero_op(aux) != None):
        caract.append(numero_op(aux))
        
    aux = s_generocine.get()
    if(numero_op(aux) != None):
        caract.append(numero_op(aux))
        
    aux = s_epoca.get()
    if(numero_op(aux) != None):
        caract.append(numero_op(aux))
    
    aux = s_clima.get()
    if(numero_op(aux) != None):
        caract.append(numero_op(aux))
        
    aux = s_edad.get()
    if(numero_op(aux) != None):
        caract.append(numero_op(aux))
        
    aux = s_estilo.get()
    if(numero_op(aux) != None):
        caract.append(numero_op(aux))
    
    aux = ""
    print(caract)
    
    if(len(caract) != 0):
        b_generar.config(text="CARGANDO...")
        # b_recalcular.config(text="CARGANDO...")
        backend()
        pantalla2()
        abrir_v2()
    else:
        print("No ha realizado ninguna seleccion")
        
    

def general():
    header = tkinter.Frame(ventana, width = ancho, height = 60, bg = clr_header)
    header.place(x=0, y=0)
    
    boton1 = tkinter.Button(ventana, text = "Vestuarios creados", command = abrir_v2, font = fuente1, bg = clr_header, fg = clr_texto1, activebackground="#8547A9", activeforeground = clr_texto1)
    boton1.place(x=40, y=10, width=150, height=35)
    
    boton2 = tkinter.Button(ventana, text = "Crear vestuario", command = abrir_v1, font = fuente1, bg = clr_header, fg = clr_texto1, activebackground="#8547A9", activeforeground = clr_texto1)
    boton2.place(x=210, y=10, width=150, height=35)

# Pantalla 1 ------------------

b_generar = tkinter.Button(p1, text = "Generar", command = ejecutar, font = fuente1, bg = clr_header, fg = clr_texto1, activebackground="#8547A9", activeforeground = clr_texto1)


def pantalla1():
    
    global b_generar
    
    lb1 = tkinter.Label(p1, text = "INICIA LA CREACIÓN DEL VESTUARIO", font = fuente3, bg = clr_fondo)
    lb1.place(x=350, y=100)
    
    lb2 = tkinter.Label(p1, text = "Completa esta serie de opciones y te indicaremos el vestuario mas apropiado para tu personaje.", font = fuente2, bg = clr_fondo)
    lb2.place(x=60, y=160)
    
    lb3 = tkinter.Label(p1, text = "Sobre el personaje.", font = fuente1, bg = clr_fondo)
    lb3.place(x=40, y=240)
    
    # EDAD ------------------
    s_edad.set("Seleccione")
    
    lb_edad = tkinter.Label(p1, text = "Edad", font = fuente1, bg = clr_fondo)
    lb_edad.place(x=60, y=275)
    
    dropd_edad = tkinter.OptionMenu(p1, s_edad, "Infante", "Joven", "Adulto", "Anciano")
    dropd_edad.config(bg = "white", font = fuente2)
    
    dropd_edad["menu"].config(bg = "white", font = fuente2)
    dropd_edad.place(x=60, y=300, width=150, height=35)
    
    # GENERO ------------------
    s_genero.set("Seleccione")
    
    lb_genero = tkinter.Label(p1, text = "Género", font = fuente1, bg = clr_fondo)
    lb_genero.place(x=60, y=360)
    
    dropd_genero = tkinter.OptionMenu(p1, s_genero, "Hombre", "Mujer")
    dropd_genero.config(bg = "white", font = fuente2)
    
    dropd_genero["menu"].config(bg = "white", font = fuente2)
    dropd_genero.place(x=60, y=385, width=150, height=35)
    
    # ESTILO ------------------
    s_estilo.set("Seleccione")
    
    lb_estilo = tkinter.Label(p1, text = "Estilo", font = fuente1, bg = clr_fondo)
    lb_estilo.place(x=60, y=445)
    
    dropd_estilo = tkinter.OptionMenu(p1, s_estilo, "Formal", "Casual")
    dropd_estilo.config(bg = "white", font = fuente2)
    
    dropd_estilo["menu"].config(bg = "white", font = fuente2)
    dropd_estilo.place(x=60, y=470, width=150, height=35)
    
    # --------------
    lb4 = tkinter.Label(p1, text = "Sobre la escena.", font = fuente1, bg = clr_fondo)
    lb4.place(x=450, y=240)
    
    # CLIMA ------------------
    s_clima.set("Seleccione")
    
    lb_clima = tkinter.Label(p1, text = "Clima", font = fuente1, bg = clr_fondo)
    lb_clima.place(x=470, y=275)
    
    dropd_clima = tkinter.OptionMenu(p1, s_clima, "Frio", "Calor", "Templado")
    dropd_clima.config(bg = "white", font = fuente2)
    
    dropd_clima["menu"].config(bg = "white", font = fuente2)
    dropd_clima.place(x=470, y=300, width=150, height=35)
    
    # --------------
    lb5 = tkinter.Label(p1, text = "Sobre la produccion.", font = fuente1, bg = clr_fondo)
    lb5.place(x=860, y=240)
    
    # GENERO CINE -------------------
    s_generocine.set("Seleccione")
    
    lb_generocine = tkinter.Label(p1, text = "Género cinematográfico", font = fuente1, bg = clr_fondo)
    lb_generocine.place(x=880, y=275)
    
    dropd_generocine = tkinter.OptionMenu(p1, s_generocine, "Accion", "Terror", "Comedia", "Drama", "Western")
    dropd_generocine.config(bg = "white", font = fuente2)
    
    dropd_generocine["menu"].config(bg = "white", font = fuente2)
    dropd_generocine.place(x=880, y=300, width=150, height=35)
    
    # EPOCA ------------------
    s_epoca.set("Seleccione")
    
    lb_epoca = tkinter.Label(p1, text = "Época", font = fuente1, bg = clr_fondo)
    lb_epoca.place(x=880, y=360)
    
    dropd_epoca = tkinter.OptionMenu(p1, s_epoca, "Moderna", "80s", "50s", "20s", "Dorada")
    dropd_epoca.config(bg = "white", font = fuente2)
    
    dropd_epoca["menu"].config(bg = "white", font = fuente2)
    dropd_epoca.place(x=880, y=385, width=150, height=35)
    
    # Boton generar --------------
    
    # b_generar = tkinter.Button(p1, text = "Generar", command = ejecutar, font = fuente1, bg = clr_header, fg = clr_texto1, activebackground="#8547A9", activeforeground = clr_texto1)
    b_generar.place(x=460, y=550, width=200, height=40)

# Pantalla 2 ------------------
def pantalla2():
    global imgs1, conjf, b_recalcular, puntua_f
    fondo1 = tkinter.Frame(p2, width = ancho, height = 120, bg = clr_inter)
    fondo1.place(x=0, y=60)
    
    lb4 = tkinter.Label(p2, text = "VISTE A TUS PERSONAJES", font = fuente3, bg = clr_inter)
    lb4.place(x=400, y=80)
    
    lb5 = tkinter.Label(p2, text = "Encuentra un vestuario apropiado para tu personaje.", font = fuente2, bg = clr_inter)
    lb5.place(x=60, y=140)
    
    lb6 = tkinter.Label(p2, text = "Vestuarios creados", font = fuente1, bg = clr_fondo)
    lb6.place(x=60, y=185)
    
    b_recalcular = tkinter.Button(p2, text = "Recalcular", command = ejecutar, font = fuente1, bg = clr_header, fg = clr_texto1, activebackground="#8547A9", activeforeground = clr_texto1)
    b_recalcular.place(x=920, y=140, width=160, height=30)
    
    card = [None, None, None]
    cint = [None, None, None]
    
    card[0] = tkinter.Frame(p2, bg = "black")
    cint[0] = tkinter.Label(card[0], bg = "white")
    cint[0].pack(fill = "both", expand = True,padx=1,pady=1)
    card[0].place(x=40, y=225,width = 280, height = 360)
    
    if(puntua_f[0] != None):
        lb_p1 = tkinter.Label(p2, text = "Puntaje: "+str(round(puntua_f[0],3)), font = fuente1, bg = clr_fondo)
        lb_p1.place(x=40, y=590)
    
    card[1] = tkinter.Frame(p2, bg = "black")
    cint[1] = tkinter.Label(card[1], bg = "white")
    cint[1].pack(fill = "both", expand = True,padx=1,pady=1)
    card[1].place(x=420, y=225,width = 280, height = 360)
    
    if(puntua_f[1] != None):
        lb_p2 = tkinter.Label(p2, text = "Puntaje: "+str(round(puntua_f[1],3)), font = fuente1, bg = clr_fondo)
        lb_p2.place(x=420, y=590)
    
    card[2] = tkinter.Frame(p2, bg = "black")
    cint[2] = tkinter.Label(card[2], bg = "white")
    cint[2].pack(fill = "both", expand = True,padx=1,pady=1)
    card[2].place(x=800, y=225,width = 280, height = 360)
    
    if(puntua_f[2] != None):
        lb_p3 = tkinter.Label(p2, text = "Puntaje: "+str(round(puntua_f[2],3)), font = fuente1, bg = clr_fondo)
        lb_p3.place(x=800, y=590)
    
    for i in range(0,3):
        if(conjf[i] != None):
            if(conjf[i][1] != conjf[i][2]):
                # Camisa
                im_path = "imagenes/"+str(conjf[i][1])+".png"
                im[i][0] = Image.open(im_path)
                im[i][0] = im[i][0].resize((110, 110), Image.ANTIALIAS)
                imgstk[i][0] = ImageTk.PhotoImage(im[i][0])
                l_img[i][0] = tkinter.Label(card[i], image = imgstk[i][0], bg="white")
                l_img[i][0].place(relx=0.05,rely=0.01)
                
                # Pantalon
                im_path = "imagenes/"+str(conjf[i][2])+".png"
                im[i][1] = Image.open(im_path)
                im[i][1] = im[i][1].resize((110, 110), Image.ANTIALIAS)
                imgstk[i][1] = ImageTk.PhotoImage(im[i][1])
                l_img[i][1] = tkinter.Label(card[i], image = imgstk[i][1], bg="white")
                l_img[i][1].place(relx=0.05,rely=0.34)
            else:
                # Vestido
                im_path = "imagenes/"+str(conjf[i][1])+".png"
                im[i][0] = Image.open(im_path)
                im[i][0] = im[i][0].resize((110, 220), Image.ANTIALIAS)
                imgstk[i][0] = ImageTk.PhotoImage(im[i][0])
                l_img[i][0] = tkinter.Label(card[i], image = imgstk[i][0], bg="white")
                l_img[i][0].place(relx=0.05,rely=0.01)
        
            # Zapatos
            im_path = "imagenes/"+str(conjf[i][4])+".png"
            im[i][2] = Image.open(im_path)
            im[i][2] = im[i][2].resize((110, 110), Image.ANTIALIAS)
            imgstk[i][2] = ImageTk.PhotoImage(im[i][2])
            l_img[i][2] = tkinter.Label(card[i], image = imgstk[i][2], bg="white")
            l_img[i][2].place(relx=0.05,rely=0.67)
            
            # Sombrero
            im_path = "imagenes/"+str(conjf[i][0])+".png"
            im[i][3] = Image.open(im_path)
            im[i][3] = im[i][3].resize((110, 110), Image.ANTIALIAS)
            imgstk[i][3] = ImageTk.PhotoImage(im[i][3])
            l_img[i][3] = tkinter.Label(card[i], image = imgstk[i][3], bg="white")
            l_img[i][3].place(relx=0.55,rely=0.01)
            
            # Chaqueta
            im_path = "imagenes/"+str(conjf[i][3])+".png"
            im[i][4] = Image.open(im_path)
            im[i][4] = im[i][4].resize((110, 110), Image.ANTIALIAS)
            imgstk[i][4] = ImageTk.PhotoImage(im[i][4])
            l_img[i][4] = tkinter.Label(card[i], image = imgstk[i][4], bg="white")
            l_img[i][4].place(relx=0.55,rely=0.34)
            
            # Accesorio
            im_path = "imagenes/"+str(conjf[i][5])+".png"
            im[i][5] = Image.open(im_path)
            im[i][5] = im[i][5].resize((110, 110), Image.ANTIALIAS)
            imgstk[i][5] = ImageTk.PhotoImage(im[i][5])
            l_img[i][5] = tkinter.Label(card[i], image = imgstk[i][5], bg="white")
            l_img[i][5].place(relx=0.55,rely=0.67)
    

general()
pantalla1()
pantalla2()

# Main loop necesario siempre, lleva registro de lo que sucede
ventana.mainloop()