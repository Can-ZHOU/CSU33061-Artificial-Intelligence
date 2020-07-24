states = ["fit", "unfit", "dead"]
actions = ["exercise", "relax"]
Vn = [0,0,0]               # [fit, unfit, dead]
q0 = [[0,0], [0,0], [0,0]] # [[fit_exercise,fit_relax], [unfit_exercise,unfit_relax], [dead_exercise,dead_relax]]

'''
Exercise:
[(Probability), (Reward)]
---------------------------------------------------------------------
| exercise | fit                   | unfit                 | dead   |
|----------+-----------------------+-----------------------+--------|
| fit      | (0.9*0.99 = 0.891), 8 | (0.9*0.01 = 0.009), 8 | 0.1, 0 |
|----------+-----------------------+-----------------------+--------|
| unfit    | (0.9*0.2 = 0.18)  , 0 | (0.9*0.8 = 0.72)  , 0 | 0.1, 0 |
|----------+-----------------------+-----------------------+--------|
| dead     | 0                 , 0 | 0                 , 0 | 1  , 0 |
---------------------------------------------------------------------
'''
exercise = [
             [[0,0],[1,2],[0,0]], # fit
             [[0,0],[0,0],[1,2]],   # unfit
             [[0,0],[0,0],[1,4]]            # dead
            ]

'''
Relaxing:
[(Probability), (Reward)]
---------------------------------------------------------------------
| relax | fit                    | unfit                  | dead    |
|-------+------------------------+------------------------+---------|
| fit   | (0.99*0.7 = 0.693), 10 | (0.99*0.3 = 0.297‬), 10 | 0.01, 0 |
|-------+------------------------+------------------------+---------|
| unfit | (0.99*0 = 0)      , 5  | (0.99*1 = 0.99)   , 5  | 0.01, 0 |
|-------+------------------------+------------------------+---------|
| dead  | 0                 , 0  | 0                 , 0  | 1   , 0 |
---------------------------------------------------------------------
'''
relax = [
         [[0,0],[0,0],[1,1]], # fit
         [[0,0],[0,0],[1,2]],   # unfit
         [[0,0],[0,0],[1,4]]                # dead
        ]

def main():
    # Input
    n = int(input("Please input a positive integer n: "))
    while n < 0:
        n = int(input("n is greater or equal to 0, please try again: "))

    s = input("please input a state (fit, unfit, dead): ")
    while s not in states:
        s = input("states are fit or unfit or dead, please try again: ")

    G = float(input("Please input a gamma-setting G (0 < G < 1): "))
    while G < 0 or G > 1:
        G = float(input("0 < G < 1, please try again: "))

    for i in range(n+1):
        if i == 0:
            (q0_exercise, q0_relax)=v0_q0_calculate(s)
            print("n=" + str(i) + " exer:" + str(q0_exercise) + " relax:" + str(q0_relax))
        else:
            (qn_exercise, qn_relax)=vn_qn_calculate(s, G)
            print("n=" + str(i) + " exer:" + str(qn_exercise) + " relax:" + str(qn_relax))


def v0_q0_calculate(s):
    q0[0][0]= q0_calculate("fit", "exercise")
    q0[0][1] = q0_calculate("fit", "relax")
    
    q0[1][0] = q0_calculate("unfit", "exercise")
    q0[1][1] = q0_calculate("unfit", "relax")
    
    q0[2][0] = 0
    q0[2][1] = 0

    # Get V0
    # V0(s) = max( q0(s,exercise), q0(s,relax) )
    Vn[0] = max(q0[0][0], q0[0][1])
    Vn[1] = max(q0[1][0], q0[1][1])
    Vn[2] = 0
    
    # Get q0
    if s == "fit":
        q0_exercise = q0[0][0]
        q0_relax = q0[0][1]
    elif s == "unfit":
        q0_exercise = q0[1][0]
        q0_relax = q0[1][1]
    else:
        q0_exercise = q0[2][0]
        q0_relax = q0[2][1]

    return q0_exercise, q0_relax


def vn_qn_calculate(s, G):
    qn_exercise_fit = qn_calculate("fit", "exercise", G)
    qn_relax_fit = qn_calculate("fit", "relax", G)

    qn_exercise_unfit = qn_calculate("unfit", "exercise", G)
    qn_relax_unfit = qn_calculate("unfit", "relax", G)

    qn_exercise_dead = 0
    qn_relax_dead = 0

    # Update Vn
    # Vn(s) = max( qn(s,exercise), qn(s,relax) )
    Vn[0] = max(qn_exercise_fit, qn_relax_fit)
    Vn[1] = max(qn_exercise_unfit, qn_relax_unfit)
    Vn[2] = 0

    # Get qn
    if s == "fit":
        qn_exercise = qn_exercise_fit
        qn_relax = qn_relax_fit
    elif s == "unfit":
        qn_exercise = qn_exercise_unfit
        qn_relax = qn_relax_unfit
    else:
        qn_exercise = qn_exercise_dead
        qn_relax = qn_relax_dead

    return qn_exercise, qn_relax


def q0_calculate(q0_state, q0_action):
    s_index = find_s_index(q0_state)
    # q0(s,a) = p(s,a,fit)*r(s,a,fit) + p(s,a,unfit)*r(s,a,unfit)
    if q0_action == "exercise" :
        return exercise[s_index][0][0] * exercise[s_index][0][1] + exercise[s_index][1][0] * exercise[s_index][1][1]
    else:
        return relax[s_index][0][0] * relax[s_index][0][1] + relax[s_index][1][0] * relax[s_index][1][1]


def qn_calculate(qn_state, qn_action, G):
    s_index = find_s_index(qn_state)
    # qn+1(s,a) = q0(s,a) + γ(p(s,a,fit)*Vn(fit) + p(s,a,unfit)*Vn(unfit))
    if qn_action == "exercise" :
        return q0[s_index][0] + G * (exercise[s_index][0][0] * Vn[0] + exercise[s_index][1][0] * Vn[1])
    else:
        return q0[s_index][1] + G * (relax[s_index][0][0] * Vn[0] + relax[s_index][1][0] * Vn[1])


def find_s_index(state):
    if state == "fit":
        return 0
    elif state == "unfit":
        return 1
    else:
        return 2
    

if __name__ == '__main__':
    main()