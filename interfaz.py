from tkinter import messagebox, filedialog
from tkinter import *
import clase_definitiva as cla
import idiomas as idi

idiomas = idi.get_idiomas()

modulo = cla.modulo_clasificador()

global results
global parameters

##Funciones MachineLearning
def crearDatasets():
    x = modulo.find_features()
    if x:
        y = modulo.crear_datasets()
        if y:
            menubar.entryconfig(3, state=NORMAL)
            menubar.entryconfig(4, state=NORMAL)
        else:
            messagebox.showerror(idiomas[controlador.idioma][22], idiomas[controlador.idioma][22])
    else:
        messagebox.showerror(idiomas[controlador.idioma][22], idiomas[controlador.idioma][22])


####Funciones Cambiar el idioma de los textos
# =============================================#

class Controlador:

    def __init__(self, idioma):
        self.bestMetrics = ""
        self.idioma = idioma
        self.corpus = ""
        self.corpusCargado = False
        self.fuente = 30

        self.bestParams= ""
        self.nombreCorpus="default"

    def cambiarIdioma(self, idioma2):
        self.idioma = idioma2


controlador = Controlador(0)






def cambiar_idioma(idiomap):
    controlador.cambiarIdioma(idiomap)
    root.title(idiomas[controlador.idioma][0])


    filemenu.entryconfig(0, label=idiomas[controlador.idioma][2])
    filemenu.entryconfig(1, label=idiomas[controlador.idioma][4])

    filemenu.entryconfig(3, label=idiomas[controlador.idioma][7])

    algorithmenu.entryconfig(0, label=idiomas[controlador.idioma][15])
    algorithmenu.entryconfig(1, label=idiomas[controlador.idioma][16])
    algorithmenu.entryconfig(2, label=idiomas[controlador.idioma][17])
    algorithmenu.entryconfig(4, label=idiomas[controlador.idioma][18])

    menubar.entryconfig(1, label=idiomas[controlador.idioma][6])
    menubar.entryconfig(2, label=idiomas[controlador.idioma][9])
    menubar.entryconfig(3, label=idiomas[controlador.idioma][19])
    menubar.entryconfig(4, label=idiomas[controlador.idioma][31])
    menubar.entryconfig(5, label=idiomas[controlador.idioma][34])



    ayuda.entryconfig(0,label=idiomas[controlador.idioma][32])
    ayuda.entryconfig(1,label=idiomas[controlador.idioma][33])


####Funciones Crear Ventanas Nuevas
# =============================================#

def validate_float(action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
    # action=1 -> insert
    if (action == '1'):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False


def create_window_LoadCorpus(hotkey):

    nombre= filedialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("csv files", "*.csv"), ("txt files", "*.txt")))
    if nombre!= '':
        window = Toplevel(root)
        window.filename=nombre
        window.geometry("+{}+{}".format(positionRight, positionDown))
        window.after(1, lambda: window.focus_force())
        window.grab_set()

        myLabel = Label(window, text=idiomas[controlador.idioma][10], font=controlador.fuente)
        myLabel.grid(row=0, column=0)

        label2 = Label(window, text=window.filename, font=controlador.fuente)
        label2.grid(row=1, column=0)

        label3 = Label(window, text=idiomas[controlador.idioma][22], font=controlador.fuente, fg="red")
        label3.grid(row=2, column=0)
    
        def onclick(event=None):

            filtro1=emojisvalue.get()
            filtro2=stopwordsvalue.get()
            if filtro1 and filtro2:
                positivos = modulo.cargar_corpus(window.filename,0)
            if filtro1 and not filtro2:
                positivos = modulo.cargar_corpus(window.filename, 3)
            if not filtro1 and  filtro2:
                positivos = modulo.cargar_corpus(window.filename, 1)
            if not filtro1 and not filtro2:
                positivos = modulo.cargar_corpus(window.filename, 2)


            if not positivos:
                messagebox.showerror(idiomas[controlador.idioma][12], idiomas[controlador.idioma][13] + window.filename)
            else:

                controlador.corpus = window.filename

                split=window.filename.split("/")
                controlador.nombreCorpus=split[len(split)-1].split(".")[0]
                root.title(idiomas[controlador.idioma][0]+ " * "+ split[len(split)-1])
                crearDatasets()
                window.destroy()


        window.bind('<Return>', onclick)
        button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick)
        button1.grid(row=5, column=0, columnspan=1, padx=10, pady=10)

        emojisvalue = BooleanVar(window)
        emojisvalue.set(True)
        stopwordsvalue = BooleanVar(window)
        stopwordsvalue.set(True)

        chemojis = Checkbutton(window, text=idiomas[controlador.idioma][35],variable=emojisvalue)
        chstopwords =Checkbutton(window, text=idiomas[controlador.idioma][36],variable=stopwordsvalue)
        chemojis.grid(row=3, column=0)
        chstopwords.grid(row=4, column=0)


def guardar_Parametros(self):
    root.filename = filedialog.asksaveasfilename(initialdir="./resultados",initialfile=controlador.nombreCorpus,
                                                 title="Select file",defaultextension="txt",
                                                 filetypes=(("txt", "*.txt"), ("all files", "*.*")))
    try:
        f = open(root.filename, "a")
        f.write(controlador.bestParams)
        f.write(controlador.bestMetrics)
        f.close()
    except OSError:
        print("Could not open/read file:", root.filename)

def create_Manual():
    window = Toplevel(root)
    window.geometry("+{}+{}".format(positionRight, positionDown))
    manual = open("manual_"+str(controlador.idioma)+".txt", "r", encoding="utf8").read()
    text= Text(window)
    text.insert(END,manual)
    text.pack()


def create_AboutMe():
    window = Toplevel(root)
    window.geometry("+{}+{}".format(positionRight, positionDown))
    nombre = Label(window, text="Autor: Pablo Luna Zaragoza",font=controlador.fuente)
    uja= Label(window, text="Universidad de Jaén",font=controlador.fuente)
    correo= Label(window, text="Mail uja: plz00003@red.ujaen.es",font=controlador.fuente)
    github= Label(window, text="Mail: paluzara@gmail.com",font=controlador.fuente)
    nombre.grid(row=0,column=0)
    uja.grid(row=1,column=0)
    correo.grid(row=2,column=0)
    github.grid(row=3,column=0)

def create_window_ezSVM():
    window = Toplevel(root)
    window.geometry("400x200")

    window.title("SVM")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    C_2d_range = [1e-2]
    gamma_2d_range = [1e-1]
    kernel_range = ["linear", "poly", "rbf", "sigmoid"]

    lcMin = Label(window, text="CMin")
    lcMin.place(x=20, y=20)


    cMin = Entry(window)
    cMin.insert(END, C_2d_range[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMin.focus_force()


    lgammaMin = Label(window, text="gMin")
    lgammaMin.place(x=20, y=80)


    gammaMin = Entry(window)
    gammaMin.insert(END, gamma_2d_range[0])
    gammaMin.place(x=20, y=100, width=50, height=30)


    Kernels = Label(window, text="Kernels : linear’, ‘poly’, ‘rbf’, ‘sigmoid", font=controlador.fuente)
    Kernels.place(x=30, y=150)

    ejecucuciones = Label(window, text="Nº Ejec:1x1x4=4 ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        valido=True
        if isfloat(cMin.get()):
            if float(cMin.get())>0:
                C_2d_range[0] = float(cMin.get())
            else:
                valido=False
        else:
            valido = False

        if isfloat(gammaMin.get()):
            if float(gammaMin.get()) > 0:
                gamma_2d_range[0] = float(gammaMin.get())
            else:
                valido = False
        else:
            valido = False
        if valido:
            maxNota=0.0
            window.destroy()
            ejecuciones.config(text=idiomas[controlador.idioma][37])
            i = 1
            for k in kernel_range:
                for c in C_2d_range:
                    for g in gamma_2d_range:
                        numero.config(text=str(i)+"/"+"4")
                        i+=1
                        parametros= modulo.crearSVC(c=c, kernel=k, gamma=g)
                        modulo.entrenar_algoritmo()
                        modulo.predecir()
                        metrics,nota=modulo.get_Metrics2(True)
                        if float(maxNota)<float(nota):
                            maxNota=float(nota)
                            controlador.bestMetrics=metrics
                            controlador.bestParams=parametros
                            res.config(text=controlador.bestMetrics)
                            params.config(text=controlador.bestParams)
                        root.update()

            ejecuciones.config(text="")
            numero.config(text="")
        else:
            messagebox.showerror(idiomas[controlador.idioma][38], idiomas[controlador.idioma][39])

    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)


def create_window_ezDecisionTree():
    window = Toplevel(root)
    window.geometry("400x200")

    window.title("Decision Tree")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    max_depth = ["None"]
    min_samples_split = [2]
    criterion_range = ["gini", "entropy"]
    splitter_range = ["best","random"]

    lcMin = Label(window, text=idiomas[controlador.idioma][26])
    lcMin.place(x=20, y=20)


    cMin = Entry(window)
    cMin.insert(END, max_depth[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMin.focus_force()


    lgammaMin = Label(window, text=idiomas[controlador.idioma][27])
    lgammaMin.place(x=20, y=80)

    gammaMin = Entry(window)
    gammaMin.insert(END, min_samples_split[0])
    gammaMin.place(x=20, y=100, width=50, height=30)


    Kernels = Label(window, text="Spliteers : 'best', ‘random’ Criterion: 'gini','entropy'", font=controlador.fuente)
    Kernels.place(x=30, y=150)

    ejecucuciones = Label(window, text="Nº Ejec:1x2x2=4 ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        if cMin.get()=="None":
            max_depth[0] = None
        else:
            max_depth[0] = int(cMin.get())


        min_samples_split[0] = int(gammaMin.get())

        maxNota=0.0
        window.destroy()
        ejecuciones.config(text=idiomas[controlador.idioma][37])
        i = 1
        for depth in max_depth:
            for sam in min_samples_split:
                for ra in criterion_range:
                    for splitter in splitter_range:
                        numero.config(text=str(i)+"/"+"4")
                        i+=1
                        parametros= modulo.crear_DecisionTree(criterion=ra,splitter=splitter,
                                                              min_samples_split=sam,max_depth=depth)
                        modulo.entrenar_algoritmo()
                        modulo.predecir()
                        metrics,nota=modulo.get_Metrics2(True)
                        if float(maxNota)<float(nota):
                            maxNota=float(nota)
                            controlador.bestMetrics=metrics
                            controlador.bestParams=parametros
                            res.config(text=controlador.bestMetrics)
                            params.config(text=controlador.bestParams)
                        root.update()

        ejecuciones.config(text="")
        numero.config(text="")


    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)


def create_window_ezRandomForest():
    window = Toplevel(root)
    window.geometry("400x280")

    window.title("Random Forest")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    max_depth = ["None"]
    min_samples_split = [2]
    criterion_range = ["gini"]
    n_arboles = [200]

    lcMin = Label(window, text=idiomas[controlador.idioma][26])
    lcMin.place(x=20, y=20)


    cMin = Entry(window)
    cMin.insert(END, max_depth[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMin.focus_force()


    lgammaMin = Label(window, text=idiomas[controlador.idioma][27])
    lgammaMin.place(x=20, y=80)

    gammaMin = Entry(window)
    gammaMin.insert(END, min_samples_split[0])
    gammaMin.place(x=20, y=100, width=50, height=30)


    lnarboles = Label(window, text=idiomas[controlador.idioma][28])
    lnarboles.place(x=20, y=150)

    n_arbolesMin = Entry(window)
    n_arbolesMin.insert(END, n_arboles[0])
    n_arbolesMin.place(x=20, y=180, width=50, height=30)


    Kernels = Label(window, text="Criterion: 'gini','entropy'", font=controlador.fuente)
    Kernels.place(x=30, y=230)

    ejecucuciones = Label(window, text="Nº Ejec:1x2 = 2 ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        if cMin.get()=="None":
            max_depth[0] = None
        else:
            max_depth[0] = int(cMin.get())


        n_arboles[0] = int(n_arbolesMin.get())


        min_samples_split[0] = int(gammaMin.get())

        maxNota=0.0
        window.destroy()
        ejecuciones.config(text=idiomas[controlador.idioma][37])
        i = 1
        for depth in max_depth:
            for sam in min_samples_split:
                for ra in criterion_range:
                    for arboles in n_arboles:
                        numero.config(text=str(i)+"/"+"2")
                        i+=1
                        parametros= modulo.crearRandomForest(criterion=ra,n_estimators=arboles,
                                                              min_samples_split=sam,max_depth=depth)
                        modulo.entrenar_algoritmo()
                        modulo.predecir()
                        metrics,nota=modulo.get_Metrics2(True)
                        if float(maxNota)<float(nota):
                            maxNota=float(nota)
                            controlador.bestMetrics=metrics
                            controlador.bestParams=parametros
                            res.config(text=controlador.bestMetrics)
                            params.config(text=controlador.bestParams)
                        root.update()

        ejecuciones.config(text="")
        numero.config(text="")


    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)



def create_window_SVM():
    window = Toplevel(root)
    window.geometry("400x200")

    window.title("SVM")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    C_2d_range = [1e-2, 1, 1e2]
    gamma_2d_range = [1e-1, 1, 1e1]
    kernel_range = ["linear", "poly", "rbf", "sigmoid"]

    lcMin = Label(window, text="CMin")
    lcMin.place(x=20, y=20)
    lcMid = Label(window, text="CMid")
    lcMid.place(x=80, y=20)
    lcMax = Label(window, text="CMax")
    lcMax.place(x=140, y=20)

    cMin = Entry(window)
    cMin.insert(END, C_2d_range[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMin.focus_force()
    cMid = Entry(window)
    cMid.insert(END, C_2d_range[1])
    cMid.place(x=80, y=40, width=50, height=30)
    cMax = Entry(window)
    cMax.insert(END, C_2d_range[2])
    cMax.place(x=140, y=40, width=50, height=30)

    lgammaMin = Label(window, text="gMin")
    lgammaMin.place(x=20, y=80)
    lgammaMid = Label(window, text="gMid")
    lgammaMid.place(x=80, y=80)
    lgammaMax = Label(window, text="gMax")
    lgammaMax.place(x=140, y=80)

    gammaMin = Entry(window)
    gammaMin.insert(END, gamma_2d_range[0])
    gammaMin.place(x=20, y=100, width=50, height=30)
    gammaMid = Entry(window)
    gammaMid.insert(END, gamma_2d_range[1])
    gammaMid.place(x=80, y=100, width=50, height=30)
    gammaMax = Entry(window)
    gammaMax.insert(END, gamma_2d_range[2])
    gammaMax.place(x=140, y=100, width=50, height=30)

    Kernels = Label(window, text="Kernels : linear’, ‘poly’, ‘rbf’, ‘sigmoid", font=controlador.fuente)
    Kernels.place(x=30, y=150)

    ejecucuciones = Label(window, text="Nº Ejec:3x3x4=36 ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        valido = True
        if isfloat(cMin.get()):
            if float(cMin.get())>=0:
                C_2d_range[0] = float(cMin.get())
            else:
                valido=False
        else:
            valido=False
        if isfloat(cMid.get()):
            C_2d_range[1] = float(cMid.get())
        else:
            valido = False
        if isfloat(cMax.get()):
            C_2d_range[2] = float(cMax.get())
        else:
            valido = False
        if isfloat(gammaMin.get()):
            gamma_2d_range[0] = float(gammaMin.get())
        else:
            valido = False
        if isfloat(gammaMid.get()):
            gamma_2d_range[1] = float(gammaMid.get())
        else:
            valido = False
        if isfloat(gammaMax.get()):
            gamma_2d_range[2] = float(gammaMax.get())
        else:
            valido = False

        if valido:
            maxNota=0.0
            window.destroy()
            ejecuciones.config(text=idiomas[controlador.idioma][37])
            i = 1
            for k in kernel_range:
                for c in C_2d_range:
                    for g in gamma_2d_range:
                        numero.config(text=str(i)+"/"+"36")
                        i+=1
                        parametros= modulo.crearSVC(c=c, kernel=k, gamma=g)
                        modulo.entrenar_algoritmo()
                        modulo.predecir()
                        metrics,nota=modulo.get_Metrics2(True)
                        if float(maxNota)<float(nota):
                            maxNota=float(nota)
                            controlador.bestMetrics=metrics
                            controlador.bestParams=parametros
                            res.config(text=controlador.bestMetrics)
                            params.config(text=controlador.bestParams)
                        root.update()

            ejecuciones.config(text="")
            numero.config(text="")
        else:
            messagebox.showerror(idiomas[controlador.idioma][38], idiomas[controlador.idioma][39])

    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)


def create_window_DecisionTree():
    window = Toplevel(root)
    window.geometry("400x200")

    window.title("Decision Tree")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    max_depth = ["None", 10, 100]
    min_samples_split = [2, 3, 4]
    criterion_range = ["gini", "entropy"]
    splitter_range = ["best","random"]

    lcMin = Label(window, text=idiomas[controlador.idioma][26])
    lcMin.place(x=20, y=20)


    cMin = Entry(window)
    cMin.insert(END, max_depth[0])
    cMin.focus_force()
    cMin.place(x=20, y=40, width=50, height=30)
    cMid = Entry(window)
    cMid.insert(END, max_depth[1])
    cMid.place(x=80, y=40, width=50, height=30)
    cMax = Entry(window)
    cMax.insert(END, max_depth[2])
    cMax.place(x=140, y=40, width=50, height=30)

    lgammaMin = Label(window, text=idiomas[controlador.idioma][27])
    lgammaMin.place(x=20, y=80)

    gammaMin = Entry(window)
    gammaMin.insert(END, min_samples_split[0])
    gammaMin.place(x=20, y=100, width=50, height=30)
    gammaMid = Entry(window)
    gammaMid.insert(END, min_samples_split[1])
    gammaMid.place(x=80, y=100, width=50, height=30)
    gammaMax = Entry(window)
    gammaMax.insert(END, min_samples_split[2])
    gammaMax.place(x=140, y=100, width=50, height=30)

    Kernels = Label(window, text="Spliteers : 'best', ‘random’ "+"\n"+"Criterion: 'gini','entropy'", font=controlador.fuente)
    Kernels.place(x=30, y=150)

    ejecucuciones = Label(window, text="Nº Ejec:=36 ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        valido=True
        if cMin.get()=="None":
            max_depth[0] = None
        else:
            if isint(cMin.get()):
                max_depth[0] = int(cMin.get())
            else:
                valido=False

        if isint(cMid.get()):
            max_depth[1] = int(cMid.get())
        else:
            valido = False
        if isint(cMax.get()):
            max_depth[2] = int(cMax.get())
        else:
            valido = False
        if isint(gammaMin.get()):
            min_samples_split[0] = int(gammaMin.get())
        else:
            valido = False
        if isint(gammaMid.get()):
            min_samples_split[1] = int(gammaMid.get())
        else:
            valido = False
        if isint(gammaMax.get()):
            min_samples_split[2] = int(gammaMax.get())
        else:
            valido = False
        if valido:
            maxNota=0.0
            window.destroy()
            ejecuciones.config(text=idiomas[controlador.idioma][37])
            i=1
            for depth in max_depth:
                for sam in min_samples_split:
                    for ra in criterion_range:
                        for splitter in splitter_range:
                            numero.config(text=str(i)+"/"+"36")
                            i+=1
                            parametros= modulo.crear_DecisionTree(criterion=ra,splitter=splitter,
                                                                  min_samples_split=sam,max_depth=depth)
                            modulo.entrenar_algoritmo()
                            modulo.predecir()
                            metrics,nota=modulo.get_Metrics2(True)
                            if float(maxNota)<float(nota):
                                maxNota=float(nota)
                                controlador.bestMetrics=metrics
                                controlador.bestParams=parametros
                                res.config(text=controlador.bestMetrics)
                                params.config(text=controlador.bestParams)
                        root.update()
            ejecuciones.config(text="")
            numero.config(text="")
        else:
            messagebox.showerror(idiomas[controlador.idioma][38], idiomas[controlador.idioma][39])




    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)


def create_window_RandomForest():
    window = Toplevel(root)
    window.geometry("400x280")

    window.title("Random Forest")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    max_depth = ["None", 10, 100]
    min_samples_split = [2, 3, 4]
    criterion_range = ["gini", "entropy"]
    n_arboles = [200,300,400]

    lcMin = Label(window, text=idiomas[controlador.idioma][26])
    lcMin.place(x=20, y=20)


    cMin = Entry(window)
    cMin.insert(END, max_depth[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMid = Entry(window)
    cMid.insert(END, max_depth[1])
    cMid.place(x=80, y=40, width=50, height=30)
    cMax = Entry(window)
    cMax.insert(END, max_depth[2])
    cMax.place(x=140, y=40, width=50, height=30)

    lgammaMin = Label(window, text=idiomas[controlador.idioma][27])
    lgammaMin.place(x=20, y=80)

    gammaMin = Entry(window)
    gammaMin.insert(END, min_samples_split[0])
    gammaMin.place(x=20, y=100, width=50, height=30)
    gammaMid = Entry(window)
    gammaMid.insert(END, min_samples_split[1])
    gammaMid.place(x=80, y=100, width=50, height=30)
    gammaMax = Entry(window)
    gammaMax.insert(END, min_samples_split[2])
    gammaMax.place(x=140, y=100, width=50, height=30)

    lnarboles = Label(window, text=idiomas[controlador.idioma][28])
    lnarboles.place(x=20, y=150)

    n_arbolesMin = Entry(window)
    n_arbolesMin.insert(END, n_arboles[0])
    n_arbolesMin.place(x=20, y=180, width=50, height=30)
    n_arbolesMid = Entry(window)
    n_arbolesMid.insert(END, n_arboles[1])
    n_arbolesMid.place(x=80, y=180, width=50, height=30)
    n_arbolesMax = Entry(window)
    n_arbolesMax.insert(END, n_arboles[2])
    n_arbolesMax.place(x=140, y=180, width=50, height=30)

    Kernels = Label(window, text="Criterion: 'gini','entropy'", font=controlador.fuente)
    Kernels.place(x=30, y=230)

    ejecucuciones = Label(window, text="Nº Ejec:2x3x3x3 = 54 ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        valido=True
        if cMin.get()=="None":
            max_depth[0] = None
        else:
            if isint(cMin.get()):
                max_depth[0] = int(cMin.get())
            else:
                valido=False

        if isint(cMid.get()):
            max_depth[1] = int(cMid.get())
        else:
            valido = False
        if isint(cMax.get()):
            max_depth[2] = int(cMax.get())
        else:
            valido = False
        if isint(gammaMin.get()):
            min_samples_split[0] = int(gammaMin.get())
        else:
            valido = False
        if isint(gammaMid.get()):
            min_samples_split[1] = int(gammaMid.get())
        else:
            valido = False
        if isint(gammaMax.get()):
            min_samples_split[2] = int(gammaMax.get())
        else:
            valido = False
        if isint(n_arbolesMin.get()):
            n_arboles[0] = int(n_arbolesMin.get())
        else:
            valido = False
        if isint(n_arbolesMid.get()):
            n_arboles[1] = int(n_arbolesMid.get())

        else:
            valido = False
        if isint(n_arbolesMax.get()):
            n_arboles[2] = int(n_arbolesMax.get())
        else:
            valido = False

        if valido:
            maxNota=0.0
            window.destroy()
            ejecuciones.config(text=idiomas[controlador.idioma][37])
            i=1
            for depth in max_depth:
                for sam in min_samples_split:
                    for ra in criterion_range:
                        for arboles in n_arboles:
                            numero.config(text=str(i)+"/"+"54")
                            i+=1
                            parametros= modulo.crearRandomForest(criterion=ra,n_estimators=arboles,
                                                                  min_samples_split=sam,max_depth=depth)
                            modulo.entrenar_algoritmo()
                            modulo.predecir()
                            metrics,nota=modulo.get_Metrics2(True)
                            if float(maxNota)<float(nota):
                                maxNota=float(nota)
                                controlador.bestMetrics=metrics
                                controlador.bestParams=parametros
                                res.config(text=controlador.bestMetrics)
                                params.config(text=controlador.bestParams)
                            root.update()

            ejecuciones.config(text="")
            numero.config(text="")
        else:
            messagebox.showerror(idiomas[controlador.idioma][38], idiomas[controlador.idioma][39])


    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)

def create_window_NaybeBayes():
    window = Toplevel(root)
    window.geometry("400x280")

    window.title("Naybe Bayes")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    alpha_range = [0, 1, 1.5,2,2.5,3]


    lcMin = Label(window, text=idiomas[controlador.idioma][29])
    lcMin.place(x=20, y=20)


    cMin = Entry(window)
    cMin.insert(END, alpha_range[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMid = Entry(window)
    cMid.insert(END, alpha_range[1])
    cMid.place(x=80, y=40, width=50, height=30)
    cMax = Entry(window)
    cMax.insert(END, alpha_range[2])
    cMax.place(x=140, y=40, width=50, height=30)


    gammaMin = Entry(window)
    gammaMin.insert(END, alpha_range[3])
    gammaMin.place(x=20, y=100, width=50, height=30)
    gammaMid = Entry(window)
    gammaMid.insert(END, alpha_range[4])
    gammaMid.place(x=80, y=100, width=50, height=30)
    gammaMax = Entry(window)
    gammaMax.insert(END, alpha_range[5])
    gammaMax.place(x=140, y=100, width=50, height=30)



    Kernels = Label(window,text=idiomas[controlador.idioma][30], font=controlador.fuente)
    Kernels.place(x=30, y=230)

    ejecucuciones = Label(window, text="Nº Ejec= 6  ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):
        valido=True
        if isfloat(cMin.get()) :
            if float(cMin.get())>=0:
                alpha_range[0] = float(cMin.get())
            else:
                valido = False
        else:
            valido=False
        if isfloat(cMin.get()) :
            alpha_range[1] = float(cMid.get())
        else:
            valido = False
        if isfloat(cMin.get()):
         alpha_range[2] = float(cMax.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[3] = float(gammaMin.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[4] = float(gammaMid.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[5] = float(gammaMax.get())
        else:
            valido = False

        if valido:
            maxNota=0.0
            window.destroy()
            ejecuciones.config(text=idiomas[controlador.idioma][37])
            i = 1
            for alpha in alpha_range:
                    numero.config(text=str(i)+"/"+"6")
                    i+=1
                    parametros= modulo.crearMultinomialNaybeBayes(alpha=alpha)
                    modulo.entrenar_algoritmo()
                    modulo.predecir()
                    metrics,nota=modulo.get_Metrics2(True)
                    if float(maxNota)<float(nota):
                        maxNota=float(nota)
                        controlador.bestMetrics=metrics
                        controlador.bestParams=parametros
                        res.config(text=controlador.bestMetrics)
                        params.config(text=controlador.bestParams)
                    root.update()

            ejecuciones.config(text="")
            numero.config(text="")
        else:
            messagebox.showerror(idiomas[controlador.idioma][38], idiomas[controlador.idioma][39])


    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)


def create_window_GaussianNaybeBayes():
    window = Toplevel(root)
    window.geometry("400x280")

    window.title("Gaussian Naybe Bayes")
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.grab_set()
    alpha_range = [1e-9, 1e-8, 1e-5, 1e-3, 0.01, 0.1]

    lcMin = Label(window, text=idiomas[controlador.idioma][29])
    lcMin.place(x=20, y=20)

    cMin = Entry(window)
    cMin.insert(END, alpha_range[0])
    cMin.place(x=20, y=40, width=50, height=30)
    cMid = Entry(window)
    cMid.insert(END, alpha_range[1])
    cMid.place(x=80, y=40, width=50, height=30)
    cMax = Entry(window)
    cMax.insert(END, alpha_range[2])
    cMax.place(x=140, y=40, width=50, height=30)

    gammaMin = Entry(window)
    gammaMin.insert(END, alpha_range[3])
    gammaMin.place(x=20, y=100, width=50, height=30)
    gammaMid = Entry(window)
    gammaMid.insert(END, alpha_range[4])
    gammaMid.place(x=80, y=100, width=50, height=30)
    gammaMax = Entry(window)
    gammaMax.insert(END, alpha_range[5])
    gammaMax.place(x=140, y=100, width=50, height=30)



    ejecucuciones = Label(window, text="Nº Ejec= 6  ", font=controlador.fuente)
    ejecucuciones.place(x=200, y=30)

    vcmd = (window.register(validate_float),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def onclick(event=None):

        if isfloat(cMin.get()):
            if float(cMin.get()) >= 0:
                alpha_range[0] = float(cMin.get())
            else:
                valido = False
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[1] = float(cMid.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[2] = float(cMax.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[3] = float(gammaMin.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[4] = float(gammaMid.get())
        else:
            valido = False
        if isfloat(cMin.get()):
            alpha_range[5] = float(gammaMax.get())
        else:
            valido = False

        if valido:
            maxNota = 0.0
            window.destroy()
            ejecuciones.config(text=idiomas[controlador.idioma][37])
            i = 1
            for alpha in alpha_range:
                numero.config(text=str(i)+"/"+"6")
                i+=1
                parametros = modulo.crearMultinomialNaybeBayes(alpha=alpha)
                modulo.entrenar_algoritmo()
                modulo.predecir()
                metrics, nota = modulo.get_Metrics2(True)
                if float(maxNota) < float(nota):
                    maxNota = float(nota)
                    controlador.bestMetrics = metrics
                    controlador.bestParams = parametros
                    res.config(text=controlador.bestMetrics)
                    params.config(text=controlador.bestParams)
                root.update()

            ejecuciones.config(text="")
            numero.config(text="")
        else:
            messagebox.showerror(idiomas[controlador.idioma][38], idiomas[controlador.idioma][39])


    window.bind('<Return>', onclick)
    button1 = Button(window, text=idiomas[controlador.idioma][1], command=onclick, width=10)
    button1.place(x=250, y=100)


####    INTERFAZ
# =============================================#


root = Tk()
root.title(idiomas[controlador.idioma][0])

root.geometry("400x500")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth() / 3 - windowWidth / 3)
positionDown = int(root.winfo_screenheight() / 3 - windowHeight / 3)

# Positions the window in the center of the page.

root.geometry("+{}+{}".format(positionRight, positionDown))

# menu
menubar = Menu(root)

#Archivo
filemenu = Menu(menubar, tearoff=0)
hotkey=1
filemenu.add_command(label=idiomas[controlador.idioma][2], command=lambda: create_window_LoadCorpus(hotkey),underline=1,accelerator="Ctrl+O")
filemenu.add_command(label=idiomas[controlador.idioma][4],command=lambda: guardar_Parametros(hotkey),underline=1,accelerator="Ctrl+S")
root.bind("<Control-s>", guardar_Parametros)
root.bind("<Control-o>",create_window_LoadCorpus)

filemenu.add_separator()
filemenu.add_command(label=idiomas[controlador.idioma][7], command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)

#Idiomas
langugemenu = Menu(menubar, tearoff=0)
langugemenu.add_command(label="Español", command=lambda: cambiar_idioma(idi.idioma.ESP.value))
langugemenu.add_command(label="English", command=lambda: cambiar_idioma(idi.idioma.ENG.value))
menubar.add_cascade(label="Idioma", menu=langugemenu)

root.config(menu=menubar)
#Algoritmos
algorithmenu = Menu(menubar, tearoff=0)
algorithmenu.add_command(label=idiomas[controlador.idioma][15], command=create_window_SVM)
algorithmenu.add_command(label=idiomas[controlador.idioma][16],command=create_window_DecisionTree)

algorithmenu.add_command(label=idiomas[controlador.idioma][17],command=create_window_RandomForest)
algorithmenu.add_command(label=idiomas[controlador.idioma][18],command=create_window_NaybeBayes)
algorithmenu.add_command(label="GaussNB",command=create_window_GaussianNaybeBayes)
menubar.add_cascade(label="Algoritmos", menu=algorithmenu, state=DISABLED)


#Ejecucion
single = Menu(menubar, tearoff=0)
single.add_command(label=idiomas[controlador.idioma][15], command=create_window_ezSVM)
single.add_command(label=idiomas[controlador.idioma][16],command=create_window_ezDecisionTree)
single.add_command(label=idiomas[controlador.idioma][17],command=create_window_ezRandomForest)

menubar.add_cascade(label=idiomas[controlador.idioma][31], menu=single, state=DISABLED)

#Ayuda
ayuda = Menu(menubar, tearoff=0)
ayuda.add_command(label=idiomas[controlador.idioma][32],command=create_Manual)
ayuda.add_command(label=idiomas[controlador.idioma][33],command=create_AboutMe)
menubar.add_cascade(label=idiomas[controlador.idioma][34], menu=ayuda)



# Pestaña Principal





ejecuciones = Label(root, font=controlador.fuente )
numero = Label(root, font=controlador.fuente)
#ejecuciones.place(x=30, y=10 )
#numero.place(x=200, y=10)
ejecuciones.grid(row=0,column=0)
numero.grid(row=0,column=1)

params = Label(root, state="active", font=controlador.fuente)
res = Label(root, state="active", font=controlador.fuente)
params.grid(row=1,column=0,columnspan=2)
res.grid(row=2,column=0,columnspan=2)

#params.place(x=200, y=40, width=200, height=280)
#res.place(x=150, y=360, width=320, height=200)

root.mainloop()
