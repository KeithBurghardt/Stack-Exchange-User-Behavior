# Stack-Exchange-User-Behavior

Original paper this code is for: 

"The Myopia of Crowds: Cognitive Load and Collective Evaluation of Answers on Stack Exchange"

By:

Keith Burghardt

Emanuel F. Alsina

Michelle  Girvan

William Rand

Kristina Lerman


This code was ripped straight from our original files, therefore it may require some tweaking. Data used in conjunction with this code is available upon request.

Reputation.py:
We reconstruct the reputation of an answerer just before an answer was voted on (this can be easily changed to be, e.g., the reputation at the moment an answer was made). The following was used to create a close facsimile of the true reputation (reputation rules are based on http://meta.stackexchange.com/questions/7237/how-does-reputation-work):

•	one of your questions is voted up/useful: +5 , 

•	one of your answers is voted up/useful: +10 , 

•	one of your answers becomes accepted: +15 , 

•	you accept an answer written by someone else to one of your own questions: +2 

•	one of your questions or answers is voted down/not useful: −2 

•	you vote an answer down/not useful: −1 

•	All users start with one reputation point. 


Furthermore, due to the information being unavailable, and in some cases as a simplification, we did not do the following:

•	a downvote on one of your questions or answers is removed: +2 

•	you suggest an edit and it is accepted: +2 (up to a total of +1000 per user)

•	you remove a downvote from an answer: +1 

•	an answer you downvoted is removed: +1 

•	one of your answers is awarded a bounty by the user offering the bounty: +full bounty amount 

•	one of your answers is awarded a bounty automatically: +½ of the bounty amount (see bounty FAQ for details) 

•	you associate accounts of two or more Stack Exchange network sites, and at least one of those accounts already has 200 or more 
reputation: +100 on each site (awarded a maximum of one time per site) 

•	(Stack Overflow only) one of your documentation contributions is approved: +2 

•	(Stack Overflow only) one of your documentation examples is voted up/useful: +5 

•	 a post where you had successfully suggested an edit has been deleted (reputation page shows the cause as "removed"): -2 

•	 the account of a user who was the final approver of a suggested edit you made has been deleted (reputation page shows the cause as 
"User was removed"): -2 

•	 an upvote on one of your questions is removed: −5 

•	 an upvote on one of your answers is removed: −10 

•	 one of your accepted answers loses accepted status: −15 

•	 you unaccept an answer written by someone else to one of your own questions: -2 

•	 you place a bounty on a question: −full bounty amount 

•	 one of your posts receives 6 spam or "it is not welcome in our community" flags(formerly known as offensive flags): −100 

•	If a vote is cast before a post becomes Community Wiki, but is removed after the post becomes CW, the removal does not affect reputation 
(source). 

•	 Before May 2011, downvoting questions cost the downvoter one reputation point (source). 

•	Deleting and undeleting posts may reverse reputation effects as well, if these posts have votes. Actions previously taken on deleted 
posts cease to affect reputation within five minutes (source), unless the post meets both the following criteria (in which case the 
reputation effects will be permanent) (source):

o	The post had a score of at least +3 

o	The post has been visible on the site for at least 60 days 

•	Voting reversal as a result of serial voting will return lost or gained reputation.

•	No user's reputation may drop below one point; if an action would cause a user's reputation to drop below one point, that user's 
reputation is set to one point (source). 

•	You can earn a maximum of +200 reputation from upvotes and suggested edits in any given day. Bounties and the bonuses for accepted 
answers are counted separately (source). Reputation "lost" from the reputation cap is not awarded on following days. 



In addition, we use the following code to parse data:



ParseVoteNormalize.py: Used to find the cumulative distribution function (CDF) of all the attributes we use in the model, and output a 
pickle file



ParseVotePData.py: Used to train the model on data from September 2009 until December 31, 2013.



glmnetLogisticRegression.R: Uses glmnet library (see: arxiv.org/pdf/1301.6375v3.pdf) and runs a penalized logistic regression of data, 
given the attributes listed in the paper. 

Output: 

Best fit regression coefficients ("BestBetas")

Penalization for lowest cross-validated error ("BestLambdas")

Deviance Ratio ("DevRatio")

Mean cross-validated error (measured in terms of deviance) for each penalization ("MeanCVPerLambda")

Standard deviations of the cross-validated error ("StdCVPerLambda")

Predicted probability and response for testing set used to find the ROC curve of the data ("ROC_test")



PlottingData.R: Used to convert the best fit coeffients into an easy-to-plot list.

Output:

Best regression coefficients versus number of answers 

Highest regression coefficients and lowest withing 1 standard deviation of the minimum mean cross-validated error
