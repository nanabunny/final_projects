import random as rd

C = {0.05: 0.003801658303553139101756466, 0.1: 0.014745844781072675877050816,
     0.15: 0.032220914373087674975117359, 0.2: 0.055704042949781851858398652,
     0.25: 0.084744091852316990275274806, 0.3: 0.118949192725403987583755553,
     0.35: 0.157983098125747077557540462, 0.4: 0.201547413607754017070679639,
     0.45: 0.249306998440163189714677100, 0.5: 0.302103025348741965169160432,
     0.55: 0.360397850933168697104686803, 0.6: 0.422649730810374235490851220,
     0.65: 0.481125478337229174401911323, 0.7: 0.571428571428571428571428572,
     0.75: 0.666666666666666666666666667, 0.8: 0.750000000000000000000000000,
     0.85: 0.823529411764705882352941177, 0.9: 0.888888888888888888888888889,
     0.95: 0.947368421052631578947368421}

# curr_trial is the # of trials (curr included) from last success


def PRD(chance, curr_trial):
    curr_chance = C[chance] * curr_trial
    if rd.random() < curr_chance:
        return True
    return False


def TRD(chance):
    return rd.random() < chance


def getPRDSequence(chance, trials):
    seq = []
    curr_trial = 1
    for trial in range(trials):
        if PRD(chance, curr_trial):
            curr_trial = 1
            seq.append(trial)
        else:
            curr_trial += 1
    return seq


def getTRDSequence(chance, trials):
    seq = []
    for trial in range(trials):
        if TRD(chance):
            seq.append(trial)
    return seq


def test():
    chance = 0.3
    trials = 20
    tries = 100

    prd_sqr_diff = 0
    trd_sqr_diff = 0

    for i in range(tries):
        prd_seq1 = getPRDSequence(chance, trials)
        prd_seq2 = getPRDSequence(chance, trials)
        prd_sqr_diff += (len(prd_seq1) - len(prd_seq2))**2

        trd_seq1 = getTRDSequence(chance, trials)
        trd_seq2 = getTRDSequence(chance, trials)
        trd_sqr_diff += (len(trd_seq1) - len(trd_seq2))**2

    print((prd_sqr_diff+0.0)/tries, (trd_sqr_diff+0.0)/tries)
