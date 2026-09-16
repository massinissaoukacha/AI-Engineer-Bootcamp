
from collections import Counter

def mostActive(customers):
    n = len(customers)
    c = Counter(customers)
    customersList = []
    for i in c :
        c[i] = c[i] / n * 100
        if c[i] >= 5 :
            customersList.append(i)
    
    return sorted(customersList)


customers = ['Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Alpha', 'Omega', 'Beta', 'Alpha', 'Alpha', 'Alpha']
print(len(customers))
result = mostActive(customers)
print(result)
