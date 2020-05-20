## Supervisor meeting 18/05/20

### Questions

* Reliability comment on section V-B
  * What is reliability in this context?
  * In which sense do we want to analyze reliability?
  * What does it mean that a recommender system is reliable?
  * What are our Reliability objectives?
    * Explain this first
    * Runtime goals and accuracy could be goals here
    * Accuracy needs to be specifed pretty accurately?
    * Do we see RMSE score below 1 as reliable, 1.10 or 1.50?
  * The section needs to be explained clearly
  * We should explain that reliability of the answers is an average case basis not a worst case? We can't promise it will be reliable all the time but we can promise it will be most of the time.
  * Before we discuss metrics we need to explain how we measure and argue that our measures is a measure of reliability.
  * It pretty critical if we don't get this right and we can easily get a lower grade due to it.
  * We need to have some substantial in our section and with some metrits.
  * Need to sell our system as reliable and be believable.
* Are we planning on also doing some stastitical tests?
  * Linked to our reliability section
  * We mention some tests earlier in the paper but are we planning on adding any.
  * example of how we can do it: [https://en.wikipedia.org/wiki/Student%27s_t-test](https://en.wikipedia.org/wiki/Student's_t-test)
  * Is Manfreds method statistically the best in all cases?
  * Look at the slides at the VIT course
  * We can also test the response time.
  * Form hypothesis and test them
  * The t test should be pretty simple. 
  * We can basically just copy and paste our data into a t-test calculator
  * We should only do all of this if time allows for it.
  * We could also do it prior to the exam if we don't do it now.
  * Manfred and Peter means although that we should not do it unless it brings something that is clearly missing/incomplete from our paper. Otherwise it could create more confussion.
    * Don't consider the time time between the handin and the exam as an extension because they can evaluate it properly at the exam and it's also against what the handin is for.
* The scenario case

  * It would be nice to see how many predictions there is for a single user
  * Why don't we try and predict on all the user instead of a single user?
  * We need to explain what it really shows?
  * Peter means that the data should be randomized.
  * This will be a discussion at the exam so we need to be able to defend it.
  * How do we want to show the results.
  * We should explain in detail what the data shows, how it show reliability.
  * The high invariance between the folds could show that they aren't many prediction per user.
  * We need to come up with a good explanation.
  * We should test for several user and then randomize and hide users in different folds and still be able to predict.
  * We should describe that we are trying how it avoids the cold start problems
  * we should explain more scenarios.
  * It's not enough to test only against one user.
  * We could take from every user and take the average.
  * We should really be precise about how we test before we show results.
  * What are the advantages and disadvantages of the protocol compared to others.
  * We should all be clear what we are doing. It's gonna be clear at the exam what will be missing.
* There are some lack of understanding that we need to deal with ASAP.

* We could do a stasticical significance test.
  * We could do a stastitical test that looks at the overall average by looking at the predictions.

Meeting at the 25 of May at 14:00

Send the draft on friday morning.
