def rlogList():
    string ='''
        rlogCarga()
        rlogHoldout()
        rlogFmin()
        #BICLASE
        rlogPredict()
        #MULTICLASE
        rlogY_change()
        rlogTraining()
        rlogPredictMulticlass()
        rlogAccuracy()
        rlogMain()
        rlogFull()

    '''
    print(string)

def rlogCarga():
    string = '''
        data = sio.loadmat("ex4data1.mat") # carga de archivo matlab, no es con pd.read_csv()
        X = pd.DataFrame(data['X'])
        y = pd.DataFrame(data['y'])
    '''
    print(string)


def rlogHoldout():
    string = '''
        def holdout(X, y, porcentage=0.7):
            X_training = X.sample(round(percentage*len(X)))  # Selecciona aleatoriamente el numero de filas indicado
            y_training = y.iloc[X_training.index]            # Selecciona las filas del X_training
            X_test = X.iloc[~X.index.isin(X_training.index)] # ~ significa NOT
            y_test = y.iloc[~X.index.isin(X_training.index)] # ~ significa NOT

            print("El tamaño del training debe ser: ", round(percentage*len(X)), " - Comprobación: tamaño X_training es ", len(X_training), " y tamaño y_training es", len(y_training))
            print("El tamaño del test debe ser: ", len(X)-round(percentage*len(X)), " - Comprobación: tamaño X_test es ", len(X_test), " y tamaño y_test es", len(y_test))

            # Reseteamos los índices de todos los conjuntos
            X_training = X_training.reset_index(drop=True)
            y_training = y_training.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)
            y_test = y_test.reset_index(drop=True)
            
            return X_training, y_training, X_test, y_test

        X_train, y_train, X_test, y_test = holdout(X, y, 0.75)

        '''
    print(string)

def rlogFmin():
    string = '''
        # FUNCIONES PARA FMIN

        def sigmoid(z):
            res = 1/(1+np.exp(-z))
            return res

        def computeCost(thetas, X, y):
            tam = X.shape[0]
            h = sigmoid(np.dot(X, thetas))
            J = 0.0
            J = (-1/tam)*(np.dot(y.T, np.log(h)) + np.dot((1-y).T, np.log(1-h)))
            return J

        def gradient(thetas, X, y):
            tam = X.shape[0]
            h = sigmoid(np.dot(X, thetas))
            J = 0.0
            J = (1/tam)*np.dot(X.T, (h-y))
            return J

        #para ejercicios NO MULTICLASE 
        theta = np.zeros((n+1,1))
        parametros_fmin = op.fmin_cg(maxiter = 200, f=costFunction, x0=theta.flatten(), fprime=gradientFunction, args=(X, y.to_numpy().flatten()))
        print("Thetas encontrado por el fmin_cg: ", parametros_fmin)

    '''
    print(string)

def rlogPredict():
    string= '''
        def predict(theta, X_train, bool_round):
            m = X_train.shape[0] #cuantas filas tendra la prediccion
            p = np.zeros((m,1))
            if bool_round:
                #redondeo
                p = np.round(sigmoid(np.dot(X_train, theta)))
            else:
                #noredondeo
                p = sigmoid(np.dot(X_train, theta))

            return p

    '''
    print(string)

def rlogY_change():
    string = '''
        #FUNCIONES MULTICLASE
        def y_change(y, cl):
            # Convertimos a numpy si y es un DataFrame
            
            if isinstance(y, pd.DataFrame):
                y = y.to_numpy()
            
            y_new = (y == cl).astype(int)  #vector binario (1 donde y == cl, 0 en otro caso)
            y_new = pd.DataFrame({'label': y_new.flatten()}) #flatten pq numpy array es bidimensional, para devolverlo como una lista normal
            return y_new.to_numpy()


    '''
    print(string)

def rlogTraining():
    string = '''
        #FUNCIONES MULTICLASE
        def training(thetas, X_train, y_train, num_clases):
            X_train = X_train.to_numpy()
            y_train = y_train.to_numpy()
            listaThetas = []
            listaCostes = []
            listaClases = []


            for clase in range(1, num_clases+1):
                y_new = y_change(y_train, clase).flatten()
                fmin_resultados = op.fmin_cg(maxiter=50, f=computeCost, x0=thetas.flatten(), fprime=gradient, args=(X_train, y_new.flatten()), full_output = True)
                listaThetas.append(fmin_resultados[0])
                listaCostes.append(fmin_resultados[1])
                listaClases.append(clase)
                
            res_optimization = pd.DataFrame({"thetas": listaThetas, "costes": listaCostes, "clases": listaClases})
            return res_optimization

    '''
    print(string)


def rlogPredictMulticlass():
    string = '''
        def predict(res_optimization, X_test):
            tam = X_test.shape[0] #iteraremos las filas
            indices_filas = [] # lista de los indices de las filas del dataset
            predicciones = [] # prediccion, valor de y para ese conjunto de datos (fila con indice)

            for fila in range(0, tam): #iteramos filas
                lista_h = [] #almacenar las h (probabilidad) de que esa fila pertenezca a cada clase

                for clase in res_optimization["clases"]: #iteramos clases
                    thetas = res_optimization[res_optimization["clases"]==clase]["thetas"].values[0]
                
                    h= sigmoid(np.dot(X_test.iloc[fila], thetas)) #.iloc porque es un dataframe, si fuera numpy ps pondriamos [] y listo.
                    lista_h.append(h)

                prediccion = np.argmax(lista_h)+1 #devuelve el indice de la h mas alta (+1 para que sea la clase y no cuente el 0)
                predicciones.append(prediccion)
                indices_filas.append(fila)

            return pd.DataFrame({"indices_filas": indices_filas, "predicciones": predicciones})

    '''
    print(string)

def rlogAccuracy():
    string = '''
        def accuracy(y_test, y_predicted):
            return np.mean(y_predicted["predicciones"]==y_test[0])

    '''
    print(string)

def rlogMain():
    string = '''
        # Paso 1:
        num_classes = 10
        # Columna de 1s en la primera posición de X está ya hecho, comprobar
        display(X)

        # si no esta hecho es así:
        ones = np.ones((len(X), 1))
        X.insert(0, "uno", ones)
        #print(X)

        # Paso 2: HOLDOUT 70-30
        X_train, X_test, y_train, y_test = holdout(X, y, 0.7)
        thetas = np.zeros((X_train.shape[1],1))

        # Paso 3: ENTRENAMIENTO
        res_optimization_training = training(thetas, X_train, y_train, num_classes)

        # Paso 4: PREDICCION Y ACCURACY
        res_prediction_training = predict(res_optimization_training, X_test) # PREDICCIÓN DEL TRAINING
        accuracy_training = accuracy(y_test, res_prediction_training) # ACCURACY DE LA PREDICCIÓN DEL TRAINING
        print("Training accuracy: ", accuracy_training)
        #print("Training accuracy sklearn:", metrics.accuracy_score(y_train,res_prediction_training['predicciones']))

    '''
    print(string)


def rlogFull():
    rlogCarga()
    print("\n\n")
    rlogHoldout()
    print("\n\n")
    rlogFmin()
    print("\n\n")
    #BICLASE
    print("\n\n")
    rlogPredict()
    #MULTICLASE
    print("\n\n")
    rlogY_change()
    print("\n\n")
    rlogTraining()
    print("\n\n")
    rlogPredictMulticlass()
    print("\n\n")
    rlogAccuracy()
    print("\n\n")
    rlogMain()
    



