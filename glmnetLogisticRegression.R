
# glmnetLogisticRegression.r
#	By: Keith Burghardt
#
# Input: True/False,param1,param2,...
# Return: 	Logistic regression best-fit parameters ("Betas") with unimportant
#			coefficients removed using 
#			"Lasso and Elastic-Net Regularized Logistic Regression" algorithm
#
# for paper on the subject, see: http://web.stanford.edu/~hastie/Papers/glmnet.pdf
#
# for documentation of glmnet, see: arxiv.org/pdf/1301.6375v3.pdf
#

# To run: type: source("file_path_to/glmnetLogisticRegression.R")

#loading libraries

library(glmnet)
directory = "/export/data/ccbdata/keith/Local\ Stack\ Exchange\ Data/Files/Parsed Data/"
training_time = 1388534400 - 1199145600#time between Jan. 1, 2008 and Jan. 1, 2014
options(scipen=999)
for (BoardType in c("Meta","NonTech","Tech"))
{
	for(VoteStr in c("BeforeAnswerAccepted","AcceptedAnswers","AfterAnswerAccepted"))
	{
		for(AllBoardsStr in c("","_NoLargestBoard"))
		#for(AllBoardsStr in c(""))		
    		{
 		    #for(IsAccepted in c("NoAccept","Accept"))
 		    for(IsAccepted in c("Accept"))
		    {
  	                      # if answer is never accepted, 
 			# ignore the "AcceptedAnswers" and "AfterAnswerAccepted" attributes
			if(VoteStr != "BeforeAnswerAccepted" && IsAccepted == "NoAccept"){next}
			for (NumAns in 2:20)
			{
				######################################################################################
				#loading data
				#filedirectory = "~/Desktop/Local\ Stack\ Exchange\ Data/Files/LogitRegressionSE/"
				# file name for Tech No SO
				file=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,AllBoardsStr,"_Normalized_AllDataCDF_AfterAug2009_TrainedCDF_",as.character(NumAns),".csv",sep="")
                                if (AllBoardsStr == "" && BoardType == "Tech")
				{
  				    #file=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_New_",as.character(NumAns),".csv",sep="")
                                    #if (VoteStr == "AfterAnswerAccepted")
				    #{
	  				file=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_2Q_TrainedCDF_", as.character(NumAns),".csv",sep="")
	  				file2=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_3Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file3=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_4Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file4=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_5Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file5=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_6Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file6=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_7Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file7=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_8Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file8=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_9Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file9=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_10-15Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
	  				file10=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_SO","_Normalized_AllDataCDF_AfterAug2009_Over16Q_TrainedCDF_",as.character(NumAns),".csv",sep="")
  				    	file11=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_NoLargestBoard","_Normalized_AllDataCDF_AfterAug2009_TrainedCDF_",as.character(NumAns),".csv",sep="")
				    #}
				}
				print(paste("Parsing:",file))
			 	if(file.exists(file))
				{
				    yx = data.matrix(read.csv(file))
					
                                    if (AllBoardsStr == "" && BoardType == "Tech")
  				    {
					#if(VoteStr=="AfterAnswerAccepted")
					#{
 					    yx2 = data.matrix(read.csv(file2))
 					    yx3 = data.matrix(read.csv(file3))
 					    yx4 = data.matrix(read.csv(file4))
 					    yx5 = data.matrix(read.csv(file5))
 					    yx6 = data.matrix(read.csv(file6))
 					    yx7 = data.matrix(read.csv(file7))
 					    yx8 = data.matrix(read.csv(file8))
 					    yx9 = data.matrix(read.csv(file9))
 					    yx10 = data.matrix(read.csv(file10))
 					    yx11 = data.matrix(read.csv(file11))
	  			 	    print(file.exists(file11))
					    lenyx1 = length(yx11[1,])
					    yxnew = matrix(0,length(yx11[,1])+length(yx10[,1])+length(yx9[,1]) + length(yx8[,1]) + length(yx7[,1]) + length(yx6[,1]) + length(yx5[,1]) + length(yx4[,1]) + length(yx3[,1]) + length(yx2[,1]) + length(yx[,1]),lenyx1)
                                            for (i in 1:length(yxnew[1,])){yxnew[,i] = c(yx11[,i],yx10[,i],yx9[,i],yx8[,i],yx7[,i],yx6[,i],yx5[,i],yx4[,i],yx3[,i],yx2[,i],yx[,i])}
					    yx2=c()
					    yx3=c()
					    yx4=c()
					    yx5=c()
					    yx6=c()
					    yx7=c()
					    yx8=c()
					    yx9=c()
					    yx10=c()
					    yx11=c()

					#}
					#else{
  					#    	file2=paste(directory,"VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,"_NoLargestBoard","_Normalized_AllDataCDF_PostAug2009_",as.character(NumAns),".csv",sep="")
 					#     	yx2 = data.matrix(read.csv(file2))
					#    	yxnew = matrix(0,length(yx2[,1]) + length(yx[,1]),length(yx[1,]))
                                        #    	for (i in 1:length(yxnew[1,])){yxnew[,i] = append(yx2[,i],yx[,i])}
					#	yx2=c()
					#}
				    }
				    else {
				        yxnew = yx
				    }

   				    # make sure we have a descent amount of data for CV
				    if(length(yxnew[,1]) > 300)
				    {	
  					################################################################################
					# TRAINING DATASET
                		        # training time = Jan. 1, 2014
					# look for all votes BEFORE this time
					pos_train = which(yxnew[,16] < training_time)
                		        yxnew_train = yxnew[pos_train,]
					pos_test = which(yxnew[,16] >= training_time)
        		                yxnew_test = yxnew[pos_test,]
					################################################################################


					######################################################################################
					#splitting data into "input" and "response (T/F)"
				
					#input matrix
					x_train = c()
					x_test = c()
					y_train = c()
					y_test = c()
                                        end = 14
                        	        if (IsAccepted == "Accept" && VoteStr != "AcceptedAnswers"){end = 15}
                	                print("END: ")
        	                        print(end)
	
					#
					#    Fits for quality attributes (i > 7)
					#    Fits for heuristic attributes (i <= 7)
					#    Fits for all (comment out "next"
					#
					NewLen = end - 1
                              	       	for(i in 2:end)
					{
                                            # i | Attribute
                                            #---------------
                                            # 1 | PickAnswer?
                                            # 2 | Votes
                                            # 3 | VoteShare			# IGNORE
                                            # 4 | VoteOrder 
                                            # 5 | ChronologicalOrder
                                            # 6 | TimeSinceAnswer
                                            # 7 | WordsPerAnswer
                                            # 8 | WordSharePerAnswer
                                            # 9 | ReputationPerAnswer
                                            # 10| ReputationsAtVotePerAnswer     # IGNORE
                                            # 11| MeanRepRatePerAnswer   
                                            # 12| ReadabilityScorePerAnswer      
                                            # 13| AnswererAgePerAnswer   
                                            # 14| NumLinksPerAnswer      
                                            # 15| AcceptedAnswer?         
					    #ignore "None"
					    # The below attributes with "#IGNORE" should NEVER be incorporated into the model 
   					    if (i == 10 || i == 3 )
					    { 
                                                # 10| ReputationsAtVotePerAnswer     # IGNORE
                                                # 3 | VoteShare			     # IGNORE

						NewLen = NewLen - 1
						next
					    }

					    x_train = c(x_train,as.numeric(unlist(yxnew_train[,i])))
					    x_test = c(x_test,as.numeric(unlist(yxnew_test[,i])))
					}
					print("Organizing x, y")
					# NewLen: 14/15 - 2 (ignore 2 columns)
					# minus any more columns ignored (e.g., if we focus on quality/heuristics)
					x_train = matrix(x_train,length(yxnew_train[,2]),NewLen) #note we ignore *2* columns: T/F and rep per vote
					x_test = matrix(x_test,length(yxnew_test[,2]),NewLen) #note we ignore *2* columns: T/F and rep per vote
					
					#response vector
					y_train = as.numeric(unlist(yxnew_train[,1]))
					y_test = as.numeric(unlist(yxnew_test[,1]))
							
					######################################################################################
					#fitting the data
					print("Fitting data")
					# finding the best fit coefficients
					# we use the default options for logistic regression
	   			 	LogitFit<-cv.glmnet(x_train,y_train,family="binomial",alpha=0)#alpha = 0: Ridge Regression, alpha = 1: LASSO
		
					#Class Names, 1:False (didn't vote for this answer), 2:True (voted for this answer)
					ClassNames = LogitFit$glmnet.fit$classnames

					#extract coefficients, including those set to 0
					#Betas = NumVariables x length(lambdas)
					#For each lambda, "l", Betas are Betas[,l]
					Betas = LogitFit$glmnet.fit$beta

					#extract coefficients, including those set to 0
					#length(dev.ratio) = length(lambdas)
					#For each lambda, "l", Betas are Betas[,l]
					DevRatio = LogitFit$glmnet.fit$dev.ratio
					print("Deviance Ratio (how much of null deviance explained):")
					print(DevRatio)
						
    					#lambda values
	    				Lambdas = LogitFit$lambda
					print("Lambdas:")
					print(Lambdas)

    					#Mean 10-fold Cross-Validation Error
    					MeanCVPerLambda = LogitFit$cvm
					print("Mean CV Error Per Lambda:")
					print(MeanCVPerLambda)
				
					StdCVPerLambda = LogitFit$cvsd
					print("Std CV Error Per Lambda:")
					print(StdCVPerLambda)
			
  		  			#Lambda value with lowest mean error
					BestLambda = LogitFit$lambda.min
					print("Best Lambda:")
					print(BestLambda)

					# Find the position of BestLambda
					BestLambdaPos = which(Lambdas==BestLambda,arr.ind=TRUE)

					#Best betas
					BestBetas = LogitFit$glmnet.fit$beta[,BestLambdaPos]
					print("Best Betas:")
					print(BestBetas)
	
					######################################################################################	
					#Exporting data
					print("Exporting Data")
			  	        file_base=paste(directory,"All Data Fits Predict/","VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,AllBoardsStr,"_Normalized_AllDataCDF_RidgeRegression_Post2009,PreJanuary2014_FullModel_TrainedCDF_",as.character(NumAns),sep="")

					write.csv(BestBetas,paste(file_base,"_BestBetas_Train2009-2013",".csv",sep=""))
					write.csv(BestLambda,paste(file_base,"_BestLambda_Train2009-2013",".csv",sep=""))

					NumLambdas = length(Lambdas)
					for (i in 1:NumLambdas){
						write.csv(Betas[,i],paste(file_base,"_Betas_",i,"_Train2009-2013.csv",sep=""))
					}	
					write.csv(Lambdas,paste(file_base,"_Lambdas_Train2009-2013",".csv",sep=""))
					print(paste(file_base,"_DevRatio_Train2009-2013",".csv",sep=""))
					write.csv(DevRatio,paste(file_base,"_DevRatio_Train2009-2013",".csv",sep=""))
					write.csv(MeanCVPerLambda,paste(file_base,"_MeanCVPerLambda_Train2009-2013",".csv",sep=""))
					write.csv(StdCVPerLambda,paste(file_base,"_StdCVPerLambda_Train2009-2013",".csv",sep=""))
					x_train = c()
					y_train = c()
						
					#######################################################################
					######			 	ROC Curve		  	  #####
					#######################################################################

					p_test=predict(LogitFit,newx=x_test,s="lambda.min",type="response")
					ROC_test = matrix(0,2,length(p_test))
					ROC_test[1,] = y_test					
					ROC_test[2,] = p_test					
					write.csv(ROC_test,paste(file_base,"_ROC_2014",".csv",sep=""))
					x_test = c()
					y_test = c()
					p_test = c()
				    }
				}

			}
		    }
		}
	}
}
