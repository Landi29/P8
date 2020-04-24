import pickle
import math

def predictGraph(graphDict):
    """
    The function loads in the the trained neural network and uses it to predict between
    two graphs and prints a prediction score.
    Parameter: graphDict is a dictionary that contains the two graphs we would like to compare
    Return: Returns a similarity score between the two graphs found in graphDict.
    """
    trainer = pickle.load(open("simGNN.p", "rb"))
    result = trainer.predictionScore(graphDict)
    print(-math.log(result))
