def rlinList():
    string = '''
        rlinCarga()
        rlinPlotData()
        rlinComputeCost()
        rlinGradFunction()
        rlinPlotCostIter()
        rlinHoldout()
        rlinError()
        rlinFull()
        rlinNormalize()
    '''
    print(string)

def rlinCarga():
    string = '''
        file_name = 'ex1data1.txt'
        print('Loading Data ...', file_name)
        file = pd.read_csv(file_name, names=["poblacion","beneficio"])
        X = pd.DataFrame({'poblacion': file['poblacion']})
        y = pd.DataFrame({'beneficio': file['beneficio']})
    '''
    print(string)

def rlinPlotData():
    string = '''
        def plotData(X, y):
            plt.scatter(X,y, marker = "x", c = "red")
            plt.xlabel("Population of City in 10,000")
            plt.ylabel("Profit in $10,000")
            plt.xticks(np.arange(5, 26, 5), rotation=45) 
            plt.yticks(np.arange(-5, 26, 5), rotation=45)
            plt.xlim(5,25) # Estamos limitando el eje x. Si los datos cambian, probablemente habrá que modificar estos valores
            plt.ylim(-5,25) # Estamos limitando el eje y. Si los datos cambian, probablemente habrá que modificar estos valores
            plt.show()

        print("El tamaño de X es: ", X.shape[0], " filas y ", X.shape[1], " columna(s) ", X.shape)
        print("La longitud del vector y es: ", len(y), y.shape)

        print("Las 5 primeras filas de los datos son: [atributo entrada X1 | clase y]")
        for i in range(0,5):
        print("\t", X['poblacion'][i],  " | ", y['beneficio'][i]) 
        # Recordar: X[:5] selecciona las 5 primeras filas de X.

        plotData(X, y)
    '''
    print(string)

def rlinNormalize():
    string = '''
        def normalize(X):
            mu = X.mean()
            sigma = X.std()
            X_norm = (X-mu)/(sigma)
            
            return X_norm, mu, sigma

        X, mu, sigma = featureNormalize(X)
        display(X.head(10))
        print("MEDIA:", mu, "\nSTD:", sigma)

    '''
    print(string)

def rlinComputeCost():
    string = '''
        def computeCost(X, y, theta):
            m = len(y) # Numero de instancias en el training
            h = np.dot(X, theta) # Hipótesis del modelo de regresión lineal 
            J = np.sum(np.power((h - y),2), axis=0)/(2*m) # Coste
            #J = (1/(2*m))*np.dot((h-y).T,(h-y))
            return J

        ones = np.ones((len(y), 1)) # Crear un array de 1
        X['uno'] = ones # Añadir a X # Es lo mismo que X['uno'] = 1
        X = X[['uno', 'poblacion']]  # Poner 'uno' como primera columna

        num_atributos = X.shape[1] # Si esta operación la hacemos antes de añadir la columna de 1 a X, debemos poner X.shape[1]+1
        theta = np.zeros((num_atributos,1), dtype=np.float64)

        J_base = computeCost(X, y, theta)
        print("\nEl coste inicializando theta a 0 debe ser aproximadamente 32.072734: ", J_base)

        # Si queremos probar con otros valores de theta: 
        J_prueba = computeCost(X, y, [[-1], [2]]) # Lo mismo que: computeCost(X, y, np.array([[-1],[2]]))
        print("\nEl coste probando con theta0=-1 y theta1=2 es: ", J_prueba)
    '''
    print(string)

def rlinGradFunction():
    string = '''
        def gradientDescent(X, y, theta, alpha, iterations):
            m = len(y) # Numero de instancias en el training
            current_iter = [] # Lista vacía para crear el histórico en un dataframe
            current_cost = [] # Lista vacía para crear el histórico en un dataframe

            for iter in range(iterations):
                h = np.dot(X,theta) # Hipótesis
                theta = theta - alpha*(1/m)*(np.dot(X.T,(h-y)))

                # Guardar el coste J de cada iteración
                current_iter.append(iter) # Añadir la iteración a una lista
                current_cost.append(computeCost(X, y, theta)) # Añadir el coste a una lista

            J_history = pd.DataFrame({'iteracion': current_iter, 'coste': current_cost}) # Crear el dataframe histórico iteracion-coste

            return theta, J_history # Último theta encontrado y dataframe histórico J_history
    
        
        iterations = 1500
        alpha = 0.01
        theta_optimo_holdout, J_history_holdout = gradientDescent(X_training, y_training, theta, alpha, iterations)

        print('Theta encontrado con el descenso del gradiente: \n', theta_optimo_holdout)
        print('\nCoste alcanzado en la última iteración : ', J_history_holdout[J_history_holdout['iteracion']==iterations-1]['coste'])
    '''
    print(string)

def rlinPlotCostIter():
    string = '''
        def plotIterationsVsCost(J_history, alpha, iteraciones):
            plt.plot(J_history['iteracion'], J_history['coste'])
            plt.xlabel('Iteraciones')
            plt.ylabel('Coste')
            plt.title('Descenso del gradiente con alpha: '+str(alpha)+' y '+str(iteraciones)+' iteraciones')
            plt.show()

        def plotData_cost(X, y, theta):

            # Grid sobre el que vamos a calcular J
            theta0_vals = np.linspace(-10, 10, 100)
            theta1_vals = np.linspace(-1, 4, 100)

            # Inicializar J_vals a una matriz de ceros
            J_vals = np.zeros((len(theta0_vals), len(theta1_vals)))

            # Rellenar J_vals
            for i in range(1, len(theta0_vals)):
                for j in range(1, len(theta1_vals)):
                    theta_ij = [[theta0_vals[i]], [theta1_vals[j]]]
                    J_vals[i][j] = computeCost(X, y, theta_ij)

            # Debido a la forma en la que las mallas funcionan en el comando contour, 
            # debemos transponer J_vals antes de llamar a dicha función
            J_vals = J_vals.T

            fig1, ax = plt.subplots(1,1)
            contour = ax.contour(theta0_vals, theta1_vals, J_vals, np.logspace(-2, 3, 20))
            fig1.colorbar(contour)
            plt.xlabel("theta_0")
            plt.ylabel("theta_1")
            plt.plot(theta[0], theta[1], marker = 'x', c='red')
            plt.show()

        def plotData_linearRegression(X, y, theta):
            plt.scatter(X['poblacion'],y, marker="x", c="red", label="Training data") # Representación del conjunto de datos
            plt.plot(X['poblacion'], np.dot(X, theta), c='blue', label="Linear regression") # Representación de la recta: h = X·theta
            plt.xlabel("Population of City in 10,000")
            plt.ylabel("Profit in $10,000")
            plt.xlim(5, 25) # Cuidado: estamos limitando el eje X 
            plt.ylim(-5, 25) # Cuidado: estamos limitando el eje y
            plt.legend()
            plt.show()
    '''
    print(string)

def rlinHoldout():
    string = '''
        def holdout(X, y, percentage=0.6):
            X_training = X.sample(round(percentage*len(X))) # Selecciona aleatoriamente el numero de filas indicado
            y_training = y.iloc[X_training.index] # Selecciona las filas del X_training
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

            # OPCION 3
        def holdout(X, y, percentage=0.6):
            X_training, X_test, y_training, y_test = train_test_split(X,y, test_size=1-percentage, random_state=1) # Cuidado con el orden de la salida
            # random_state: controla el barajado aplicado a los datos antes de aplicar la división. Si le pasamos un int, la salida se reproducirá siempre que llamemos a la función
            
            print("El tamaño del training debe ser: ", round(percentage*len(X)), " - Comprobación: tamaño X_training es ", len(X_training), " y tamaño y_training es", len(y_training))
            print("El tamaño del test debe ser: ", len(X)-round(percentage*len(X)), " - Comprobación: tamaño X_test es ", len(X_test), " y tamaño y_test es", len(y_test))
            
            # Reseteamos los índices de todos los conjuntos
            X_training = X_training.reset_index(drop=True)
            y_training = y_training.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)
            y_test = y_test.reset_index(drop=True)

            return X_training, y_training, X_test, y_test

        X_training, y_training, X_test, y_test = holdout(X, y, 0.7)
    '''
    print(string)

def rlinError():
    string = '''
        y_predicted = np.dot(X_test, theta_optimo_holdout)

        m = len(y_test)

        # MAE: 
        error_absoluto_medio_holdout = (1/m) * np.sum((np.abs(y_test-y_predicted)), axis=0)
        print("El error absoluto medio es: ", error_absoluto_medio_holdout)
        MAE_sklearn_holdout = metrics.mean_absolute_error(y_test, y_predicted)
        print("El error absoluto medio usando sklearn es: ", MAE_sklearn_holdout)

        # MSE: 
        error_cuadratico_medio_holdout = (1/m) * np.sum(np.power((y_test-y_predicted),2), axis=0)
        print("\n\nEl error cuadrático medio es: ", error_cuadratico_medio_holdout)
        MSE_sklearn_holdout = metrics.mean_squared_error(y_test, y_predicted)
        print("El error cuadrático medio usando sklearn es: ", MSE_sklearn_holdout)
    '''
    print(string)

def rlinFull():
    rlinCarga()
    print("\n\n")
    rlinPlotData()
    print("\n\n")
    rlinComputeCost()
    print("\n\n")
    rlinGradFunction()
    print("\n\n")
    rlinPlotCostIter()
    print("\n\n")
    rlinHoldout()
    print("\n\n")
    rlinError()
    print("\n\n")
    rlinNormalize()