import more_itertools


class Node:
    def __init__(self, description):
        self.description = description
        self.inT = []
        self.outT = []

class Automata:
    def __init__(self,alphabet) -> None:
        self.Q = []
        self.T = []
        self.I = []
        self.F = []
        self.alphabet = alphabet

    def copy(A):
        new = Automata(A.alphabet)
        for q in A.Q:
            new.addQ(q)
        for i in A.I:
            new.addQ(I)
        for f in A.F:
            new.addQ(f)
        for t in A.T:
            new.addQ(t)

        return new

    def combine(A,B):
        assert  set(A.alphabet) == set(B.alphabet)
        
        new = Automata(A.alphabet)
        mapA = {}
        mapB = {}
        j = 1
        for q in A.Q:
            n = Node("q"+j)
            new.addQ(q)
            mapA[q] = n
            i+=1         
        for q in B.Q:
            n = Node("q"+j)
            new.addQ(q)    
            mapB[q] = n
            j+=1    
        
        for i in A.I:
            new.addI(mapA[i])
        for i in B.I:
            new.addI(mapB[i])

        for f in A.F:
            new.addF(mapA[i])
        for f in B.F:
            new.addF(mapB[i])
            
        for t in A.T:
            new.addT(mapA[t[0]],t[1],mapA[t[2]])
        for t in B.T:
            new.addT(mapB[t[0]],t[1],mapB[t[2]])
        return new

    def addQ(self,node):
        assert node.description not in [d.description for d in self.Q]
        self.Q.append(node)

    def addT(self,t):
        assert len(t) == 3 
        self.addT(t[0],t[1],t[2])


    def addT(self,q,a,r):
        assert q in self.Q   
        assert r in self.Q  
        assert a != "" 
        self.T.append((q,a,r))
        q.outT.append((a,r))
        r.inT.append((a,q))

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
            
            for t in q.outT:
                (a,r) = t
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

    def powerset_construction(self):
        B = Automata(self.alphabet)

        for i, combi in enumerate(more_itertools.powerset(self.Q)):
            
            B.addQ("q"+i)
            assert False, "ToDO"

    def isComplete(self):
        for q in self.Q:
            for a in self.alphabet:
                if a not in [x[0] for x in q.outT]:
                    return  False
        return True

    def isDeterministic(self):
        for q in self.Q:
            for t1 in q.outT:
                for t2 in q.outT:
                    if t1[0] == t2[0] and t1[1] != t2[1]:
                        return False
        return True 
    
    def makeComplete(self):
        B = Automata(self.alphabet,self.Q,self.T,self.I,self.F)
        qdead = Node(self.find_free_state("dead"))
        B.addQ(B)


        

             

def main():
    A = Automata(["a","b","c"])
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