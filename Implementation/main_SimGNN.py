"""SimGNN runner."""

from simgnn.utils import tab_printer
from simgnn.simgnn import SimGNNTrainer
from simgnn.param_parser import parameter_parser
import torch
import json
import torch.multiprocessing as mp
import pickle

def main_SimGNN(training, test, labels):
    """
    Parsing command line parameters, reading data.
    Fitting and scoring a SimGNN model.
    """
    args = parameter_parser(training, test)
    tab_printer(args)
    f = 4
    trainer = SimGNNTrainer(args, labels)
    processes = []
    #for processors in range(f):
    #    p = mp.spawn(fn=trainer.fit)
    #    processes.append(p)
    #for p in processes:
    #    p.join()
    trainer.fit()
    trainer.score()
    pickle.dump(trainer, open("simGNN.p", "wb"))

if __name__ == "__main__":
    with open("Movielens_data/SimGNN/2_to_9.json", "r") as file:
       training = json.load(file)
    with open("Movielens_data/SimGNN/fold0.json", "r") as file:
        test = json.load(file)
    with open("Movielens_data/SimGNN/Label_list.json", "r") as file:
        labels = json.load(file)
    main_SimGNN(training, test, labels)