"""SimGNN runner."""

from utils import tab_printer
from simgnn import SimGNNTrainer
from param_parser import parameter_parser
import pickle
import load

def main():
    """
    Parsing command line parameters, reading data.
    Fitting and scoring a SimGNN model.
    """
    args = parameter_parser()
    tab_printer(args)
    trainer = SimGNNTrainer(args)
    trainer.fit()
    trainer.score()
    pickle.dump(trainer, open("simGNN.p", "wb"))


if __name__ == "__main__":
    main()
