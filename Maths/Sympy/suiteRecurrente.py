import sympy as sp
import math

def recurrenceGeneralTerm(a, r, u0, U):
    #variables
    n = sp.symbols('n', real=True, nonnegative=True)

    # suite y(n)
    u = sp.Function('u')

    #Relation de récurrence
    recurrence = sp.Eq(u(n+1), a*u(n)+r)

    #Résolution
    u_n = sp.rsolve(recurrence, u(n), {u(0):u0})

    #عبارة الحد العام
    expression = sp.Eq(u_n, U)
    return expression

def solveRecurrence(a, r, u0, U):

    #Variables
    n = sp.symbols('n', real=True, nonnegative=True)

    #Trouver n
    solution = sp.solve(recurrenceGeneralTerm(a, r, u0, U), n)

    return math.ceil(solution[0])
