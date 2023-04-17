import pyomo.environ as pyo
import numpy as np
from creator import create_param_1, create_param_2, read_data
np.random.seed(123)
import pandas as pd
from features import crear_reporte, productor, acopio

import sys

# def read_data():
#     CTQ1_path = 'Prod-CAQ.csv'
#     aux = pd.read_csv(CTQ1_path, index_col=0)
#     CTQ1 = {}
#     for i in aux.keys():
#         for j in aux.columns:
#             CTQ1[i, j, 0] = aux[j][i]

#     return CTQ1

def modelo_2(dep):
    model = pyo.ConcreteModel(name="Queso_1")

    actors, CTL1, CTQ1, CTQ2, A, B, CAL, CapPL, D, CapPQ, CPQ, CI, COA, CapAQ, CAA, natt_cost = read_data(dep)

    #Conjuntos
    model.I = pyo.Set(initialize=actors['prov']) # Productores de leche
    # model.J = pyo.Set(initialize=range(2))
    model.K = pyo.Set(initialize=actors['prod']) # Productores de queso
    model.R = pyo.Set(initialize=actors['prod']) #Centros de acopio
    model.M = pyo.Set(initialize=actors['com']) # Centros de consumo
    model.L = pyo.Set(initialize=range(1)) # Tipos de leche
    model.Q = pyo.Set(initialize=range(1)) # Tipos de queso
    


    #CapAQ, CAA = create_param_2(model)



    #Parametros
    model.CTL1 = pyo.Param(model.I, model.K, model.L, initialize=CTL1) #Costo de transporte de leche a productor
    # model.CTL2 = pyo.Param(model.J, model.K, model.L, initialize=CTL2) 
    model.CTQ1 = pyo.Param(model.K, model.R, model.Q, initialize=CTQ1) #Costo de transporte de queso a acopio
    model.CTQ2 = pyo.Param(model.R, model.M, model.Q, initialize=CTQ2) #Costo de transporte de queso a centro consumo
    # model.COT = pyo.Param(model.J, model.L, initialize=COT) #Costo de operacion del tanque
    model.CPQ = pyo.Param(model.K, model.Q, initialize=CPQ) #Costo de produccion de queso
    model.CI = pyo.Param(model.R, model.Q, initialize=CI) #Costo de inventario de queso
    model.COA = pyo.Param(model.R, model.Q, initialize=COA) #Costo de operacion de centro de acopio queso
    model.CAL = pyo.Param(model.I, model.L, initialize=CAL) #Costo de adquisicion de leche
    model.B = pyo.Param(model.M, model.Q, initialize=B) #Precio de venta de queso
    model.CapPL = pyo.Param(model.I, model.L, initialize=CapPL) #Capacidad maxima de produccion de leche
    model.CAA = pyo.Param(model.R, initialize=CAA) # Costo de apertura del centro de acopio de queso
    model.CapPQ = pyo.Param(model.K, model.Q, initialize=CapPQ) #Capacidad maxima de produccion de queso
    model.CapAQ = pyo.Param(model.R, initialize=CapAQ) #Capacidad maxima de almacenamiento de queso
    model.D = pyo.Param(model.M, model.Q, initialize=D) #Demanda de queso
    model.A = pyo.Param(model.L, model.Q, initialize=A) #Rendimiento de leche a queso
    model.natt_cost = pyo.Param(initialize=natt_cost)
    #model.MX = pyo.Param(initialize=1000000000)


    #Variables

    model.x1 = pyo.Var(model.I, model.K, model.L, within=pyo.NonNegativeReals, initialize=0) #Leche desde fincas a productores
    # model.x2 = pyo.Var(model.J, model.K, model.L, within=pyo.NonNegativeReals)
    model.x3 = pyo.Var(model.K, model.R, model.Q, within=pyo.NonNegativeReals) #Queso desde productores
    model.x4 = pyo.Var(model.R, model.M, model.Q, within=pyo.NonNegativeReals) #Queso desde centros de acopio
    model.y = pyo.Var(model.R, within=pyo.Binary) #Se abre o no el centro de acopio
    model.natt = pyo.Var(model.M, model.Q, within=pyo.NonNegativeReals)

    def _inv(model, r):
        return sum(sum(model.x3[k, r, q] for q in model.Q) for k in model.K) - sum(sum(model.x4[r, m, q] for q in model.Q) for m in model.M)
    model.inv = pyo.Expression(model.R, rule=_inv)

    #Funcion Objetivo

    def obj_rule(model):
        obj = sum(sum(sum(model.B[m, q]*model.x4[r,m,q] for q in model.Q) for m in model.M) for r in model.R) #Ingreso de ventas
        obj -= sum(sum(sum(model.CAL[i,l]*model.x1[i,k,l] for l in model.L) for k in model.K) for i in model.I) #Costo de adquision leche
        obj -= sum(sum(sum(model.CTL1[i,k,l]*model.x1[i,k,l] for l in model.L) for k in model.K) for i in model.I) #Costo de transporte de leche a prod.
        obj -= sum(model.CAA[r]*model.y[r] for r in model.R) #Costo de apertura de centro de acopio
        obj -= sum(sum(sum(model.CTQ1[k, r, q]*model.x3[k, r, q] for q in model.Q) for r in model.R) for k in model.K) #Costo de transporte de queso a acopio
        obj -= sum(sum(sum(model.CTQ2[r, m, q]*model.x4[r, m, q] for q in model.Q) for m in model.M) for r in model.R) #Costo de transporte de queso a cent. consumo
        obj -= sum(sum(model.natt[m,q] for q in model.Q) for m in model.M) * model.natt_cost #Costo de demanda no atendida
        obj -= sum(sum(sum(model.CPQ[k, q]*model.x3[k, r, q] for q in model.Q) for k in model.K) for r in model.R) #Costo de produccion de queso
        obj -= sum(sum(sum(model.COA[r, q]*model.x4[r, m, q] for q in model.Q) for m in model.M) for r in model.R) #Costo de operacion de los acopios de de queso
        obj -= sum(sum(model.CI[r, q] * (sum(model.x3[k, r, q] for k in model.K) - sum(model.x4[r, m, q] for m in model.M))  for q in model.Q) for r in model.R) #Costo de inventario de los acopios de de queso

        return obj

    model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

    #Restricciones

    def r1_rule(model, i, l):
        # Capacidad de producción de leche en las fincas
        return sum(model.x1[i, k, l] for k in model.K) <= model.CapPL[i,l]

    model.r1 = pyo.Constraint(model.I, model.L, rule=r1_rule, name='Mx_cap_PL')

    # def r2_rule(model, j, l):
    #     return sum(model.x1[i, j, l] for i in model.I) <= model.CapAL[j,l]

    # model.r2 = pyo.Constraint(model.J, model.L, rule=r2_rule)

    def r3_rule(model, k, q):
        # Capacidad de producción de queso
        return sum(model.x3[k, r, q] for r in model.R) <= model.CapPQ[k,q]

    model.r3 = pyo.Constraint(model.K, model.Q, rule=r3_rule, name='Mx_cap_PQ')

    def r4_rule(model, r):
        # Capacidad de almacenamiento de los almacenes de queso
        #expr = sum(sum(model.x3[k, r, q] for q in model.Q) for k in model.K) - sum(sum(model.x4[r, m, q] for q in model.Q) for m in model.M) - model.y[r] * model.CapAQ[r]
        return sum(sum(model.x3[k, r, q] for q in model.Q) for k in model.K)  <= model.CapAQ[r] * model.y[r]
        #return (0, expr, 0)

    model.r4 = pyo.Constraint(model.R, rule=r4_rule, name='Mx_Cap_AQ')

    def r4_2_rule(model, r):
        return sum(sum(model.x4[r, m, q] for q in model.Q) for m in model.M) <= sum(sum(model.x3[k, r, q] for q in model.Q) for k in model.K)
    model.r4_2 = pyo.Constraint(model.R, rule=r4_2_rule, name='Mx_salida_Q')

    def r5_rule(model, m, q):
        # Respuesta a la demanda
        return sum(model.x4[r, m, q] for r in model.R) == model.D[m, q] - model.natt[m, q]

    model.r5 = pyo.Constraint(model.M, model.Q, rule=r5_rule)

    def r6_rule(model, k, l, q):
        # Equivalencia de producción de leche a queso
        return sum(model.x3[k, r, q] for r in model.R) == model.A[l, q] * sum(model.x1[i, k, l] for i in model.I)

    model.r6 = pyo.Constraint(model.K, model.L, model.Q, rule=r6_rule)


    # def r7_rule(model, j, l):
    #     return sum(model.x1[i, j, l] for i in model.I) == sum(model.x2[j, k, l] for k in model.K)

    # model.r7 = pyo.Constraint(model.J, model.L, rule=r7_rule)

    def r8_rule(model, r, q):
        return sum(model.x3[k, r, q] for k in model.K) == sum(model.x4[r, m, q] for m in model.M)

    model.r8 = pyo.Constraint(model.R, model.Q, rule=r8_rule)

    def r9_rule(model, r):

        return sum(sum(model.x3[k, r, q] for q in model.Q) for k in model.K) * (1 - model.y[r]) <= 0 

    model.r9 = pyo.Constraint(model.R, rule=r9_rule)
    
    return model

    

def modelo_1():
    model = pyo.ConcreteModel(name="Queso_v2")

    #Conjuntos
    model.I = pyo.Set(initialize=range(3))
    model.J = pyo.Set(initialize=range(2))
    model.K = pyo.Set(initialize=range(4))
    model.R = pyo.Set(initialize=range(2))
    model.M = pyo.Set(initialize=range(3))
    model.L = pyo.Set(initialize=range(1))
    model.Q = pyo.Set(initialize=range(3))


    CTL1, CTL2, CTQ1, CTQ2, COT, CPQ, CI, COA, CAL, B, CapPL, CapAL, CapPQ, CapAQ, D, A = create_param_1(model)



    #Parametros
    model.CTL1 = pyo.Param(model.I, model.J, model.L, initialize=CTL1) #Costo de transporte de leche a acopio
    model.CTL2 = pyo.Param(model.J, model.K, model.L, initialize=CTL2) #Costo de transporte de leche a productor
    model.CTQ1 = pyo.Param(model.K, model.R, model.Q, initialize=CTQ1) #Costo de transporte de queso a acopio
    model.CTQ2 = pyo.Param(model.R, model.M, model.Q, initialize=CTQ2) #Costo de transporte de queso a centro consumo
    model.COT = pyo.Param(model.J, model.L, initialize=COT) #Costo de operacion del tanque
    model.CPQ = pyo.Param(model.K, model.Q, initialize=CPQ) #Costo de produccion de queso
    model.CI = pyo.Param(model.R, model.Q, initialize=CI) #Costo de inventario de queso
    model.COA = pyo.Param(model.R, model.Q, initialize=COA) #Costo de operacion de centro de acopio queso
    model.CAL = pyo.Param(model.I, model.L, initialize=CAL) #Costo de adquisicion de leche
    model.B = pyo.Param(model.M, model.Q, initialize=B) #Precio de venta de queso
    model.CapPL = pyo.Param(model.I, model.L, initialize=CapPL) #Capacidad maxima de produccion de leche
    model.CapAL = pyo.Param(model.J, model.L, initialize=CapAL) #Capacidad maxima de almacenamiento de leche
    model.CapPQ = pyo.Param(model.K, model.Q, initialize=CapPQ) #Capacidad maxima de produccion de queso
    model.CapAQ = pyo.Param(model.R, initialize=CapAQ) #Capacidad maxima de almacenamiento de queso
    model.D = pyo.Param(model.M, model.Q, initialize=D) #Demanda de queso
    model.A = pyo.Param(model.L, model.Q, initialize=A) #Rendimiento de leche a queso


    #Variables

    model.x1 = pyo.Var(model.I, model.J, model.L, within=pyo.NonNegativeReals, initialize=0) #Leche desde fincas
    model.x2 = pyo.Var(model.J, model.K, model.L, within=pyo.NonNegativeReals) #Leche desde tanques
    model.x3 = pyo.Var(model.K, model.R, model.Q, within=pyo.NonNegativeReals) #Queso desde productores
    model.x4 = pyo.Var(model.R, model.M, model.Q, within=pyo.NonNegativeReals) #Queso desde centros de acopio

    #Funcion Objetivo

    def obj_rule(model):
        obj = sum(sum(sum(model.B[m, q]*model.x4[r,m,q] for q in model.Q) for m in model.M) for r in model.R) #Ingreso de ventas
        obj -= sum(sum(sum(model.CAL[i,l]*model.x1[i,j,l] for l in model.L) for j in model.J) for i in model.I) #Costo de adquision queso
        obj -= sum(sum(sum(model.CTL1[i,j,l]*model.x1[i,j,l] for l in model.L) for j in model.J) for i in model.I) #Costo de transporte de leche a tanques
        obj -= sum(sum(sum(model.CTL2[j,k,l]*model.x2[j, k, l] for l in model.L) for k in model.K) for j in model.J) #Costo de transporte de leche a prod
        obj -= sum(sum(sum(model.CTQ1[k, r, q]*model.x3[k, r, q] for q in model.Q) for r in model.R) for k in model.K) #Costo de transporte de queso a acopio
        obj -= sum(sum(sum(model.CTQ2[r, m, q]*model.x4[r, m, q] for q in model.Q) for m in model.M) for r in model.R) #Costo de transporte de queso a cent. consumo
        obj -= sum(sum(sum(model.COT[j, l]*model.x1[i, j, l] for i in model.I) for j in model.J) for l in model.L) #Costo de operacion de los tanque
        obj -= sum(sum(sum(model.CPQ[k, q]*model.x3[k, r, q] for q in model.Q) for k in model.K) for r in model.R) #Costo de produccion de queso
        obj -= sum(sum(sum(model.COA[r, q]*model.x4[r, m, q] for q in model.Q) for m in model.M) for r in model.R) #Costo de operacion de los acopios de de queso
        obj -= sum(sum(model.CI[r, q] * (sum(model.x3[k, r, q] for k in model.K) - sum(model.x4[r, m, q] for m in model.M))  for q in model.Q) for r in model.R) #Costo de operacion de los acopios de de queso

        return obj

    model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

    #Restricciones

    def r1_rule(model, i, l):
        return sum(model.x1[i, j, l] for j in model.J) <= model.CapPL[i,l]

    model.r1 = pyo.Constraint(model.I, model.L, rule=r1_rule)

    def r2_rule(model, j, l):
        return sum(model.x1[i, j, l] for i in model.I) <= model.CapAL[j,l]

    model.r2 = pyo.Constraint(model.J, model.L, rule=r2_rule)

    def r3_rule(model, k, q):
        return sum(model.x3[k, r, q] for r in model.R) <= model.CapPQ[k,q]

    model.r3 = pyo.Constraint(model.K, model.Q, rule=r3_rule)

    def r4_rule(model, r):
        return sum(sum(model.x3[k, r, q] for q in model.Q) for k in model.K) - sum(sum(model.x4[r, m, q] for q in model.Q) for m in model.M) <= model.CapAQ[r]

    model.r4 = pyo.Constraint(model.R, rule=r4_rule)

    def r5_rule(model, m, q):
        return sum(model.x4[r, m, q] for r in model.R) == model.D[m, q]

    model.r5 = pyo.Constraint(model.M, model.Q, rule=r5_rule)

    def r6_rule(model, l, q):
        return model.A[l, q] * sum(sum(model.x2[j, k, l] for k in model.K) for j in model.J) == sum(sum(model.x3[k, r, q] for k in model.K) for r in model.R)

    model.r6 = pyo.Constraint(model.L, model.Q, rule=r6_rule)


    def r7_rule(model, j, l):
        return sum(model.x1[i, j, l] for i in model.I) == sum(model.x2[j, k, l] for k in model.K)

    model.r7 = pyo.Constraint(model.J, model.L, rule=r7_rule)

    def r8_rule(model, r, q):
        return sum(model.x3[k, r, q] for k in model.K) == sum(model.x4[r, m, q] for m in model.M)

    model.r8 = pyo.Constraint(model.R, model.Q, rule=r8_rule)

    #solver = pyo.SolverFactory('gurobi')

    model.pprint()
    sys.exit()


    #results = solver.solve(model)

    print('Funcion objetivo: {}'.format(pyo.value(model.obj)))






if __name__ == "__main__":

    prov = '../Prov-Prod.csv' #Este es el path del proveedor
    prod = '../.csv'
    
    model = modelo_2('cordoba')

    solver = pyo.SolverFactory('gurobi')


    results = solver.solve(model)

    print('Capacidad de almacenamiento queso {}'.format(pyo.value(sum(model.CapAQ[r] for r in model.R))))

    print('Total x3 ')
    print(pyo.value(sum(sum(sum(model.x3[k, r, q] for k in model.K) for r in model.R) for q in model.Q)))
    print('Total x4 ')
    print(pyo.value(sum(sum(sum(model.x4[r, m, q] for m in model.M) for r in model.R) for q in model.Q)))
    print('Funcion objetivo: {}'.format(pyo.value(model.obj)))

    print(' ')
    for m in model.M:
        print('Se atendieron {} de {}'.format(pyo.value(sum(model.x4[r, m, 0] for r in model.R)), pyo.value(model.D[m, 0])))

    print('Capacidad de prod. queso {}'.format(pyo.value(sum(model.CapPQ[k, 0] for k in model.K))))

    # # a =  read_data()
    crear_reporte(model, 'CORDOBA')
    #acopio(2, model, 'Cordoba')


