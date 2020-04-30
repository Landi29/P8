def get_fold_indexes():
    training_folds = [
                        [
                            "fold0", "fold1", "fold2",
                            "fold3", "fold4", "fold5",
                            "fold6", "fold7"
                        ],

                        [
                            "fold1", "fold2",
                            "fold3", "fold4", "fold5",
                            "fold6", "fold7", "fold8"
                        ],

                        [
                            "fold2", "fold3",
                            "fold4", "fold5", "fold6",
                            "fold7", "fold8", "fold9"
                        ],

                        [
                            "fold3", "fold4",
                            "fold5", "fold6", "fold7",
                            "fold8", "fold9", "fold0"
                        ],

                         [
                            "fold4", "fold5",
                            "fold6", "fold7", "fold8",
                            "fold9", "fold0", "fold1"
                        ],

                         [
                            "fold5", "fold6",
                            "fold7", "fold8", "fold9",
                            "fold0", "fold1", "fold2"
                        ],

                        [
                            "fold6", "fold7",
                            "fold8", "fold9", "fold0",
                            "fold1", "fold2", "fold3"
                        ],

                         [
                            "fold7", "fold8",
                            "fold9", "fold0", "fold1",
                            "fold2", "fold3", "fold4"
                        ],

                        [
                            "fold8", "fold9",
                            "fold0", "fold1", "fold2",
                            "fold3", "fold4", "fold5"
                        ],
                        
                        [
                            "fold9", "fold0",
                            "fold1", "fold2", "fold3",
                            "fold4", "fold5", "fold6"
                        ]
                    ]     
    return training_folds