class HashTable:
    def __init__(self):
        self.collection = {} # {valeur_clé_hachée, {cle: valeur}}
    
    def hash(self, string):
        valeur_hachage_calculee = sum(ord(char) for char in string)
        return valeur_hachage_calculee

    def add(self, cle, valeur):
        hachage_cle = self.hash(cle)
        if hachage_cle in self.collection :
            self.collection[hachage_cle][cle] = valeur
        else :
            self.collection[hachage_cle] = {cle : valeur}
        
    def remove(self, cle):
        hachage_cle = self.hash(cle)
        if hachage_cle in self.collection :
            if cle in self.collection[hachage_cle]:
                if len(self.collection[hachage_cle]) > 1:
                    del self.collection[hachage_cle][cle]
                else :
                    del self.collection[hachage_cle]
            else :
                pass
        else :
            pass
   
    def lookup(self, cle):
        hachage_cle = self.hash(cle)

        if hachage_cle not in self.collection :
            return None

        if cle not in self.collection[hachage_cle]:
            return None

        return self.collection[hachage_cle][cle]       
if __name__ == '__main__':
    ht = HashTable()
    ht.add('hello', 'valeur1')
    ht.add('hello2', 'valeur2')
    ht.collection[582]['hello3'] = 'valeur3'
    print(ht.collection)
    ht.remove('hello')
    print(ht.collection)
    print(ht.lookup('hello'))