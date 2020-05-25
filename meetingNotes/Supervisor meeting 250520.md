## Supervisor meeting 25/05/20

### Questions 

* What does "baseline with meta data mean"
  * A simple K-NN baseline on feature vectors could used for movies and users which is an aggregated feature vector in which we could use cosine for as a baseline to test if our model perform better than simple methods.
  * We most likely won't have time for it
* A better word than idempotens
  * Our interpretation is more deterministic
    * If nothing happens then the result is the same
  * Idempotens doesn't really have anything to do with this
  * We have to be careful if we mean "producing the same result under identical conditions" or "producing identical conditions under similar conditions"
    * These two doesn't mean the same
* We should explain our hypothesis 2 
  * The average recommendation time of what?....
    * Explain about this
* RMSE off values
  * We should use the word "outlier values" instead of "off values"
  * A small number of relatively extreme conditions can dominate the predictions
  * We shouldn't worry about this since our values are between 1 and 5 so at worst it can be 4
  * We can also include MAE data and simply just delete the sentence and not worry about it
    * We already have the data
* TET special scenario
  * In the scenario we have setup the task is more difficult since we seperate the training and test set and we would like to model the cold item start problem
    * Can we explain why in this scenario for why TET gets a lower RMSE value (seen in figure 14) when compared to the normal task seen in figure 11.
* We can keep the explanation that we we split the data in 80/10/10 but in our experimentation section or conclusion section we can simply just say that we never use it for anything.
* Validation sets can be used for hyperparameter tuning
  * An example of this could be the number of nearest neighbors
    * We could calibrate this using the validation set
* We should try and make a few references to the appendicies
  * Try and establish some form of connection between it and the main paper.
  * We could include it in the discussion of the conclussion and reference it there
  * Gives the censor a reason to read the appendix
* 

### AOB

Pre exam supervisor meeting will be held on the 18'th of June in the afternoon at 13:00 pm o'clock.