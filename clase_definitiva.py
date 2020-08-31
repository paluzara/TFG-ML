from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import sklearn.naive_bayes
import sklearn.metrics

import filtro


class modulo_clasificador():
    def __init__(self):
        self.data = []
        self.data_labels = []
        self.algoritmo = 0
        self.vectorizer = CountVectorizer(
            analyzer='word',
            lowercase=False,
        )
        self.features_nd = []

        self.porcentajeEntrenamiendo = 0.80
        self.X_train = 0
        self.X_test = 0
        self.y_train = 0
        self.y_test = 0

        # Errors
        self.entrenado = False
        self.data_sets = False
        self.corpus_cargado = False
        self.features = False
        self.predict = False



    def cargar_corpus(self, ruta,tipofiltro):
        try:
            corpus = open(ruta, "r", encoding="utf8").read()
        except OSError:
            print("Could not open/read file:", ruta)
            return False
        else:

            for i in corpus.split("\n"):

                split = i.split("|")
                if len(split)>1:
                    x=""
                    if tipofiltro == 0:
                        x = filtro.filtrar_soft(split[1])
                    if tipofiltro == 1:
                        x = filtro.filtrar_soft_con_emojis(split[1])
                    if tipofiltro == 2:
                        x = filtro.filtrar_conEmojis_YstopWords(split[1])
                    if tipofiltro == 3:
                        x = filtro.filtrar_constopWords(split[1])

                    self.data.append(x)
                    if (split[2] == "1"):
                        self.data_labels.append(1)
                    else:
                        self.data_labels.append(0)
            print("Text Clean =======================")
            self.corpus_cargado = True
            return True

    def find_features(self):
        if not self.corpus_cargado:
            raise ValueError("Load Corpus First")
        else:
            features = self.vectorizer.fit_transform(self.data)

            self.features_nd = features.toarray()
            self.features = True
            return True

    def crear_datasets(self):
        if not self.features:
            raise ValueError("Find Features First")
        else:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.features_nd,
                self.data_labels,
                train_size=self.porcentajeEntrenamiendo,
                random_state=5678)
            self.data_sets = True
            return True

    # var algoritmo: Algoritmo de ML con los parametros que quiera probar
    def entrenar_algoritmo(self ):
        if not self.data_sets:
            raise ValueError("Define Datasets First")
        else:

            self.algoritmo.fit(X=self.X_train, y=self.y_train)
            print("Algoritmo Entrenado")
            self.entrenado = True
            return True

    def predecir(self):
        if not self.data_sets:
            raise ValueError("Train Algorithm First")
        else:
            self.y_pred = self.algoritmo.predict(self.X_test)
            self.predict = True
            return True

    def get_Metrics(self):
        return sklearn.metrics.classification_report(self.y_test, self.y_pred)

    def get_Metrics2(self,criterio):
        metrics=""
        acc = sklearn.metrics.accuracy_score(self.y_test, self.y_pred)
       # prec=self.calcular_precision_score()
        f1 = self.calcular_f1()
       # recall = self.calcular_recall_score()
        metrics += "Accuracy Score: " + str(acc*100) +"%"+ "\n"
       # metrics += "                 precision  recall    f1-score"+ "\n"
       # metrics +="            0    "+str(round(prec[0],2))+"       "+str(round(recall[0],2))+"      "+str(round(f1[0],2))+ "\n"
       # metrics +="            1    "+str(round(prec[1],2))+"       "+str(round(recall[1],2))+"      "+str(round(f1[1],2))+ "\n"
       # metrics += "   Macro AVG     " + str(round(prec[2],2))+"      "+str(round(recall[2],2))+"      "+str(round(f1[2],2))+ "\n"
       # metrics += "Weighted AVG     " + str(round(prec[3],2))+"     "+str(round(recall[3],2))+"      "+str(round(f1[3],2))+ "\n"
        metrics+=self.get_Metrics()
        metrics+="\n"
        if(criterio):

            return metrics, acc
        else:
            return metrics,f1[2]


    def calcular_f1(self):

        x=sklearn.metrics.f1_score(self.y_test, self.y_pred,pos_label=0,average="binary")
        z=sklearn.metrics.f1_score(self.y_test, self.y_pred, pos_label=1, average="binary")
        w=sklearn.metrics.f1_score(self.y_test, self.y_pred,  average="macro")
        s=sklearn.metrics.f1_score(self.y_test, self.y_pred,  average="weighted")

        return x,z,w,s

    def calcular_recall_score(self):

        x=sklearn.metrics.recall_score(self.y_test, self.y_pred,pos_label=0,average="binary")
        z=sklearn.metrics.recall_score(self.y_test, self.y_pred, pos_label=1, average="binary")
        w=sklearn.metrics.recall_score(self.y_test, self.y_pred,  average="macro")
        s=sklearn.metrics.recall_score(self.y_test, self.y_pred,  average="weighted")

        return x,z,w,s

    def calcular_precision_score(self):

        x=sklearn.metrics.precision_score(self.y_test, self.y_pred,pos_label=0,average="binary")
        z=sklearn.metrics.precision_score(self.y_test, self.y_pred, pos_label=1, average="binary")
        w=sklearn.metrics.precision_score(self.y_test, self.y_pred,  average="macro")
        s=sklearn.metrics.precision_score(self.y_test, self.y_pred,  average="weighted")

        return x,z,w,s

    def precision_recall_fscore_support(self):

        x=sklearn.metrics.precision_recall_fscore_support(self.y_test, self.y_pred,pos_label=0,average="binary")
        z=sklearn.metrics.precision_recall_fscore_support(self.y_test, self.y_pred, pos_label=1, average="binary")
        w=sklearn.metrics.precision_recall_fscore_support(self.y_test, self.y_pred,  average="macro")
        s=sklearn.metrics.precision_recall_fscore_support(self.y_test, self.y_pred,  average="weighted")
        return x, z, w, s
    

    def crear_DecisionTree(self, criterion="gini", splitter="best", max_depth=None, min_samples_split=2):
        self.algoritmo = sklearn.tree.DecisionTreeClassifier(criterion=criterion, splitter=splitter
                                                             , max_depth=max_depth, min_samples_split=min_samples_split)
        parametros=""
        parametros +="****** DECISION TREE ******"+ "\n"
        parametros +="Valor de los parametros: "+ "\n"
        parametros += "-Criterion: " + str(criterion) + "\n"
        parametros += "-Splitter: "  +  str(splitter) + "\n"
        parametros += "-Max_Depth: " + str(max_depth) + "\n"
        parametros += "-Min_Samples_split: " + str(min_samples_split)+ "\n"

        return parametros


    def crearSVC(self,gamma ,c=1.0, kernel='rbf' ):

        self.algoritmo = SVC(C=float(c), kernel=kernel,  gamma=float(gamma))
        parametros=""
        parametros += "****** SVM ******"+ "\n"
        parametros += "Valor de los parametros: " + "\n"
        parametros += "-C param: " + str(c) + "\n"
        parametros += "-Kernel: " + str(kernel) + "\n"
        parametros += "-Gamma: " + str(gamma) + "\n"

        return parametros


    def crearGaussianNaybeBayes(self, var_smoothing=1e-9):
        self.algoritmo = sklearn.naive_bayes.GaussianNB(var_smoothing=var_smoothing)
        parametros=""
        parametros += "****** GAUSSIAN NAYBEBAYES ******"+ "\n"
        parametros += "Valor de los parametros: " + "\n"
        parametros += "-Smoothing: " + str(var_smoothing) + "\n"
        return parametros


    def crearMultinomialNaybeBayes(self,alpha=1.0):
        self.algoritmo = sklearn.naive_bayes.MultinomialNB(alpha=alpha)
        parametros=""
        parametros += "****** MULTINOMIAL NAYBEBAYES ******"+ "\n"
        parametros += "Valor de los parametros: " + "\n"
        parametros += "-Alpha: " + str(alpha) + "\n"
        return parametros


    def crearRandomForest(self,n_estimators=100, criterion="gini",max_depth=None,min_samples_split=2):
        self.algoritmo = RandomForestClassifier(n_estimators=n_estimators,criterion=criterion
                                                ,max_depth=max_depth ,min_samples_split=min_samples_split)

        parametros=""
        parametros += "****** RANDOM FOREST ******"+ "\n"
        parametros += "Valor de los parametros: " + "\n"
        parametros += "-N_Arboles: " + str(n_estimators) + "\n"
        parametros += "-Criterion: " + str(criterion) + "\n"
        parametros += "-Max_Depth: " + str(max_depth )+ "\n"
        parametros += "-Min_Samples_split: " + str(min_samples_split) + "\n"

        return parametros






