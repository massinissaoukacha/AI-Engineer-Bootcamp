from operator import neg
class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({'amount': amount, 'description': description})
    
    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False
        
        self.deposit(neg(amount), description)
        return True

    def get_balance(self):
        return sum(operation['amount'] for operation in self.ledger)

    def transfer(self, amount, caterory):
        if not self.check_funds(amount):
            return False
        
        self.withdraw(amount, description=f"Transfer to {caterory.name}")
        caterory.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def __str__(self):
        title = '*' * ((30 - len(self.name)) // 2) + self.name + '*' * ((30 - len(self.name)) // 2)
        items = '\n'.join(
            f"{o['description'][:23]:<23}{o['amount']:>7.2f}"
            for o in self.ledger
        )
        total = "Total: " + str(self.get_balance())
        return f"{title}\n{items}\n{total}"
        

def create_spend_chart(categories):
    spent = []

    # Calcul des dépenses de chaque catégorie
    for category in categories:
        amount = sum(
            -item['amount']
            for item in category.ledger
            if item['amount'] < 0
        )
        spent.append(amount)

    # Total de toutes les dépenses
    total_spent = sum(spent)

    # Pourcentages
    percentages = [
        int(amount / total_spent * 100) // 10 * 10
        for amount in spent
    ]

    result = "Percentage spent by category\n"

    # Axe Y + barres
    for level in range(100, -1, -10):
        result += f"{level:>3}|"

        for percentage in percentages:
            if percentage >= level:
                result += " o "
            else:
                result += "   "

        result += "\n"

    # Ligne horizontale
    result += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Noms des catégories verticalement
    max_length = max(len(category.name) for category in categories)

    for i in range(max_length):
        result += "     "

        for category in categories:
            if i < len(category.name):
                result += category.name[i] + "  "
            else:
                result += "   "

        if i < max_length - 1:
            result += "\n"

    return result

food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)