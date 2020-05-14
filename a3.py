import math
from math import log



class factor:
    def __init__(self, evidence, query):
        self.query = query
        self.evidence = evidence
#        self.res = []
        self.val = evidence + query
        self.val.sort()
        prob = None

    def set_prob(self,prob):
        self.prob = prob

    def restrict(self, variable, value):

        if variable not in self.val:
            return 0
        #self.res.append(variable)

        index = self.val.index(variable)
        #self.val.remove(variable)
        new_l = []
        for i in self.prob:
            tf = i[0]
            if value == tf[index]:
                new_l.append(i)
        self.prob = new_l

        return 1

    def sumout(self, val):
        index = self.val.index(val)

        new_prob =[]
        for i in self.prob:
            tf = i[0]
            tf.pop(index)
            new_prob.append((tf,i[1]))
        length = len(new_prob)
        final_prob = []
        for i in range(length):
            for j in range(i+1, length):
                if new_prob[i][0] == new_prob[j][0]:
                    pair = (new_prob[i][0],new_prob[i][1] +new_prob[j][1])
                    final_prob.append(pair)
        self.prob = final_prob
        self.val.remove(val)

    def print_fac(self):
        print("variables:\n {0}".format(convert_to_val(self.val)))
        print("table:")
        for i in self.prob:
            print(i)
        print("\n")

def convert_to_val(l):
    result =[]
    for i in l:
        if i == 1:
            result.append("OC")
        if i == 2:
            result.append("Fraud")
        if i == 3:
            result.append("Trav")
        if i == 4:
            result.append("FP")
        if i == 5:
            result.append("IP")
        if i == 6:
            result.append("CRP")
    return result

def normalize(a,b):
    sum = a+b
    return (a/sum, b/sum)

# return a new factor
def multiply(fac1, fac2):
    v1 = set(fac1.val)
    v2 = set(fac2.val)
    # print(fac1.prob)
    # print(fac2.prob)
    # print(v1)
    # print(v2)
    intersec = list(v1 & v2)
    intersec.sort()
    val = list(v1 | v2)
    val.sort()
    index_l = []

    for i in val:
        if i in fac1.val and i not in fac2.val:
            index = fac1.val.index(i)
            index_l.append((index, -1))
        elif i not in fac1.val and i in fac2.val:
            index = fac2.val.index(i)
            index_l.append((-1, index))
        else:
            index = fac1.val.index(i)
            index2 = fac2.val.index(i)
            index_l.append((index, index2))

    index_inter = []
    for i in index_l:
        if i[0] >= 0 and i[1] >= 0:
            index_inter.append(i)

    prob_l = []
    for i in fac1.prob:
        for j in fac2.prob:
            flag = True
            for k in index_inter:
                in1 = k[0]
                in2 = k[1]
                if i[0][in1] != j[0][in2]:
                    flag = False
                    break
            if flag == True:
                new_prob = i[1] * j[1]
                # print(new_prob)
                tf = []
                for k in index_l:
                    in1 = k[0]
                    in2 = k[1]
                    if in1 >= 0:
                        tf.append(i[0][in1])
                    else:
                        tf.append(j[0][in2])
                # print(tf)
                prob_l.append((tf, new_prob))
    new_fac = factor([],val)
    new_fac.set_prob(prob_l)

    return new_fac


def inference(factorlst, queryVar, eliminationVar, evidenceVar):
    fl = []
    for i in factorlst:
        fl.append(i)
    for i in eliminationVar:
        tmp = []
        # print("fac len is {0}".format(len(factorlst)))
        for j in fl:
            # print("---")
            # print(j.val)
            # print(len(factorlst))
            # print("---")
            if i in j.val:
                # print(j.val)
                # print(i)
                # print("try")
                factorlst.remove(j)


                tmp.append(j)


        while len(tmp) >1:
            f1 = tmp.pop()
            f2 = tmp.pop()
            newf = multiply(f1,f2)
            tmp.append(newf)
            newf.print_fac()
        final_fac = tmp[0]
        final_fac.sumout(i)
        # print("sumout is")
        # print(final_fac.prob)
        # print("end sumout")
        factorlst.append(final_fac)


    # print("fac len is {0}".format(len(factorlst)))
    while (len(factorlst) >1):
        f1 = factorlst.pop()
        f2 = factorlst.pop()
        newf = multiply(f1, f2)
        newf.print_fac()
        factorlst.append(newf)

    result = factorlst[0]
    for evi in evidenceVar:
        variable = evi[0]
        value = evi[1]
        result.restrict(variable, value)
    tup = normalize(result.prob[0][1],result.prob[1][1])
    normalized_result =[]
    normalized_result.append((result.prob[0][0], tup[0]))
    normalized_result.append((result.prob[1][0], tup[1]))
    result.prob = normalized_result
    print("final factor:")
    result.print_fac()







def main():
    print("A3 Q1")

if __name__ == "__main__":
    main()
    f1 = factor([], [3])
    f1.set_prob([([True],0.05),
                 ([False],0.95)])
    f2 = factor([2,3],[4])
    f2.set_prob([([True, True, True],0.9),([True, True, False], 0.1),
                 ([True, False, True], 0.1),([True, False,False],0.9),
                 ([False, True, True],0.9), ([False, True, False], 0.1),
                 ([False, False,True],0.01), ([False, False, False], 0.99)
                 ])
    f3 = factor([3], [2])
    f3.set_prob([([True,True], 0.01),([True, False], 0.004),
                 ([False,True], 0.99),([False, False], 0.996)])

    f4 = factor([1,2], [5])
    f4.set_prob([([True, True, True],0.02),([True, True, False], 0.98),
                 ([True, False, False], 0.99),([True, False,True],0.01),
                 ([False, True,True],0.001),  ([False, True, False], 0.999),
                 ([False, False,True],0.011),([False, False, False], 0.889)
                 ])

    f5 = factor([],[1])
    f5.set_prob([([True],0.6),
                 ([False],0.4)])
    f6 = factor([1],[6])
    f6.set_prob([([True,True], 0.1),([True, False], 0.9),
                 ([False,True], 0.001),([False, False], 0.999)])

    print("part b (i)\n")
    inference([f1, f3], [], [3], [])

    print("part b (ii)\n")
    inference([f1, f2, f3, f4, f5, f6], [], [1,3], [(6, True), (5, False), (4, True)])

    print("part c\n")
    inference([f1,f2,f3,f4,f5,f6],[],[1],[(6,True),(5,False),(4, True),(3,True)])

    print("part d\n")
    inference([f1, f2, f3, f4, f5, f6], [], [1], [(1, True),(6, True), (4, False), (5, True), (3, False)])

    # print("query is {0}".format(f2.query))
    # print("ev is {0}".format(f2.evidence))
    # # f2.restrict(4,True)
    # # f3.restrict(2, True)
    # print(f2.prob)
    # print("query is {0}".format(f2.query))
    # print("ev is {0}".format(f2.evidence))
    # print(f2.val)
    #
    # newf = multiply(f2, f3)
    # #newf = multiply(newf, f1)
    # newf.restrict(4, True)
    # print(newf.prob)
    # newf = multiply(newf, f1)
    #
    #
    # print(newf.prob)
    # print(newf.val)
    # newf.sumout(3)
    # # newf1 = multiply(f6, f4)
    # # newf1 = multiply(newf1, f5)
    #
    # print(newf.prob)
    # print(newf.val)
    #
    # newf1= multiply(f6, f4)
    # newf1.restrict(5, False)
    # newf1.restrict(6, True)
    #
    # newf1= multiply(newf1, f5)
    # newf1.sumout(1)
    #
    #
    # newf1 = multiply(newf1, newf)
    # print(newf1.prob)



















