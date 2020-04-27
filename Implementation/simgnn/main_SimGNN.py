"""SimGNN runner."""

from src.utils import tab_printer
from src.simgnn import SimGNNTrainer
from src.param_parser import parameter_parser

def main_SimGNN(training, test, number_of_graphs, labels):
    """
    Parsing command line parameters, reading data.
    Fitting and scoring a SimGNN model.
    """
    args = parameter_parser(training, test)
    tab_printer(args)
    trainer = SimGNNTrainer(args, number_of_graphs, labels)
    trainer.fit()
    trainer.score()
