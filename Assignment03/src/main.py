from bayes_net import BayesNet

if __name__ == '__main__':
    net = BayesNet("data/earthquake.json")

    query = "Alarm"
    evidence = {"Burglary": True, "Earthquake": False}

    result = net.eliminate(query, evidence)
    for prob, val in zip(result, [True, False]):
        print(f"P({query}={val} | {evidence}) = {prob:.3f}")
