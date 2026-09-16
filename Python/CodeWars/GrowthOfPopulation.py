"""
import sympy as sp
import math

def nb_year(p0, percent, aug, p):
    rate = 1 + percent / 100
    P = p
    def recurrenceGeneralTerm(p0, rate, aug, P):
        #variables
        n = sp.symbols('n', real=True, nonnegative=True)

        # suite y(n)
        p = sp.Function('p')

        #Relation de récurrence
        recurrence = sp.Eq(p(n+1), rate * p(n) + aug)

        #Résolution
        p_n = sp.rsolve(recurrence, p(n), {p(0):p0})

        #عبارة الحد العام
        expression = sp.Eq(p_n, P)
        return expression

    def solveRecurrence(p0, rate, aug, P):

        #Variables
        n = sp.symbols('n', real=True, nonnegative=True)

        #Trouver n
        solution = sp.solve(recurrenceGeneralTerm(p0, rate, aug, P), n)

        return math.ceil(solution[0])

    return solveRecurrence(p0, rate, aug, P)
"""

import math

def nb_year(p0, percent, aug, p):
    percent /= 100
    rate = 1 + percent
    if rate != 1 :
        return math.ceil(math.log((aug + p * percent) / (aug + p0 * percent)) / math.log(rate))
    else :
        if aug != 0 : return math.ceil((p - p0) / aug)
        else : return 'infini'

print(nb_year(1000, 0, 67, 1200))