directory = "/export/data/ccbdata/keith/Local\ Stack\ Exchange\ Data/Files/Parsed Data/"
#directory = "~/Desktop/Local Stack Exchange Data/Files/LogitRegressionSE/"
for(BoardType in c("Meta","NonTech","Tech"))
{
        for(VoteStr in c("BeforeAnswerAccepted","AcceptedAnswers","AfterAnswerAccepted"))
        {
                for(IsAccepted in c("Accept","NoAccept"))
                {
                        # if answer is never accepted,
                        # ignore the "AcceptedAnswers" and "AfterAnswerAccepted" attributes
                        if(VoteStr != "BeforeAnswerAccepted" && IsAccepted == "NoAccept"){next}
			for(AllBoardsStr in c("_NoLargestBoard",""))
                        {
				# NOTE FOR ACCEPT: TotalNumParams = 11
                            TotalNumParams = 12  #12 - 2
                            if (VoteStr == "AcceptedAnswers"){TotalNumParams = 12 - 1}  #12 - 2
				# NOTE FOR ACCEPT: comment this out, else LEAVE UN-COMMENTED
                            #if (VoteStr == "AfterAnswerAccepted" || (VoteStr == "BeforeAnswerAccepted" && IsAccepted == "Accept")){TotalNumParams = TotalNumParams + 1}
                            print(TotalNumParams)
    			    print("Importing Data")
    			    BestBetas = c()
    			    BetasLow = c()
    			    BetasHigh = c()
    			    Betas = c()
    			    BestLambda = c()
    			    Lambdas = c()
    			    Betas = c()
    			    MeanCVs = c()
    			    StdCVs = c()
                            NoVals = rep.int(NA,TotalNumParams)
                            for (NumAns in 2:40)
                            {
				#RemovedAttribute = "Accept"#"WebpageOrder"#"Accept"#"WordShare"#"ChronologicalOrder"#
				file_base=paste(directory,"All Data Fits Predict/","VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,AllBoardsStr,"_Normalized_AllDataCDF_RidgeRegression_Post2009,PreJanuary2014_FullModel_TrainedCDF_",as.character(NumAns),sep="")
				#VoteP_Tech_Logit_Accept_BeforeAnswerAccepted_Normalized_AllDataCDF_RidgeRegression_Post2009,PreJanuary2014_FullModel_9_MeanCVPerLambda_Train2009-2013.csv		              
				BestBetaFile=paste(file_base,"_BestBetas","_Train2009-2013.csv",sep="")
				BetaFileBase=paste(file_base,"_Betas_",sep="")
				BestLambdaFile=paste(file_base,"_BestLambda","_Train2009-2013.csv",sep="")
				LambdasFile=paste(file_base,"_Lambdas","_Train2009-2013.csv",sep="")
				MeanCVsFile=paste(file_base,"_MeanCVPerLambda","_Train2009-2013.csv",sep="")
				StdCVsFile=paste(file_base,"_StdCVPerLambda","_Train2009-2013.csv",sep="")
				print(BestBetaFile)
				print(file.exists(BestBetaFile))
                                if(file.exists(BestBetaFile))
                                {
                                    NewBestBetaVals=c(read.csv(BestBetaFile))$x
                                    BestBetas=c(BestBetas,NewBestBetaVals)
                                    MeanCVVals=c(read.csv(MeanCVsFile))$x
				    MinCVPos = match(min(MeanCVVals),MeanCVVals)
                                    StdCVVals=c(read.csv(StdCVsFile))$x
				    UpperCVPos = which.min(abs(min(MeanCVVals) + StdCVVals[MinCVPos] - MeanCVVals))
				    LowerCVPos = which.min(abs(min(MeanCVVals) - StdCVVals[MinCVPos] - MeanCVVals))

                                    BetasHigh=c(BetasHigh,c(read.csv(paste(BetaFileBase,UpperCVPos,"_Train2009-2013.csv",sep="")))$x)
                                    BetasLow=c(BetasLow,c(read.csv(paste(BetaFileBase,LowerCVPos,"_Train2009-2013.csv",sep="")))$x)
                                    print("Length of Beta Vals: ")
                                    print(length(NewBestBetaVals) == length(NoVals))
                                    print(NewBestBetaVals)
                                    print(length(BestBetas))

                                }else{
				    BestBetas = c(BestBetas,NoVals)
				    BetasHigh = c(BetasHigh,NoVals)
				    BetasLow  = c(BetasLow,NoVals)
				}

                            }
                            BestBetas=matrix(unlist(BestBetas),length(NoVals),length(BestBetas)/length(NoVals))	
                            BetasHigh=matrix(unlist(BetasHigh),length(NoVals),length(BetasHigh)/length(NoVals))	
                            BetasLow=matrix(unlist(BetasLow),length(NoVals),length(BetasLow)/length(NoVals))	

			    params=c(	"Votes",
					#"VoteShare",
					"VoteOrder",
					"ChronologicalOrder",
					"TimeSinceAnswer",
					"WordsPerAnswer",
					"WordSharePerAnswer",
					"ReputationPerAnswer",
					"MeanRepRatePerAnswer",
					"ReadabilityScorePerAnswer",
					"AnswererAgePerAnswer",
					"NumLinksPerAnswer"
					,"IsAnswerAccepted"
					)

  	 	  	    write_file_base=paste(directory,"All Plot Train/","VoteP_",BoardType,"_Logit_",IsAccepted,"_",VoteStr,AllBoardsStr,"_Normalized_AllDataCDF_RidgeRegression_Post2009,PreJanuary2014_FullModel_TrainedCDF_",sep="")

			    for(i in 1:length(NoVals))
			    {
                                if(params[i] == "VoteOrder"){
				    BestBetas[i,] = -BestBetas[i,]
				    BetasHigh[i,] = -BetasHigh[i,]
				    BetasLow[i,] = -BetasLow[i,]
				}
				print(params[i])
				#print(BestBetas[i,])
                                BestBetasVals=matrix(unlist(c(2:40,BestBetas[i,])),39,2)
				#print(BestBetasVals)
                                write.table(BestBetasVals,paste(write_file_base,"BestBetas_",params[i],".dat",sep=""))
                                BetasHighVals=matrix(unlist(c(2:40,BetasHigh[i,])),39,2)
				#print(BetasHighVals)
                                write.table(BetasHighVals,paste(write_file_base,"BetasHigh_",params[i],".dat",sep=""))
                                BetasLowVals=matrix(unlist(c(2:40,BetasLow[i,])),39,2)
				#print(BetasLowVals)
                                write.table(BetasLowVals,paste(write_file_base,"BetasLow_",params[i],".dat",sep=""))
			    }
			}
		}
	}
}
