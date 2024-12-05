import pandas as pd
from sklearn.metrics import accuracy_score

def testTitanicModel(model, preprocess):
    
    try:
        df = pd.read_csv('https://masc-portal.soe.manchester.ac.uk/website/content/documentation/courses/aero40041_labs_cw/assets/TitanicTest.csv')
    except:
        try:
            df = pd.read_csv('https://raw.githubusercontent.com/AlexSkillen/AlexSkillen.github.io/refs/heads/main/AERO40041/TitanicTest.csv')
        except:
            df = pd.read_csv('./TitanicTest.csv')

    df = preprocess(df)
    
    df = df.dropna( axis=0)
    
    y = df['Survived'].copy() 
    X = df.loc[:, df.columns != 'Survived'].copy()  

    if( len(y) <= 375 ):
        print("Your preprocessing is too agressive. We're not left with enough samples to test against")
        print("You have ", len(y), "samples remaining in the test set, but at least 375 are required")
        return 0.0
    y_hat = model.predict(X)

    # Compute accuracy
    accuracy = accuracy_score(y, y_hat)

    return accuracy
