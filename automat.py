import more_itertools
import itertools

class Node:
    def __init__(self, description):
        self.description = description
        self.inT = []
        self.outT = []

    def addInT(self,a, q):
        self.inT.append((a,q))

    def removeInT(self,a, q):
        self.inT.remove((a,q))

    def addOutT(self,a, r):
        self.outT.append((a,r))

    def removeOutT(self,a, q):
        self.outT.remove((a,q))

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
            new.addQ(i)
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

    def removeT(self,q,a,r):
        q.removeOutT(a,r)
        r.removeInT(a,q)
        self.T.remove((q,a,r))

    def addT(self,q,a,r):
        assert q in self.Q   
        assert r in self.Q  
        assert a != "" 
        self.T.append((q,a,r))
        q.addOutT(a,r)
        r.addInT(a,q)

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
        B = self.copy()
        qdead = Node(self.find_free_state("dead"))
        B.addQ(qdead)
        for q in B.Q:
            for a in B.alphabet:
                if not a in [x[0] for x in q.outT]:
                    B.addT((q,a,qdead))
        return B

    def complement(self):
        if self.isComplete():
            B = Automata.copy(self)
        else:
            B = self.makeComplete()
        new_F = []
        for q in self.Q:
            if q not in self.F:
                new_F.append(q)
        B.F = []
        for f in new_F:
            B.addF(f)
        return B

    def inital_normalized(self):
        B = Automata.copy(self)
        qinitial = Node(B.find_free_state("initial"))
        B.addQ(qinitial)
        for i in self.I:
            for t in i.outT:
                B.addT((qinitial,t[0],t[1]))
        B.I = []
        B.addI(qinitial)

        if set(self.I) & set(self.F):
            B.addF(qinitial)
        return B
        
    def final_normalized(self):
        B = Automata.copy(self)
        qfinal = Node(B.find_free_state("initial"))
        B.addQ(qfinal)
        for f in self.F:
            for t in f.inT:
                B.addT((t[1],t[0],qfinal))
        B.F = []
        B.addF(qfinal)

        if set(self.I) & set(self.F):
            B.addI(qfinal)
        return B

    def normalized(self):
        pass # todo

    def Kleene(self):
        print("Kleene")
        maxk = len(self.Q)-1
        sets =  []
        for i,f in itertools.product(self.I,self.F):
            indi = self.Q.index(i)
            indf = self.Q.index(f)
            x = self.X(maxk,indi,indf)
            sets.append(x)
        
        old = REGEX("MULTIUNION", sets)
        #pretty = old.getSmart()
        return old

    def X(self,k,m,l):
        if k == -1:
            t= [x[0] for x in self.Q[m].outT if x[1] == self.Q[l]]
            if len(t) == 0 and m!= l:
                return REGEX("EMPTY")
            if len(t) == 0 and m==l:
                return REGEX("EPSILON")
            if len(t) == 1:
                return REGEX("LITERAL",t[0])
            return REGEX("SET",[REGEX("Literal",x) for x in t])
        else:
            term1 = self.X(k-1,m,l)
            term2 = self.X(k-1,m,k)
            term3 = self.X(k-1,k,k)
            term4 = self.X(k-1,k,l)

            return REGEX("UNION",term1,REGEX("CONCAT",term2,REGEX("CONCAT",REGEX("STAR",term3),term4)))

class REGEX():
    def __init__(self,type,a = None,b = None):
        self.type = type
        self.a = a
        self.b = b

    def getSmart(self):
        if self.type == "STAR":
            if self.a.getSmart().type == "EMPTY":
               return REGEX("EPSILON")
            return REGEX("STAR",self.a.getSmart())
        if self.type == "CONCAT":
            if self.a.getSmart().type == "EMPTY":
                return REGEX("EMPTY")
            if self.b.getSmart().type == "EMPTY":
                return REGEX("EMPTY")
            if self.a.getSmart().type == "EPSILON":
                return self.b.getSmart()
            if self.b.getSmart().type == "EPSILON":
                return self.a.getSmart()
            return REGEX("CONCAT",self.a.getSmart(),self.b.getSmart())
        if self.type == "UNION":
            if self.a.getSmart().type == "EMPTY":
                return self.b.getSmart()
            if self.b.getSmart().type == "EMPTY":
                return self.a.getSmart()
            return REGEX("CONCAT",self.a.getSmart(),self.b.getSmart())
        if self.type == "MULTIUNION":
            if self.a == []:
                return REGEX("EMPTY")
            if len(self.a) == 1:
                return self.a[0].getSmart()
            self.a = [x.getSmart() for x in self.a]
            return self
        if self.type == "LITERAL":
            return self
        if self.type == "EMPTY":
            return self
        if self.type == "EPSILON":
            return self
        print("here not supoortet",self.type)


    def toString(self, point = False):
        smartself = self.getSmart()
        if smartself.type == "LITERAL":
            return smartself.a
        if smartself.type == "UNION":
            return "{ " + smartself.a.toString(point) +" UNION "+ smartself.toString(point) + " }"
        if smartself.type == "MULTIUNION":
            return "MULTIUNION{ " +" , ".join([x.toString(point) for x in smartself.a]) +"}"
        if smartself.type == "CONCAT":
            return smartself.a.toString(point) + " POINT "*point +smartself.b.toString(point) 
        if smartself.type == "STAR":
            return "("+ smartself.a.toString(point)+")*"
        if smartself.type == "EPSILON":
            return("E")
        
        print("not supported",smartself.type)

        pass

    def print(self):
        smartself = self.getSmart()
        if smartself.type == "MULTIUNION":
            print("MULTIUNION:{")
            for x in smartself.a:
                print(x.toString(),",")
            print("}")
        else:
            print(smartself.toString())




def main():
    A = Automata(["a","b"])
    q11 = Node("1,1")
    q13 = Node("1,3")
    q22 = Node("2,2")
    q32 = Node("3,2")
    q33 = Node("3,3")
    q31 = Node("3,1")
    A.addQ(q11)
    A.addQ(q13)
    A.addQ(q22)
    A.addQ(q32)
    A.addQ(q33)
    A.addQ(q31)

    A.addI(q11)
    A.addF(q11)
    A.addF(q13)
    A.addF(q33)

    A.addT(q11,"b",q11)
    A.addT(q11,"a",q22)

    A.addT(q22, "a", q32)
    A.addT(q22, "b", q13)

    A.addT(q13, "b", q11)
    A.addT(q13, "a", q22)

    A.addT(q32,"a",q32)
    A.addT(q32,"b", q33)

    A.addT(q33,"a",q32)
    A.addT(q33, "b", q31)
    A.addT(q31, "a", q32)
    A.addT(q31, "b", q31)


    A.Kleene().print()

if __name__ == '__main__':
    main()
