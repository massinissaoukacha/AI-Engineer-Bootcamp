"""
1*** Vous devriez créer une fonction nommée fibonacci.

2*** Vous devez définir une liste nommée sequence dans le fibonacci fonction,
et il doit être initialisé avec les valeurs [0, 1].

3*** La fonction fibonacci doit accepter un paramètre, un entier non négatif n.

4*** Appeler fibonacci(n) devrait utiliser une approche de programmation dynamique
pour calculer et retourner le n-ème nombre de la séquence de Fibonacci,
où chaque nombre est la somme des deux nombres précédents.

5*** Chaque numéro Fibonacci calculé doit être ajouté au sequenceliste."""

def fibonacci(n):
    if n < 0:
        return
    sequence = [0, 1]
    for i in range(2, n + 1):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence[n]

print(fibonacci(15))