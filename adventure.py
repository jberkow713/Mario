class Map:
    def __init__(self, quadrant):
        self.quadrant = quadrant
    def find_neighbors(self):
        pass

class Zone:
    def __init__(self, name):
        self.name = name
        self.neighbors = Map.find_neighbors(self.name)
    def __repr__(self):
        return self.name    

class Player:
    def __init__(self, name):
        self.name = name 
        self.zone = Zone('start')


m = Map(4)
z = Zone('Home')
p = Player('link')
print(f"{z.neighbors}\n{p.zone}")

def l_l_tuples(A,R,L):
    import random
    final = []
    for _ in range(A):
        x = []
        for _ in range(R):
            c = []
            for _ in range(L):            
                c.append(random.randint(0,100))
            x.append(tuple(c))
        final.append(x)   
    return final 

def dict_tuples(num, len,amt,sub):
    d = {}
    for i in range(num):
        d[i] = l_l_tuples(len,amt,sub)
    return d 

class list_tuples:
    def __init__(self, num, length,amount,sub):
        self.num = num 
        self.length = length 
        self.amount = amount 
        self.sub = sub
        self.dict = None 
    def create_dict(self):
        self.dict = dict_tuples(self.num,self.length,self.amount, self.sub)

l = list_tuples(5,2,3,4)
l.create_dict()
print(l.dict)


            