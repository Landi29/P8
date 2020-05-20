# Reliability
Notes from 20/05 2020.

## What is Reliability:


#### In recommender systems:
A recommender can be accurate, fast and also trustworthy. With accurate, we mean that the system provides recommendations with a good rating estimate compared to the rating, the user would actually give the item.

* The system must also be idempotent, and it must produce the same results under similar conditions.
* A recommender system must also be updatable.
* A recommender system must be robust, thus being able to withstand attempts of manipulation.
* The system must only collect the amount of data necessary, in order to give accurate recommendations.

#### What aspects to consider when measuring Reliability (how do we want to measure Reliability):
* We want to focus on accuracy as the main measure and speed as a secondary measure, because we are not analyzing a full recommender system, but focus on the task of recommendation.
* We want to measure accuracy as an average precision value.
* This can be done with Root Mean Square Error (RMSE).
* Accuracy hypothesis:
  * We will define a baseline RMSE, and expect the other recommendation methods to be better.  
* As a consequens, we cannot say anything about best or worst case scenarios.
* Speed will be measured in seconds per recommendation.
* Speed hypothesis:
  * The average recommendation time is less than 10 seconds.
* Average human attention span is 12 seconds, so after 12 seconds, the recommendation might not be valuable anymore.

## Why do we use RMSE:
* It is one of two standard measures for measuring the difference between predicted and observed values.
* The other measure Mean Absolute Error (MAE).
* This measure is less tolerant regarding off values (wrongly predicted values) and it is thus better at telling us, if we have predicted wrong values.
