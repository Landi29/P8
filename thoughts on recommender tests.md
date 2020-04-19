* There are subtleties that we need to take care of and explain.
  * Do we devide the data on the node level or the edge level?
  * This determines what would we be testing?
  * Lars: i would like to divide on edge level and test on the ability to construct or reconstruct edges between movies and users. We could do the same with list and try to reconstruct the list of bedst movies for a user
* Leave-one-out method
* Splitting the data into folds
  * Lars: i think we should make 20 folds this would allow us to take the standart 70/30 model for splitting training and test and addabt it to a 70/15/15 for training, validation and test.
* Recommender Systems handbook. Read the chapter on evaulating recommender systems.
  * Before the experiment: 
    * what is the **Hypothesis**?
    * what is our **Variables**?
    * can the conclutiuon be **Generalized**?
  * Offline experiments:
    * what is the **dataset**?
    * what kind of **behavior** does it simulate?
  * drawing conclutions:
    * what is our **confidence level and P-values**?
    * what is the **Accuracy**? (RMSE or MAE)
    * how ofthen is the prediction right? (**Usage Prediction**)
    * Can we see a clear best from the **Paired Results**?
* We should have that sorted by next week how we want to evaluate our recommender systems
