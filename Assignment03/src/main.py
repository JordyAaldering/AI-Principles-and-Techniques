from bayes_net import BayesNet

def print_result(query, evidence, result):
    evidence = ", ".join([f"{e}={evidence[e]}" for e in evidence])
    for prob, val in zip(result, [True, False]):
        print(f"P({query}={val} | {evidence}) = {prob:.3f}")

if __name__ == "__main__":
    query = "Alarm"
    evidence = {
        "Burglary": True,
        "Earthquake": False
    }

    net = BayesNet("data/earthquake.json")
    result = net.eliminate(query, evidence)
    print_result(query, evidence, result)
