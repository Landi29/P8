"""SimGNN runner."""

from simgnn.utils import tab_printer
from simgnn.simgnn import SimGNNTrainer
from simgnn.param_parser import parameter_parser

def main_SimGNN(training, test, number_of_graphs, labels):
    """
    Parsing command line parameters, reading data.
    Fitting and scoring a SimGNN model.
    """
    args = parameter_parser(training, test)
    tab_printer(args)
    trainer = SimGNNTrainer(args, number_of_graphs, labels)
    trainer.fit([])
    trainer.score()
