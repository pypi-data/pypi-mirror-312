import numpy as np


    

def test_forward(forward):
     

    N_Neurons=[1, 30, 1]

    W1 = np.arange(N_Neurons[1] * N_Neurons[0]).reshape(N_Neurons[1], N_Neurons[0])
    W2 = np.arange(N_Neurons[2] * N_Neurons[1]).reshape(N_Neurons[2], N_Neurons[1])
    b1 = np.ones((N_Neurons[1],1))*3.3
    b2 = np.ones((N_Neurons[2],1))+4.4

    n1_t = 2274.0
    a1_t = 29.997282836572317
    n2_t = 440.3999998764675
    a2_t = 440.3999998764675

    tol=1e-9

    try:
        n1, a1, n2, a2 = forward( np.array([[5]]), W1, W2, b1, b2 )

        passed = False
        try:
            if(np.abs(np.sum(n1)-n1_t)<tol and 
               np.abs(np.sum(a1)-a1_t)<tol and 
               np.abs(np.sum(n2)-n2_t)<tol and 
               np.abs(np.sum(a2)-a2_t)<tol ):
                passed = True 
                print("Passed!")
        except:
            pass

        
        if not passed:
            print("This has not passed our test."+ 
                  " This does not necessarily mean it"+ 
                  " is incorrect (for instance if you"+ 
                  " have changed the order of arguments"+ 
                  " or return values it might produce a"+ 
                  " false negative). It is recommended"+ 
                  " you recheck you code or ask for"+ 
                  " assistance if you cannot spot any issues.")

    except Exception as error:
        print("Your forward function does not seem to run. The error is:")
        print(type(error).__name__, "–", error)

def test_cost(cost):
     

    N_Neurons=[1, 30, 1]

    W1 = np.arange(N_Neurons[1] * N_Neurons[0]).reshape(N_Neurons[1], N_Neurons[0])
    W2 = np.arange(N_Neurons[2] * N_Neurons[1]).reshape(N_Neurons[2], N_Neurons[1])
    b1 = np.zeros((N_Neurons[1],1))
    b2 = np.zeros((N_Neurons[2],1))
 
    c_t = 5362091.033332357

    tol=1e-2

    try:
        c = cost( np.array([[5]]), np.array([[5]]), W1, W2, b1, b2 )

        passed = False

        try:
            if(np.abs(c-c_t)<tol ):
                passed = True
                print("Passed!")
        except:
            pass

        if not passed:
            print("This has not passed our test."+
                  " This does not necessarily mean it is"+
                  " incorrect. It is recommended you recheck"+
                  " you code or ask for assistance if you cannot spot any issues.")
    except Exception as error:
        print("Your cost function does not seem to run. The error is:")
        print(type(error).__name__, "–", error)



def test_backward(backward):
    N_Neurons=[1, 30, 1]

    W1 = np.arange(N_Neurons[1] * N_Neurons[0]).reshape(N_Neurons[1], N_Neurons[0])*66.9
    W2 = np.arange(N_Neurons[2] * N_Neurons[1]).reshape(N_Neurons[2], N_Neurons[1])*6.1
    b1 = np.zeros((N_Neurons[1],1))+5.4
    b2 = np.zeros((N_Neurons[2],1))+10.4

    n1 = np.arange(N_Neurons[1]).reshape((N_Neurons[1],1))*10.01
    a1 = np.arange(N_Neurons[1]).reshape((N_Neurons[1],1))*20.02
    n2 = np.arange(N_Neurons[2]).reshape((N_Neurons[2],1))*10.03
    a2 = np.arange(N_Neurons[2]).reshape((N_Neurons[2],1))*20.04

    a_t = 29101.500246481486
    b_t = 8711353.5
    c_t = 162.00004929629756
    d_t = 1010.4

    tol=1e-9

    
    try:
        a, b, c, d = backward( np.array([[5]]), np.array([[5]]), n1, a1, n2, a2, W1, W2, b1, b2, 100. )

        passed = False
        try:

            if(np.abs(np.sum(a)-a_t)<tol and 
               np.abs(np.sum(b)-b_t)<tol and 
               np.abs(np.sum(c)-c_t)<tol and 
               np.abs(np.sum(d)-d_t)<tol ):
                print("Passed!")
                passed = True
        except:
            pass
        
        if not passed:
            print("This has not passed our test."+
                  " This does not necessarily mean it"+
                  " is incorrect (for instance if you have"+
                  " changed the order of arguments the" +
                  " test might produce a false negative)." +
                  " It is recommended you recheck you code" +
                  " or ask for assistance if you cannot spot any issues.")
    except Exception as error:
        print("Your backward function does not seem to run. The error is:")
        print(type(error).__name__, "–", error)

