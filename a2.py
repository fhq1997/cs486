import math
from math import log
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q


class tree:
    def __init__(self, left, right, word_id, yes_instance, no_instance):
        self.left = left
        self.right = right
        self.word = word_id
        self.yes = yes_instance
        self.no = no_instance

        y_count = len(self.yes)
        n_count = len(self.no)
        self.estimate = expectation(y_count, n_count)

    def expand(self, word_l):
        #initialize left, right and word id

        child_left_yes = []
        child_left_no =[]
        child_right_yes = []
        child_right_no = []
        delta = 0
        for i in word_l:
            ly =[]
            ln =[]
            ry =[]
            rn =[]
            for j in self.yes:
                if i in j:
                    ly.append(j)
                else:
                    ry.append(j)
            for j in self.no:
                if i in j:
                    ln.append(j)
                else:
                    rn.append(j)
            E1 = expectation( len(ly), len(ln))
            E2 = expectation( len(ry), len(rn))
            N1 = len(ly) + len(ln)
            N2 = len(ry) + len(rn)
            #tmp_delta = ave_info_gain(self.estimate, E1, E2)
            tmp_delta = weighted_info_gain(self.estimate, E1, E2,N1, N2)
            #print("tmp delta is {0}".format(tmp_delta))
            if tmp_delta > delta:
                child_left_no = ln
                child_left_yes = ly
                child_right_no = rn
                child_right_yes = ry
                self.word= i
                delta = tmp_delta
            #print(tmp_delta)


        t1 = tree(None, None, None, child_left_yes, child_left_no)
        t2 = tree(None, None, None, child_right_yes, child_right_no)
        # print(len(child_left_yes))
        # print(len(child_left_no))
        # print(len(child_right_yes))
        # print(len(child_right_no))
        if delta == 0:
            self.left = None
            self.right = None
         #   print("leaf")
            return delta

        self.left = t1
        self.right = t2
        #print(delta)
        return delta







def expectation(yes_count, no_count):
    if yes_count == 0 or no_count == 0:
        return 0
    total = yes_count + no_count
    prob = yes_count / total
    result = - math.log(prob,2) * prob - (1-prob) * math.log(1-prob,2)
    return result

def ave_info_gain(E, E1, E2):
    return E - 0.5*E1 -0.5*E2

def weighted_info_gain(E, E1, E2, N1, N2):
    return E - N1/(N1+N2) * E1 -N2/(N1+N2) *E2



def main():
    print("Decision tree")

if __name__ == "__main__":
    main()

    # use a list to store all input data
    file1 = open("trainData.txt", "r")
    lines = file1.readlines()
    file1.close()
    #print(lines[0].split())
    dic = {}
    training = []
    word_dic = {}
    for i in lines:
        i = i.split()
        if i[1] not in word_dic:
            word_dic[i[1]] = 1
        else:
            word_dic[i[1]] += 1

        if i[0] not in dic:
            tmp = [i[0], [i[1]]]
            training.append(tmp)
            dic[i[0]] = len(training)
        else:
            index = dic[i[0]] - 1
            training[index][1].append(i[1])

    file2 = open("trainLabel.txt", "r")
    line1 = file2.readlines()
    tmp_in = 0
    for i in training:
        index = int(i[0])
        i.append(line1[index-1].split()[0])
    file2.close()
    #for i in range(len(line1)):
    #    training[i].append(line1[i])

    #for i in range(5):
    #    print(training[i])
    word_list = list(word_dic.keys())
    yes_instance =[]
    no_instance = []
    for i in training:
        if i[2] == '1':
            yes_instance.append(i[1])
        else:
            no_instance.append(i[1])

    root = tree( None, None, None, yes_instance, no_instance)
    PQ = Q.PriorityQueue()
    #PQ.put((0,root))
    info = root.expand(word_list)
    delta1 = root.left.expand(word_list)
    delta2 = root.right.expand(word_list)
    if delta1 > 0:
        t = (-1 * delta1, root.left)
        PQ.put(t)
    if delta2 > 0:
        t = (-1 * delta2, root.right)
        PQ.put(t)
    #
    count = 0
    while not PQ.empty() and count <= 20:
        node = PQ.get()
        cur = node[1]
        d1 = cur.left.expand(word_list)
        d2 = cur.right.expand(word_list)

        print("word is {0} with {1}".format(cur.word, node[0]))
        if d1 > 0:
            PQ.put((-1 *d1, cur.left))
        if d2 > 0:
            PQ.put((-1 *d2, cur.right))

        # q1 = list(PQ.queue)
        # for i in q1:
        #     print("count is {0}".format(count))
        #     print("{0}  {1}" .format(i[0], i[1].word))
        count += 1
    print("count is")
    print(count)










