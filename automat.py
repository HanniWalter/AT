"\u03B5"

class Node:
    def __init__(self, description):
        self.description = description

class Automata:
    def __init__(self) -> None:
        self.Q = []
        self.T = []
        self.I = []
        self.F = []

    def addQ(self,node):
        assert node.description not in [d.description for d in self.Q]
        self.Q.append(node)

    def addT(self,t):
        assert len(t) == 3 
        assert t[0] in self.Q   
        assert t[1] in self.Q   
        self.T.append(t)

    def addT(self,q,a,r):
        assert q in self.Q   
        assert r in self.Q  
        assert a != "" 
        self.T.append((q,a,r))

    def addI(self,node):
        assert node in self.Q
        self.I.append(node)

    def addF(self,node):
        assert node in self.Q
        self.F.append(node)


    def generateWords(self,maxlenght=10):
        runs = []
        words = []
        for i in self.I:
            runs.append(("",i))

        while runs:
            (word,q) = runs.pop(0)
            if len(word) > maxlenght:
                break
            if q in self.F:
                if not word in words:
                    words.append(word)
            
            for t in self.T:
                print(t)
                (s,a,r) = t
                if s == q:
                    if not (word+a,r) in runs:
                        runs.append((word+a,r))
        
        for word in words:
            if word == "":
                print("\u03B5")
            else:
                print(word)

    def find_free_state(self,prefix):
        if prefix in [x.description for x in self.Q]:
            return prefix
        i = 0
        while True:
            if prefix+"_"+i in [x.description for x in self.Q]:
                return prefix+"_"+i    

def main():
    A = Automata()
    q1 = Node("q1")
    q2 = Node("q2")
    q3 = Node("q3")
    q4 = Node("q4")
    A.addQ(q1)
    A.addQ(q2)
    A.addQ(q3)
    A.addQ(q4)

    A.addI(q1)
    A.addF(q1)
    A.addF(q3)
    
    A.addT(q1,"a",q1)
    A.addT(q1,"a",q2)
    A.addT(q1,"b",q2)
    A.addT(q2,"b",q2)
    A.addT(q2,"c",q3)


if __name__ == '__main__':
    main()