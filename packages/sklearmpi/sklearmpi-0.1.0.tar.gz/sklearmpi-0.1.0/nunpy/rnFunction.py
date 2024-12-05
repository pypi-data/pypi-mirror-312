def rnList():
    string = '''
        rnCarga()
        rnHoldout()
        rnNormalize()
        rnRandInitializeWeights()
        rnForward()
        rnCostFunction()
        rnGradFunction()
        rnTraining()
        rnPredict()
        rnFull()

    '''
    print(string)

def rnCarga():
    string = '''
        CargaOpcion1:
            import pandas as pd
            data = pd.read_csv("drivers_behavior.csv")
            y = pd.DataFrame({'target': data['Target']})
            X = data.drop(['Target'], axis=1)
            # Definición parámetros RED NEURONAL
        
        CargaOpcion2:
            import scipy.io as sio
            data = sio.loadmat("ex4data1.mat") # tipo dict
            X = data['X']
            y = data['y']
            m = X.shape[0]
            # Definición parámetros RED NEURONAL
    '''
    print(string)

def rnHoldout():
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


def rnNormalize():
    string = '''
        def normalize(X):
            mu = X.mean()
            sigma = X.std()
            X_norm = (X-mu)/(sigma)
            
            return X_norm, mu, sigma

        X_train, mu_train, sigma_train = normalize(X_train)
        X_test, mu_test, sigma_test = normalize(X_test)
    
    '''
    print(string)

def rnRandInitializeWeights():
    string = '''
        def randInitializeWeights(capa_entrada, capa_salida):
            epsilon_init = 0.12
            W = np.random.rand(capa_salida, capa_entrada) * 2 * epsilon_init - epsilon_init
            return W
    
    '''

def rnForward():
    string = '''
        def sigmoid(z):
            res = 1/(1+np.exp(-z))
            return res

        def forward(X, theta1, theta2, theta3):
            #variables
            m = len(X)
            ones = np.ones((m, 1))
            
            #activaciones
            a1 = np.hstack((ones, X))
            a2 = sigmoid(np.dot(a1, theta1.T))
            
            a2 = np.hstack((ones, a2))
            a3 = sigmoid(np.dot(a2, theta2.T))
            
            a3 = np.hstack((ones, a3))
            a4 = sigmoid(np.dot(a3, theta3.T))
            
            return a1, a2, a3, a4
    '''
    print(string)

def rnCostFunction():
    string = '''
        def nnCostFunction(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X, y):
            #variables
            m = len(X)
            
            #desenrollar thetas
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size+1)
            theta1 = np.reshape(nn_params[:fin], (hidden_layer_size1, input_layer_size + 1), 'F')
            
            inicio = fin
            fin = fin + hidden_layer_size2 * (hidden_layer_size1+1)
            theta2 = np.reshape(nn_params[inicio:fin], (hidden_layer_size2, hidden_layer_size1 + 1), 'F')
            
            theta3 = np.reshape(nn_params[fin:], (num_labels, hidden_layer_size2+1), 'F')
            
            #calculo activaciones
            a1, a2, a3, h = forward(X, theta1, theta2, theta3)
            
            #getdummies
            y_d = pd.get_dummies(y.flatten())
            
            #calculo coste
            #J = (-1/m) * np.sum(np.sum(np.multiply(y_d,np.log(h)) + np.multiply((1- y_d), np.log(1-h))))
            J = (-1/m)*np.sum(np.dot(y_d.T, np.log(h))+ np.dot((1-y_d).T, np.log(1-h)))

            return J
    '''
    print(string)

def rnGradFunction():
    string= '''
        def nnGradFunction(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X, y):
            #variables
            m = len(X)
            
            #desenrollar thetas
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size+1)
            theta1 = np.reshape(nn_params[inicio:fin], (hidden_layer_size1, input_layer_size + 1), 'F')
            
            inicio = fin
            fin = fin + hidden_layer_size2 * (hidden_layer_size1+1)
            theta2 = np.reshape(nn_params[inicio:fin], (hidden_layer_size2, hidden_layer_size1 + 1), 'F')
            
            theta3 = np.reshape(nn_params[fin:], (num_labels, hidden_layer_size2+1), 'F')
            
            #calculo activaciones
            a1, a2, a3, a4 = forward(X, theta1, theta2, theta3)
            
            #getdummies
            y_d = pd.get_dummies(y.flatten())
            
            #calculo deltas
                #inicializacion
            delta1 = np.zeros(theta1.shape)
            delta2 = np.zeros(theta2.shape)
            delta3 = np.zeros(theta3.shape)
            
                #d's
            d4 = a4 - y_d
            d3 = np.multiply(np.dot(d4, theta3), np.multiply(a3, (1-a3)))
            d2 = np.multiply(np.dot(d3[:,1:], theta2), np.multiply(a2,(1-a2)))
            
            d3 = d3[:,1:]
            d2 = d2[:,1:]
            
                #producto deltas
            delta1 = d2.T @ a1
            delta2 = d3.T @ a2
            delta3 = d4.T @ a3
            
                #normalizacion
            delta1 /= m
            delta2 /= m
            delta3 /= m
            
            delta3 = delta3.to_numpy()
            
            #unroll
            gradiente = np.hstack((delta1.ravel(order='F'), delta2.ravel(order='F'), delta3.ravel(order='F')))
            return gradiente
    '''
    print(string)

def rnTraining():
    string= '''
        theta1 = randInitializeWeights(input_layer_size +1, hidden_layer_size1)
        theta2 = randInitializeWeights(hidden_layer_size1 +1, hidden_layer_size2)
        theta3 = randInitializeWeights(hidden_layer_size2 +1, num_labels)

        nn_initial_params = np.hstack((theta1.ravel(order='F'), theta2.ravel(order='F'), theta3.ravel(order='F')))

        maxiter = 10
        X_train = X_train.to_numpy()
        y_train = y_train.to_numpy()
        print(X_train.shape)
        print(y_train.shape)

        nn_params = opt.fmin_cg(maxiter=maxiter, f=nnCostFunction, x0=nn_initial_params, fprime=nnGradFunction, args=(input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_train, y_train.flatten()))

        # desenrollar thetas -----

        inicio = 0
        fin = hidden_layer_size1 * (input_layer_size+1)
        theta_opt1 = np.reshape(nn_params[inicio:fin], (hidden_layer_size1, input_layer_size + 1), 'F')

        inicio = fin
        fin = fin + hidden_layer_size2 * (hidden_layer_size1+1)
        theta_opt2 = np.reshape(nn_params[inicio:fin], (hidden_layer_size2, hidden_layer_size1 + 1), 'F')

        theta_opt3 = np.reshape(nn_params[fin:], (num_labels, hidden_layer_size2+1), 'F')
    '''
    print(string)

def rnPredict():
    string = '''
        def predict(theta1, theta2, theta3, X):
            a1, a2, a3, h = forward(X, theta1, theta2, theta3)
            pred = np.argmax(h, axis=1) + 1  
            return pred

        y_test = y_test.to_numpy()
        pred = predict(theta_opt1, theta_opt2, theta_opt3, X_test)
        print("Accuracy: ", np.mean(pred== y_test.flatten())*100)
    '''
    print(string)

def rnFull():
    rnCarga()
    print("\n\n")
    rnHoldout()
    print("\n\n")
    rnNormalize()
    print("\n\n")
    rnRandInitializeWeights()
    print("\n\n")
    rnForward()
    print("\n\n")
    rnCostFunction()
    print("\n\n")
    rnGradFunction()
    print("\n\n")
    rnTraining()
    print("\n\n")
    rnPredict()