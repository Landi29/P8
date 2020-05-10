## Supervisor meeting 06/05/20

### Paper feedback

* The SimGNN results seem suspiciously low.
* We need to specify for the SimGNN what the target similarity is.
  * It can be that the underlying GED computation is so easy that it makes SimGNN not suitable since we can just calculate the GED ourselves.
* We need to understand what is happening behind the scene and explain this in more detail.
* It is surprising that the 3 methods get the exact same error results
  * There is a bug somewhere in our system
* We should first predict the baseline which could be the global average
  * If a method has an error that is worse than the baseline then it is worse.
* If we try to predict everything then how do we seperate training, validation and test set?
* A similarity construct like TET which tries to predict structural similarity doest really care what the individual users has rated.
* Do they look similar according to the attributes we have?
* Our technique isn't wrong but follows a different priciple which we need to take into account.
  * The problem right now is that our prediction method follows a differnet priciple which doesn't suit TET's very well since it doesn't focus on structural similarity.
* We might have to drop SimGNN since it would be overkill since it just tries to find a GED which we could easily calculate ourselves which would make it overkill.
* We should try to come up with a training example like the one we discussed during the meeting
* A user which has rated 3 western movies possitive and 2 comedy negative.
* Even if we have results on a very small dataset when we a testing on different methods it might still be good.
* What can be useful and what can be scaled?
* What do we mean with reliable in our sense? We need to explain this in our paper
  * We could argue that reliability is accuracy.
* In the introduction of our paper their seems to be a bit of fuzziness about what is content based recommender systems
* 





