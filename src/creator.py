import numpy as np
#np.random.seed(1)
import pandas as pd
import json
import sys
def create_param_1(model):

    CTL1 = {}
    CTL2 = {}
    CTQ1 = {}
    CTQ2 = {}
    COT = {}
    CPQ = {}
    CI = {}
    COA = {}
    CAL = {}
    B = {}
    CapPL = {}
    CapAL = {}
    CapPQ = {}
    CapAQ = {}
    D = {}
    A = {}
    for i in model.I:
        for j in model.J:
            for l in model.L:
                CTL1[i,j,l] = np.random.normal(100, 15)
    
    for j in model.J:
        for k in model.K:
            for l in model.L:
                CTL2[j,k,l] = np.random.normal(100, 15)
    
    for k in model.K:
        for r in model.R:
            for q in model.Q:
                CTQ1[k,r,q] = np.random.normal(150, 20)
    
    for r in model.R:
        for m in model.M:
            for q in model.Q:
                CTQ2[r,m,q] = np.random.normal(150, 20)
    
    for j in model.J:
        for l in model.L:
            COT[j,l] = np.random.normal(70, 10)

    for k in model.K:
        for q in model.Q:
            CPQ[k,q] = np.random.normal(1000, 200)
    
    for r in model.R:
        for q in model.Q:
            CI[r,q] = np.random.normal(75, 15)
    
    for r in model.R:
        for q in model.Q:
            COA[r,q] = np.random.normal(60, 15)
    
    for i in model.I:
        for l in model.L:
            CAL[i,l] = np.random.normal(30, 10)

    for m in model.M:
        for q in model.Q:
            B[m,q] = np.random.normal(16000, 1000)
    
    for i in model.I:
        for l in model.L:
            CapPL[i,l] = np.random.normal(200, 20)

    for j in model.J:
        for l in model.L:
            CapAL[j,l] = np.random.normal(500, 20)
    
    for k in model.K:
        for q in model.Q:
            CapPQ[k,q] = np.random.normal(40, 10)
    
    for r in model.R:
        CapAQ[r] = np.random.normal(50, 20)
    
    for m in model.M:
        for q in model.Q:
            D[m,q] = np.random.normal(40, 15)
    
    for l in model.L:
        for q in model.Q:
            A[l,q] = np.random.normal(0.1, 0.03)

    return CTL1, CTL2, CTQ1, CTQ2, COT, CPQ, CI, COA, CAL, B, CapPL, CapAL, CapPQ, CapAQ, D, A


def read_data(dep:str, data=None):
    """
    Arg:
    dep (str) nombre del departamento a experimentar. "cordoba", "magdalena", "guajira"
    data (str) nombre del archivo de datos para el departamento en cuestion
    """

    if not data:
        data_filepath = '../data/{}/data.json'.format(dep)
    else:
        data_filepath = '../data/{}/{}.json'.format(dep, data)
    
    with open(data_filepath) as data:
        data = json.load(data)
    
    prov_path = '../data/{}/prov.csv'.format(dep)
    prod_path = '../data/{}/prod.csv'.format(dep)
    com_path = '../data/{}/com.csv'.format(dep)
    b_path = '../data/{}/B.csv'.format(dep)
    CAL_path = '../data/{}/CAL.csv'.format(dep)
    CapPL_path = '../data/{}/CapPL.csv'.format(dep)
    D_path = '../data/{}/D.csv'.format(dep)
    CapPQ_path = '../data/{}/CapPQ.csv'.format(dep)
    CPQ_path = '../data/{}/CPQ.csv'.format(dep)


    A = {}
    A[0,0] = np.random.normal(data['A']['mean'], data['A']['std'])

    aux_prov = pd.read_csv(prov_path, index_col=0, sep=';')
    CTL1 = {}
    for i in aux_prov.index:
        for j in aux_prov.columns:
            CTL1[i, j, 0] = aux_prov[j][i] * data['cu_tl']
    
    aux_prod = pd.read_csv(prod_path, index_col=0, sep=';')
    CTQ1 = {}
    for i in aux_prod.index:
        for j in aux_prod.columns:
            CTQ1[i, j, 0] = aux_prod[j][i] * data['cu_tq1']
    
    aux_com = pd.read_csv(com_path, index_col=0, sep=';')
    CTQ2 = {}
    for i in aux_com.index:
        for j in aux_com.columns:
            CTQ2[i, j, 0] = aux_com[j][i] * data['cu_tq2']

    aux_b = pd.read_csv(b_path, index_col=0, sep=';', header=None)
    B = {}
    for i in aux_b.index:
        B[i, 0] = aux_b[1][i] * 5.5 # AUMENTADO

    aux_CAL = pd.read_csv(CAL_path, index_col=0, sep=';', header=None)
    CAL = {}
    for i in aux_CAL.index:
        CAL[i, 0] = aux_CAL[1][i]
    
    aux_CapPL = pd.read_csv(CapPL_path, index_col=0, sep=';', header=None)
    CapPL = {}
    for i in aux_CapPL.index:
        CapPL[i, 0] = aux_CapPL[1][i] * 10 # AUMENTADO
    
    aux_D = pd.read_csv(D_path, index_col=0, sep=';', header=None)
    D = {}
    for i in aux_D.index:
        D[i, 0] = aux_D[1][i]
    
    aux_CapPQ = pd.read_csv(CapPQ_path, index_col=0, sep=';', header=None)
    CapPQ = {}
    for i in aux_CapPQ.index:
        CapPQ[i, 0] = aux_CapPQ[1][i]

    aux_CPQ = pd.read_csv(CPQ_path, index_col=0, sep=';', header=None)
    CPQ = {}
    for i in aux_CPQ.index:
        CPQ[i, 0] = aux_CPQ[1][i] * 0.5 # DISMINUIDO
    
    CI = {}
    for i in aux_prod.index:
        CI[i, 0] = np.random.normal(data['cu_inv']['mean'], data['cu_inv']['std'])

    COA = {}
    for i in aux_prod.index:
        COA[i, 0] = np.random.normal(data['COA']['mean'], data['COA']['std'])

    CapAQ = {}
    for i in aux_prod.index:
        CapAQ[i] = np.random.normal(data['CapAQ']['mean'], data['CapAQ']['std'])
    
    CAA = {}
    for i in aux_prod.index:
        CAA[i] = np.random.normal(data['CAA']['mean'], data['CAA']['std'])
    

    
    
    
    actors = {'prov': [i for i in aux_prov.index], 
              'prod': [i for i in aux_prod.index], 
              'com': [i for i in aux_com.columns]}
    
    
    return actors, CTL1, CTQ1, CTQ2, A, B, CAL, CapPL, D, CapPQ, CPQ, CI, COA, CapAQ, CAA, data['natt_cost']

def create_param_2(model):

    CTL1 = {}
    # CTL2 = {}
    CTQ1 = {}
    CTQ2 = {}
    # COT = {}
    CPQ = {}
    CI = {}
    COA = {}
    CAL = {}
    B = {}
    CapPL = {}
    CAA = {}
    CapPQ = {}
    CapAQ = {}
    D = {}
    A = {}
    for i in model.I:
        for k in model.K:
            for l in model.L:
                CTL1[i,k,l] = np.random.normal(50, 15)
    
    # for j in model.J:
    #     for k in model.K:
    #         for l in model.L:
    #             CTL2[j,k,l] = np.random.normal(100, 15)
    
    for k in model.K:
        for r in model.R:
            for q in model.Q:
                CTQ1[k,r,q] = np.random.normal(150, 20)
    
    for r in model.R:
        for m in model.M:
            for q in model.Q:
                CTQ2[r,m,q] = np.random.normal(150, 20)
    
    # for j in model.J:
    #     for l in model.L:
    #         COT[j,l] = np.random.normal(70, 10)

    # for k in model.K:
    #     for q in model.Q:
    #         CPQ[k,q] = np.random.normal(1000, 200)
    
    # for r in model.R:
    #     for q in model.Q:
    #         CI[r,q] = np.random.normal(75, 15)
    
    for r in model.R:
        for q in model.Q:
            COA[r,q] = np.random.normal(60, 15)
    
    # for i in model.I:
    #     for l in model.L:
    #         CAL[i,l] = np.random.normal(30, 10)

    # for m in model.M:
    #     for q in model.Q:
    #         B[m,q] = np.random.normal(50000, 3000)
    
    # for i in model.I:
    #     for l in model.L:
    #         CapPL[i,l] = np.random.normal(800, 100)

    for r in model.R:
        CAA[r] = np.random.normal(100, 20)
    
    # for k in model.K:
    #     for q in model.Q:
    #         CapPQ[k,q] = np.random.normal(800, 5)
    
    for r in model.R:
        CapAQ[r] = np.random.normal(700, 20)
    
    # for m in model.M:
    #     for q in model.Q:
    #         D[m,q] = np.random.normal(400, 15)
    
    # for l in model.L:
    #     for q in model.Q:
    #         A[l,q] = np.random.normal(1/7, 0.03)

    return CapAQ, CAA


if __name__ == "__main__":
    actors, a, b, c = read_data('cordoba')