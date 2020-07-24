exerciseProb = [[0.891, 0.009, 0.1],
                [0.18,  0.72,   0.1],
                [0,     0,      1]]

exerciseReward =    [[8, 8, 0],
                    [0, 0, 0],
                    [0, 0, 0]]

            #relax| fit  |  unfit  | dead
relaxProb = [[0.693, 0.297, 0.01],
            [0,      0.99,  0.01],
            [0,      0,     1 ]]

relaxReward = [[10, 10, 0],
                [5, 5, 0],
                [0, 0, 0]]

q0 = [0,0,0,0,0,0]
qn = [0,0,0,0,0,0]
iteration = 0

def main():
    global qn
    global q0

    while True:
        G =  float (input("Enter G Value: 0 < G < 1 \n"))
        if(G>1 or G<0):
            print("Wrong input try again")
        else:
            False
            break
    while True:
        n = int (input("Enter n Value for iterations \n"))
        if(n<0):
            print("n must be positive\n")
        else:
            False
            break

    while True:
        s = input("Enter state (fit, unfit or dead)\n")
        if(s == "fit" or s=="unfit" or s=="dead"):
            False
            break
        else:
            print("Wrong input try again")

    exQN = [0,0,0]
    relaxQN = [0,0,0]

    for i in range(0,3):
         for j in range(0,3):
             exQN[i] = exerciseProb[i][j]*exerciseReward[i][j] + exQN[i]
             relaxQN[i] = relaxProb[i][j]*relaxReward[i][j] + relaxQN[i]


    qn = exQN + relaxQN
    for i in range(len(qn)):
        q0[i] = qn[i]

    decision(G,n,s)

def decision(G, n, s):
    global q0
    global qn
    global iteration

    if( s == "fit"):
         exercise = qn[0]
         relax = qn[3]
    elif (s=="unfit"):
         exercise = qn[1]
         relax = qn[4]
    else:
         exercise = qn[2]
         relax = qn[5]

    print("qn="+str(iteration) +" exer:"+str(exercise) + " relax:"+ str(relax))
    iteration = iteration+1

    sVal = ["fit", "unfit", "dead"]
    if (n>0):
        tempEx = [0,0,0]
        tempRel = [0,0,0]
        for i in range(0,3):
            for j in range(0,3):
                tempEx[i] = (exerciseProb[i][j]*Vn(sVal[j])) + tempEx[i]
                tempRel[i] = (relaxProb[i][j]*Vn(sVal[j])) + tempRel[i]
            tempEx[i] = tempEx[i]*G+q0[i]
            tempRel[i] = tempRel[i]*G+q0[i+3]

        for i in range(0,3):
            qn[i] = tempEx[i]
            qn[i+3] = tempRel[i]

        n = n-1
        decision(G, n, s)

def Vn(s):
    global qn

    if( s == "fit"):
        return max(qn[0], qn[3])
    elif (s=="unfit"):
        return max(qn[1],qn[4])
    else:
        return max(qn[2], qn[5])


if __name__ == '__main__':
    main()