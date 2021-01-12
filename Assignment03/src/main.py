from bayes_net import BayesNet

if __name__ == '__main__':
    net = BayesNet("data/earthquake.json")
    net.sort_topological()
    net.probability("Alarm", {'Alarm': True, 'Burglary': True, "Earthquake": False})

    query = 'Alarm'
    evidence = {'Burglary': 'True'}
