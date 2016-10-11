import ast
import functools
import math
from bisect import bisect_left
import pickle
import itertools

SONumAns = 7;

def mean(l):
    mu = float(sum(l))/len(l) if len(l) > 0 else float('nan')
    return mu

# taken from Stack Overflow: http://stackoverflow.com/questions/212358/binary-search-bisection-in-python
def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi else -1) # don't walk off the end

def CDF(binary_search,sorted_list,x,bin_width):
    if x < max(sorted_list):
        # Perform a binary search:
        #    Find pos s.t. list[pos] >= x
        #    P(i <= x) = (pos + 1) * bin_width (note: this is only true because pos starts at 0)
        pos = binary_search(sorted_list,x)
        p = (pos + 1) * bin_width
    else: p = 1.0
    return p

def MonthToSecond(Year,Num):
    NumDays = 30
    #Number of days in a given month
      
    if Num in [1,3,5,7,8,10,12]:
        NumDays = 31
        
    elif Num == 2:
        if Year in [2008,2012,2016]:
            NumDays = 29
        else:
            NumDays = 28            
        
    NumSecs = NumDays*86400;
    return NumSecs
def Time(MonthToSecond,date):
    #Number of seconds BEFORE this year
    YearsToSec = 31536000*(date[0] - 2008)
    #number of leap days BEFORE this year
    leapdays = 0
    if date[0] > 2008:
        leapdays = 1
    if date[0] > 2012:
        leapdays = 2
    
    #number of seconds BEFORE this month
    MonthsToSec = sum([MonthToSecond(date[0], date[1] - i) for i in range(1,int(date[1]))])

    #number of seconds BEFORE today (plus leap days)
    DaysToSec = 86400*(date[2] - 1 + leapdays)
    #number of seconds up to the current hour
    HoursToSec = 60*60*date[3]
    #number of seconds up to the current minute
    MinsToSec = 60*date[4]
    #number of seconds since the minute started
    Secs = date[5]

    #TOTAL time
    time = YearsToSec + MonthsToSec + DaysToSec + HoursToSec + MinsToSec + Secs
    return time      



def ParallelWork(VotesOverTimeADataAcceptVotesAcceptAns):

    VotesOverTimeBoardName,ADataBoardName,ACCEPT,VOTES_ACCEPT_ANSWER = VotesOverTimeADataAcceptVotesAcceptAns
    VotesOverTimeADataAcceptVotesAcceptAns = []
    
    #print the board name
    print(ADataBoardName[0][0])
    VotePBoardName = []
    ADataNumAnsPos = [[] for i in range(len(VotesOverTimeBoardName))]
    for lineAnswerIndex in range(len(ADataBoardName)):
        Num = int(ADataBoardName[lineAnswerIndex][1]);
        if Num > 199 or Num < 2: continue
        #if ADataNumAnsPos[Num-2] == []:
        ADataNumAnsPos[Num-2].append(lineAnswerIndex)
        #record the last position where NumAns is oberved
        #else: ADataNumAnsPos[Num-2][1] = lineAnswerIndex

    for TotalNumberOfAnswers in range(SONumAns,SONumAns +1): #range(2,len(VotesOverTimeBoardName) + 1):#1, 2, 3, 4, ...
        print(TotalNumberOfAnswers)    
        if len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1]) == 0: continue 
        PrevQid = 0
        thread  = -1
        indices = ADataNumAnsPos[TotalNumberOfAnswers-2]
        if len(indices) > 0:
            for lineIndex in indices:
                    Qid = ADataBoardName[lineIndex][3]
                    # if this is a new question...
                    #if Qid not in Qids:
                    if Qid != PrevQid:
                        PrevQid = Qid
                        thread = thread + 1
                        if len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread]) == 0: continue

                        Aid = [int(ADataBoardName[lineIndex + i][2]) for i in range(TotalNumberOfAnswers)]
                        AidSortedIndices = sorted(range(len(Aid)),key=lambda x:Aid[x])
                        Aid = sorted(Aid)


                        # User ID associated with each answer (Aid)
                        
                        pos = 4                        
                        AcceptedAnswer = 9999
                        if ACCEPT:
                            pos = 5
                            
                            if ADataBoardName[lineIndex][pos - 1] in Aid:
                                AcceptedAnswer = Aid.index(ADataBoardName[lineIndex][pos - 1])

                        Uid = [ADataBoardName[lineIndex + i][pos] for i in AidSortedIndices]
                        
                        # Time each answer was made 
                        Ta = [ADataBoardName[lineIndex + i][pos + 1] for i in AidSortedIndices]

                        pos = 7
                        if ACCEPT:
                            pos = 8
                        # Number of Words
                        NumWords = [ADataBoardName[lineIndex + i][pos] for i in AidSortedIndices]

                        # The answer's number of hyperlinks*)
                        NumLinks = [ADataBoardName[lineIndex + i][pos + 1] for i in AidSortedIndices]

                        # The answer's readability
                        ReadabilityScore = [ADataBoardName[lineIndex + i][pos + 4] for i in AidSortedIndices]
                        
                        # Answerer reputation just before answer is created
                        Reputation = [ADataBoardName[lineIndex + i][pos + 5] for i in AidSortedIndices]

                        #Seconds since user signed up

                        DaysSinceSignUp = [ADataBoardName[lineIndex + i][pos + 6]/86400 for i in AidSortedIndices]

                        # Note: this SHOULD NOT happen.
                        # We find that this DOES happen, so this data may be wrong, and we ignore it
                        for i,days in enumerate(DaysSinceSignUp):
                            if days <= 0 or days > 999999999999999999:
                                DaysSinceSignUp[i] = None
                       
                        MeanRepRate = [None for i in range(TotalNumberOfAnswers)]          
                        for i in range(TotalNumberOfAnswers):
                            if Reputation[i] != None and DaysSinceSignUp[i] != None:
                                MeanRepRate[i] = Reputation[i]/DaysSinceSignUp[i]


                        # 
                        #   We start with 0 votes per answer and an arbitrary answer order.
                        #   This changes as more votes are cumulatively added
                        #

                        # Array of 0s of length "Total number of answers"
                        VotesPerAnswer = [0] * TotalNumberOfAnswers

                        AnswerOrder = [0] * TotalNumberOfAnswers
                        AnswerNotAcceptedYet = True

                        # for the current number of answers equal to 2, 3, 4,...Total Number Of Answers
                        for CurrentNumberOfAnswers in range(1,TotalNumberOfAnswers+1):

                            TotalNumWords = sum([n for n in NumWords[:CurrentNumberOfAnswers]])
                            if TotalNumWords > 0:
                                WordShare = [n/TotalNumWords for n in NumWords[:CurrentNumberOfAnswers]]
                            else: print(NumWords)
                            #print(CurrentNumberOfAnswers)
                            #print(len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1]))
                            #print(len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread]))
                            if len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1]) > 0:
                                #All votes made (in chronological order) in this timeframe
                                CurrentVote = VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1]
                                # If CurrentVote = {a,b,c,d}, then it should be {{a,b,c,d}}
                                for v in CurrentVote:
                                    if len(v) > 2:
                                        if v[2] == 1:
                                                AnswerNotAcceptedYet = False

                                        # CASES: 
                                        #     1) Before acceptance: ignore if Answer is accepted
                                        #     2) Accept answer: ONLY record data if answer is accepted
                                        #     3) After acceptance: ignore UNLESS answer is already accepted
                                        #
                                        

                                        UpVote = v[2]
                                        if UpVote == 2:
                                                UpVote = 1
                                        elif UpVote == 3:
                                                UpVote = -1

                                        # Which Answer was voted
                                        VoteAid = v[1]
                                        if VoteAid in Aid[:CurrentNumberOfAnswers]:

                                                Apos = Aid.index(VoteAid)
                            

                                                # Votes for each answer and record whether answer was chosen
                                                # note answer is in chronological order,
                                                #   and VotesPerAnswer was reordered appropriately

                                                Votes = [[j == Apos, VotesPerAnswer[j]] for j in range(CurrentNumberOfAnswers)]
                                                # Vote Share of each answer, and record whether answer was chosen


                                                if sum(VotesPerAnswer) > 0:
                                                    VoteShare = [[j == Apos, VotesPerAnswer[j]/sum(VotesPerAnswer)] for j in range(CurrentNumberOfAnswers)]
                                                else:
                                                    VoteShare = [[j == Apos, None] for j in range(CurrentNumberOfAnswers)]          

                                                AnswersOrderedByVote = list(reversed(sorted(VotesPerAnswer)))

                                                VoteOrder = [[j == Apos, AnswersOrderedByVote.index(VotesPerAnswer[j])] for j in range(CurrentNumberOfAnswers)]
                                                #print(VoteOrder)
                                                # if some answers have the same vote
                                                if len(VotesPerAnswer[:CurrentNumberOfAnswers]) != len(set(VotesPerAnswer[:CurrentNumberOfAnswers])):
                                                    VoteOrder = []
                                                    for j in range(CurrentNumberOfAnswers):
                                                        AllIndices = [i for i,x in enumerate(AnswersOrderedByVote) if x == VotesPerAnswer[j]]
                                                        MeanIndices = sum(AllIndices)/len(AllIndices)
                                                        VoteOrder.append([j == Apos, MeanIndices])
 

                                                #if we look at votes AFTER acceptance, answer is accepted and vote order is not "None"
                                                if VOTES_ACCEPT_ANSWER == 1 and (not AnswerNotAcceptedYet):

                                                    #pos between 0 and Current # of Answers - 1
                                                    if AcceptedAnswer < CurrentNumberOfAnswers:
                                                        if VoteOrder[AcceptedAnswer][1] != None:
                                                            #Accepted answers are ordered first UNLESS Qid == Answer Uid (equivalent to ordered with a high vote)
                                                            #if the accepted answer isn't listed first
 

                                                            VotesPerAnswer2 = [VotesPerAnswer[j] for j in range(CurrentNumberOfAnswers)]
                                                            VotesPerAnswer2[AcceptedAnswer] = 999999999999
                                                            AnswersOrderedByVote2 = list(reversed(sorted(VotesPerAnswer2)))
 
                                                            VoteOrder = [[j == Apos, AnswersOrderedByVote2.index(VotesPerAnswer2[j])] for j in range(CurrentNumberOfAnswers)]
                                                            # if some answers have the same vote
                                                            if len(VotesPerAnswer2[:CurrentNumberOfAnswers]) != len(set(VotesPerAnswer2[:CurrentNumberOfAnswers])):
                                                                VoteOrder = []
                                                                for j in range(CurrentNumberOfAnswers):
                                                                    AllIndices = [i for i,x in enumerate(AnswersOrderedByVote2) if x == VotesPerAnswer2[j]]
                                                                    MeanIndices = sum(AllIndices)/len(AllIndices)
                                                                    VoteOrder.append([j == Apos, MeanIndices])
                                                    else:
                                                            VoteOrder = [[j == Apos, None] for j in range(CurrentNumberOfAnswers)]
        

                                                # chronological order (oldest to newest) and record of whether answer was chosen

                                                ChronologicalOrder = [[j == Apos, Aid.index(Aid[j])] for j in range(CurrentNumberOfAnswers)]

                                                TimeSinceAnswer= [[j == Apos, (v[3] - Ta[j])/86400] for j in range(CurrentNumberOfAnswers)]                                                

                                                VoteAgePerAnswer= [[j == Apos, v[3]] for j in range(CurrentNumberOfAnswers)]
                                                
                                                WordsPerAnswer = [[j == Apos, NumWords[j]] for j in range(CurrentNumberOfAnswers)]
                                                WordSharePerAnswer = [[j == Apos, WordShare[j]] for j in range(CurrentNumberOfAnswers)]
                                                TotalNumWordsPerAnswer = [[j == Apos, TotalNumWords] for j in range(CurrentNumberOfAnswers)]
                                                #print(WordSharePerAnswer)
                                                NumLinksPerAnswer = [[j == Apos, NumLinks[j]] for j in range(CurrentNumberOfAnswers)]

                                                ReadabilityScorePerAnswer = [[j == Apos, ReadabilityScore[j]] for j in range(CurrentNumberOfAnswers)]

                                                ReputationPerAnswer = [[j == Apos, Reputation[j]] for j in range(CurrentNumberOfAnswers)]

                                                VoteUid = Uid[Apos]
                                                Vid = v[0]
                                                #We are ignoring this data because it can be highly correlated with Reputation at answer
                                                #and it's motivation may be less clear than the reputation at the moment an answer is created
                                                ReputationsAtVote = [None for j in range(CurrentNumberOfAnswers)]#FindReputationAtVote(RDataBoardName,Uid,VoteUid,Vid)
                                                ReputationsAtVotePerAnswer = [[j == Apos, ReputationsAtVote[j]] for j in range(CurrentNumberOfAnswers)]

                                                # Age of each answerer
                                                AnswererAgePerAnswer = [[j == Apos, DaysSinceSignUp[j]] for j in range(CurrentNumberOfAnswers)]

                                                # Mean rate that reputation increases per answerer
                                                MeanRepRatePerAnswer = [[j == Apos, MeanRepRate[j]] for j in range(CurrentNumberOfAnswers)]

                                                # Whether or not the answer was eventually accepted
                                                AcceptedAnswerVoted = [[j == Apos, int(j==AcceptedAnswer)] for j in range(CurrentNumberOfAnswers)]


                                                # update the number of votes per answer *after* we record data visible to voter

                                                VotesPerAnswer[Apos] = VotesPerAnswer[Apos] + UpVote

                                                if (AnswerNotAcceptedYet and VOTES_ACCEPT_ANSWER == -1) or ((not AnswerNotAcceptedYet) and VOTES_ACCEPT_ANSWER >= 0):
                                                    #if we wait until after an answer is accepted, we ignore the data for the accepted answer (v[2] == 1)
                                                    if VOTES_ACCEPT_ANSWER != 1 or (VOTES_ACCEPT_ANSWER == 1 and v[2] != 1): 
                                                        if CurrentNumberOfAnswers > 1 and min(Ta)-(1230768000 -1199145600) - 18316800 > 0:
                                                            #                                    -(Jan. 1,2009-Jan.1,2008) - (Aug. 1 - Jan. 1, 2009)
                                                            VotePBoardName.append([CurrentNumberOfAnswers,
                                                            Votes,
                                                            VoteShare,
                                                            VoteOrder,
                                                            ChronologicalOrder,
                                                            TimeSinceAnswer,
                                                            WordsPerAnswer,
                                                            WordSharePerAnswer,
                                                            ReputationPerAnswer,
                                                            ReputationsAtVotePerAnswer,
                                                            MeanRepRatePerAnswer,
                                                            ReadabilityScorePerAnswer,
                                                            AnswererAgePerAnswer,
                                                            NumLinksPerAnswer,
                                                            AcceptedAnswerVoted,
                                                            TotalNumWordsPerAnswer,
                                                            VoteAgePerAnswer # Tv, time since Jan. 1, 2008
                                                            ])

                                                    # if we only look at the accepted answer, ignore all other data
                                                    if  VOTES_ACCEPT_ANSWER == 0: break
                            if  VOTES_ACCEPT_ANSWER == 0 and not AnswerNotAcceptedYet: break
        

    return VotePBoardName

    
def Load(file):
    s = open(file,"r")
    print(file)
    if "NoAcceptedAnswers_NonTech" in file or "NoAcceptedAnswers_Tech" in file:
        Data = s.readline().split("[], [], [], [], [], [], [], [], [], []], ")#Split by board

        for index in range(1,len(Data)-1):
            Data[index] = ast.literal_eval(Data[index] + "[], [], [], [], [], [], [], [], [], []]")

        Data[0] = ast.literal_eval(Data[0] + "[], [], [], [], [], [], [], [], [], []]]")[0]
        Data[-1] = ast.literal_eval("[" + Data[-1])[0]

    elif "NoAcceptedAnswers_SO" in file:
        DataString = s.readline()
        Data = ast.literal_eval(DataString)
        DataString = []
        #print([len(val) for val in Data[0]])
    elif "AcceptedAnswers_SO" in file:   
        breakstring="";
        DataString = s.readline()
        # removing spare '[...]'
        DataString = DataString[1:-1]
        #split in the following way:
        #read '[': leftbracket = leftbracket + 1
        #read ']': rightbracket = rightbracket + 1
        # (ignore first '[')
        # when leftbracket - rightbracket = 0, we have found the end of the character for numans = XX
        # record pos,
        # find next leftbracket: leftbracket = 1, rightbracket = 0
        # split by positions
        NumAnsPos = []
        NumAns = 0
        leftbracket = 0
        rightbracket = 0
        CharCount = 0
        #print(len(DataString))
        for char in DataString[1:-1]:
            CharCount = CharCount + 1
            if char == '[': leftbracket = leftbracket + 1
            elif char == ']': rightbracket = rightbracket + 1
            if leftbracket - rightbracket == 0 and leftbracket > 0:
                NumAnsPos.append(CharCount) # '[...]'
                NumAns = NumAns + 1
                leftbracket = 0
                rightbracket = 0
                #print(NumAns)
                #print(CharCount)

        PrevIndex = 1
        Data = [[] for i in range(NumAns)]

        for index in range(SONumAns-1,SONumAns): #range(NumAns):#
            #NumAnsData = DataString[PrevIndex:NumAnsPos[index] + 1]
            PrevIndex = NumAnsPos[index - 1] + 3
            DataPos = [PrevIndex,NumAnsPos[index] + 1]
            Data[index] = ast.literal_eval(''.join(DataString[DataPos[0]:DataPos[1]]))
        Data = [Data]
        DataString = []
    else:
        Data = s.readline().split(", [[], [[[")#Split by board
        for index in range(1,len(Data)-1):
            Data[index] = ast.literal_eval("[[], [[[" + Data[index])

        Data[0] = ast.literal_eval(Data[0]+ "]")[0]
        Data[-1] = ast.literal_eval("[[[], [[[" + Data[-1])[0]

    s.close()

    print("Votes Over Time Parsed")

    if "_SO" not in file:
        for BoardNameIndex in range(len(Data)):
            for TotalNumberOfAnswers in range(1,len(Data[BoardNameIndex])+1):
                if len(Data[BoardNameIndex][TotalNumberOfAnswers - 1]) > 0:
                     for thread in range(len(Data[BoardNameIndex][TotalNumberOfAnswers - 1])):
                         if len(Data[BoardNameIndex][TotalNumberOfAnswers - 1][thread]) > 0:
                             for CurrentNumberOfAnswers in range(1, len(Data[BoardNameIndex][TotalNumberOfAnswers - 1][thread])+1):
                                 # if votes are made
                                 if len(Data[BoardNameIndex][TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1]) > 0:
                                    for v in range(len(Data[BoardNameIndex][TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1])):
                                        Vote = Data[BoardNameIndex][TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1][v]
                                        Vote = [float(i) for i in Vote]
                                        Data[BoardNameIndex][TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1][v] = Vote

    return Data


def Make_Vote_Data_List (data):
    ConvertedData = [[] for i in range(2,41)]
    for BoardNameIndex in range(len(data)):
        for sublist in data[BoardNameIndex]:
            #ignore any sublist with missing data
            if "None" not in sublist and None not in sublist:
                NumAns = sublist[0]
                line = sublist[1:]
                for j in range(NumAns):
                    # new_lines = [T/F, [val1, val2, val3,...]]
                    new_line = [[str(line[0][j][0])],[str(line[k][j][1]) for k in range(len(line))]]
                    # flatten list
                    new_line = [item for sublist in new_line for item in sublist]
                    if NumAns <= 40:
                        ConvertedData[NumAns - 2].append(new_line)
            #else: print(sublist)
    return ConvertedData

def Make_Binned (list,bin_width):
    #make binned values such that P(x < X_i) = bin_width * i
    # make sure bins are appropriate
    #print(len(list))
    if bin_width < 1/len(list): bin_width = 1/len(list)
    # sort the list
    sorted_list = sorted(list)
    # max values within each bin
    binned_list = [sorted_list[round(round(len(sorted_list) * bin_width * i,1)) - 1] for i in range(1,round(1/bin_width)+1)]
    return binned_list

def ConvertToLogitForm(data):

    # Votes Data To Normalize: 
    #              Votes (divide by current number of answers, so we do not over-count)
    #              TimeSinceAnswer,

    # AData To Normalize: 
    #              WordsPerAnswer,
    #              ReputationPerAnswer,
    #              MeanRepRatePerAnswer,
    #              ReadabilityScorePerAnswer,
    #              AnswererAgePerAnswer,
    #              NumLinksPerAnswer,


    #data is a list in the old form,
    #First, we want to seperate out "2" answers from "3", etc.
    data = Make_Vote_Data_List(data)

    directory = '/export/data/ccbdata/keith/Local Stack Exchange Data/Files/'
    CDF_file = directory + "Parsed Data/VoteP_Normalized_CDF_Training.p"
    CDF_List = pickle.load(open(CDF_file,'rb'))
    bin_width = 0.001

    print("Normalizing values for number of answers equal to...")

    for NumAns in range(2,41):
        print(NumAns)
        if len(data[NumAns - 2]) > 0:

            #Non-uniform distribution normalization
            #Uniform distributions must by normalized
            #
            # [3]  VoteOrder          (/Max)
            # [4]  ChronologicalOrder (/Max)
            # 
            # Otherwise, if they are not between 0 and 1, they are normalized by their CDF

            data[NumAns - 2] = [	[line[0],
                                          str(CDF(binary_search,CDF_List['VotesPerAnswer'],float(line[1]),bin_width)),               # number of votes
                                          str(CDF(binary_search,CDF_List['VoteSharePerAnswer'],float(line[2]),bin_width)),               # vote share
                                          str(float(line[3])/NumAns),                                                                # vote order
                                          str(float(line[4])/NumAns),                                                                # chronological order
                                          str(CDF(binary_search,CDF_List['TimeSinceAnswer'],float(line[5]),bin_width)),              # seconds after answer created
                                          str(CDF(binary_search,CDF_List['WordsPerAnswer'],float(line[6]),bin_width)),               # words per answer
                                          str(CDF(binary_search,CDF_List['WordSharePerAnswer'],float(line[7]),bin_width)),               # word share per answer
                                          str(CDF(binary_search,CDF_List['ReputationPerAnswer'],float(line[8]),bin_width)),          # Reputation at answer creation
                                          line[9],                                                                                   # ReputationPerVote: we ignore this value                    
                                          str(CDF(binary_search,CDF_List['MeanRepRatePerAnswer'],float(line[10]),bin_width)),        # reputation/days since signup
                                          str(CDF(binary_search,CDF_List['ReadabilityScorePerAnswer'],float(line[11]),bin_width)),   # Flech readability score
                                          str(CDF(binary_search,CDF_List['AnswererAgePerAnswer'],float(line[12]),bin_width)),        # days since signup
                                          str(CDF(binary_search,CDF_List['NumLinksPerAnswer'],float(line[13]),bin_width)),           # number of links
                                          str(float(line[14])),                                                                      # Was answer accepted?
                                          str(float(line[16]))                                                                       # Tv, since since Jan. 1, 2008
                                          ] for line in data[NumAns - 2] if 'None' not in line[:9] and 'None' not in line[10:] and float(line[3])/NumAns < 1.0]

    return data

def Export(data,file):

    for i in range(len(data)):
        #assume file ends in .csv
        if file[-4:]==".csv" or file[-4:]==".dat":
            NumAnsFile = file[0:-4] + "_" + str(i+2) + file[-4:]
        else:
            print("CANNOT UNDERSTAND CURRENT FILE FORMAT")
            exit()
        f = open(NumAnsFile,"w")

        f.write("PickAnswer?,Votes,VoteShare,VoteOrder,ChronologicalOrder,TimeSinceAnswer,WordsPerAnswer,WordSharePerAnswer,ReputationPerAnswer,ReputationsAtVotePerAnswer,MeanRepRatePerAnswer,ReadabilityScorePerAnswer,AnswererAgePerAnswer,NumLinksPerAnswer,AcceptedAnswer?,VoteAge\n")
        #sort by the number of words
        for line in data[i]:
            #if "None" does not appear in the file (aside from "reputation per vote")
            if 'None' not in line[:9] and 'None' not in line[10:]:
                for words in line[:-1]:
                    if file[-4:] == ".csv":
                        f.write(words + ",")
                    else:
                        f.write(words + "   ")
                #final word has no comma
                f.write(line[-1] + "\n")
        f.close()




#==============================================================================
# MAIN.
#==============================================================================
def main():
    

    directory = '/export/data/ccbdata/keith/Local Stack Exchange Data/Files/'

    #List all boards to parse

    board = ["academia", "academiameta", "android", "androidmeta","anime", "animemeta", "apple", "applemeta", "arduino","arduinometa", "askubuntumeta", "astronomy", "astronomymeta","aviation", "aviationmeta", "avp", "avpmeta", "beer", "beermeta","bicycles", "bicyclesmeta", "biology", "biologymeta","bitcoin","bitcoinmeta", "blender", "blendermeta", "boardgames","boardgamesmeta", "bricks", "bricksmeta", "buddhism","buddhismmeta", "chemistry", "chemistrymeta", "chess","chessmeta","chinese", "chinesemeta", "christianity", "christianitymeta","codegolf", "codegolfmeta", "codereview", "codereviewmeta","cogsci", "cogscimeta", "comaskubuntu", "comserverfault","comstackapps", "comsuperuser", "cooking", "cookingmeta","craftcms", "craftcmsmeta", "crypto", "cryptometa", "cs","csmeta","cstheory", "cstheorymeta", "datascience", "datasciencemeta","dba", "dbameta", "diy", "diymeta", "drupal", "drupalmeta","dsp","dspmeta", "earthscience", "earthsciencemeta", "ebooks","ebooksmeta", "electronics", "electronicsmeta", "ell", "ellmeta","english", "englishmeta", "expatriates", "expatriatesmeta","expressionengine", "expressionenginemeta", "fitness","fitnessmeta", "freelancing", "freelancingmeta", "french","frenchmeta", "gamedev", "gamedevmeta", "gaming", "gamingmeta","gardening", "gardeningmeta", "genealogy", "genealogymeta","german", "germanmeta", "gis", "gismeta", "graphicdesign","graphicdesignmeta", "ham", "hammeta", "hermeneutics","hermeneuticsmeta", "hinduism", "hinduismmeta", "history","historymeta", "homebrew", "homebrewmeta", "islam","islammeta", "italian", "italianmeta", "japanese","japanesemeta", "joomla", "joomlameta", "judaism", "judaismmeta","linguistics", "linguisticsmeta", "magento", "magentometa","martialarts", "martialartsmeta", "Math", "matheducators","matheducatorsmeta", "mathematica", "mathematicameta","mathmeta","mathoverflowmeta", "mechanics", "mechanicsmeta", "meta","moderators", "moderatorsmeta", "money", "moneymeta", "movies","moviesmeta", "music", "musicmeta", "netmathoverflow","networkengineering", "networkengineeringmeta", "opendata","opendatameta", "outdoors", "outdoorsmeta", "parenting","parentingmeta", "patents", "patentsmeta", "pets", "petsmeta","philosophy", "philosophymeta", "photo", "photometa","physics","physicsmeta", "pm", "pmmeta", "poker", "pokermeta","politics","politicsmeta", "productivity", "productivitymeta","programmers","programmersmeta", "ptmeta", "puzzlingmeta", "quant","quantmeta","raspberrypi", "raspberrypimeta", "reverseengineering","reverseengineeringmeta", "robotics", "roboticsmeta", "rpg","rpgmeta", "russian", "russianmeta", "salesforce","salesforcemeta", "scicomp", "scicompmeta", "scifi", "scifimeta","security", "securitymeta", "serverfaultmeta", "sharepoint","sharepointmeta", "skeptics", "skepticsmeta", "softwarerecs","softwarerecsmeta", "sound", "soundmeta", "space", "spacemeta","spanish", "spanishmeta", "sports", "sportsmeta", "sqa","sqameta","stackoverflowmeta", "stackoverflowpt", "startups","startupsmeta", "stats", "statsmeta", "superusermeta","sustainability", "sustainabilitymeta", "tex", "texmeta","tor","tormeta", "travel", "travelmeta", "tridion", "tridionmeta","unix", "unixmeta", "ux", "uxmeta", "webapps", "webappsmeta","webmasters", "webmastersmeta", "windowsphone","windowsphonemeta","wordpress", "wordpressmeta", "workplace", "workplacemeta","writers", "writersmeta"]
 
    #Board types (Technical, Non-Technical, and Meta)

    TechnicalBoards = ["android", "apple", "arduino", "blender","codegolf", "codereview", "comstackapps", "comaskubuntu", "comserverfault","comsuperuser", "craftcms", "crypto", "datascience", "dba","drupal", "dsp", "ebooks", "electronics", "expressionengine","gamedev", "gis", "joomla", "magento", "mathematica","networkengineering", "opendata", "programmers", "raspberrypi","reverseengineering", "robotics", "salesforce", "security","sharepoint", "SO", "softwarerecs", "sound", "space", "sqa","stackoverflowpt", "startups", "tex", "tor", "tridion", "unix","ux", "webapps", "webmasters", "windowsphone", "wordpress"]
    LargestBoard = {}
    LargestBoard["Meta"] = "meta"
    LargestBoard["NonTech"] = "Math"
    LargestBoard["Tech"] = "SO" #Stack Overflow
    #Meta and NonTechnical Boards
    NonTechnicalBoards=[]
    MetaBoards=[]

    for string in board:
        if "meta" in string:
                MetaBoards.append(string)
        elif string not in TechnicalBoards:
                NonTechnicalBoards.append(string)

    for BoardType in ["Tech"]:#["Meta","NonTech","Tech"]:

        if BoardType == "Meta":
                Boards = MetaBoards
        elif BoardType == "NonTech":
                Boards = NonTechnicalBoards
        else: Boards = TechnicalBoards

        print(len(Boards))
        # combine Accept = T/F for BEFORE?
        for ACCEPT in [True]:#[True,False]:
            ###########################################################################
            # Are we looking at smallest boards or all boards?
            #  All boards: True, Smallest boards (all but the largest): False
            ###########################################################################
            for ALL_BOARDS in [True]:#[False,True]:

                # We ignore the SO board
                if ALL_BOARDS and BoardType == "Tech": 
                    Boards = ["SO"]
                else:
                    Boards = [BoardName for BoardName in Boards if BoardName != "SO"]

                print("BoardType: %s" %BoardType)
                print(Boards)
                print("ACCEPT: %s" %str(ACCEPT))

                ################################################################
                # Answer Data
                AData = {}

                if BoardType == "Tech" and ALL_BOARDS:
                    if ACCEPT:
                        s = open(directory + "Answer Data/Accepted Answers All Boards/AcceptedAnswers_SO.csv","r")
                    else:
                        s = open(directory + "Answer Data/No Accepted Answers All Boards/NoAcceptedAnswers_SO.csv","r")

                else:
                    if ACCEPT:
                        s = open(directory + "Answer Data/Accepted Answers All Boards/AcceptedAnswers_"+ BoardType +"_NEW.csv","r")
                    else:
                        s = open(directory + "Answer Data/No Accepted Answers All Boards/NoAcceptedAnswers_"+ BoardType +".csv","r")

                for line in s:
                    if line != '\n':
                        if line.split(",")[0] in Boards:

                                #Board Name
                                BoardName = line.split(",")[0]
                                #If AData has a board, append
                                if BoardName in AData:
                                    # split lines of CSV file by commas
                                    AData[BoardName].append(line.replace("\n","").split(","))
                                # Otherwise, AData doesn't have this board,
                                # Create a new list:
                                else:
                                    AData[BoardName] = [line.replace("\n","").split(",")]
                                # convert strings to numbers NOT Ta (answer time) or Te (edit time)
                                TaPos = 5
                                if ACCEPT:
                                    TaPos = 6
                                #Last line of AData from 1 -> TaPos - 1: Make into floating point numbers
                                AData[BoardName][-1][1:TaPos] = [float(i) for i in AData[BoardName][-1][1:TaPos]]
                                #If last element in the line isn't "\n"
                                for i in range(len(AData[BoardName][-1])):
                                    if AData[BoardName][-1][i] == '':
                                        AData[BoardName][-1][i] = '999999999999999999999999999999999'
                                AData[BoardName][-1][TaPos + 2:] = [float(i) for i in AData[BoardName][-1][TaPos + 2:]]

                                if AData[BoardName][-1][TaPos + 7] > 9999999999999999999999:
                                    # ignore unknown reputations
                                    AData[BoardName][-1][TaPos + 7] = None

                                if AData[BoardName][-1][TaPos + 8] < 1:
                                    AData[BoardName][-1][TaPos + 8] = 999999999999999999999999999999999



                                #convert date to seconds since 2008
                                # e.g., "2014-7-14 13:07.24" -> 1.231*10^8 (I made this number up)
                                split_line = AData[BoardName][-1]
                                date = split_line[TaPos].split()
                                if len(date) > 0:
                                    date[0] = date[0].split("-")
                                    date[-1] = date[-1].split(":")
                                    date = date[0] + date[1]
                                    date = [float(i) for i in date]
                                    Ta = Time(MonthToSecond,date)
                                else: Ta = None

                                if split_line[TaPos + 1] != '999999999999999999999999999999999':
                                    date = split_line[TaPos + 1].split()
                                    if len(date) > 0:
                                        date[0] = date[0].split("-")
                                        date[-1] = date[-1].split(":")
                                        date = date[0] + date[1]
                                        date = [float(i) for i in date]
                                        Tedit = Time(MonthToSecond,date)
                                    else: Tedit = None
                                else: Tedit = None
                                # put time (seconds since 2008) back into data
                                AData[BoardName][-1][TaPos] = Ta
                                AData[BoardName][-1][TaPos + 1] = Tedit


                print("AData Parsed")

                ################################################################
                # Vote Data
                if BoardType == "Tech" and ALL_BOARDS:
                    if ACCEPT:
                        VotesOverTime = Load(directory + "Parsed Data/VotesOverTimeAcceptedAnswers_SO_Python_Faster_NEW_UpdatedCode3.dat")
                    else:
                        VotesOverTime = Load(directory + "Parsed Data/VotesOverTimeNoAcceptedAnswers_SO_Python_Faster_NEW_UpdatedCode3.dat")
                else:
                    if ACCEPT:
                        VotesOverTime = Load(directory + "Parsed Data/VotesOverTimeAcceptedAnswers_" + BoardType + "_Python_Faster_NEW_UpdatedCode2.dat")
                    else:
                        VotesOverTime = Load(directory + "Parsed Data/VotesOverTimeNoAcceptedAnswers_" + BoardType + "_Python_Faster_NEW_UpdatedCode2.dat")


                ################################################################


                print("Starting VoteP")
  

                # Are we looking at votes before, during, or after acceptance?
                #
                # -1: all data BEFORE answer is accepted
                #  0: all data for accepted answer
                #  1: all data AFTER answer is accepted
                for VOTES_ACCEPT_ANSWER in [-1,0]:#[-1,0,1]:
                        #if answers never accepted, we ignore cases 0 and 1
                        if (not ACCEPT) and VOTES_ACCEPT_ANSWER >= 0: continue

                        if VOTES_ACCEPT_ANSWER == -1:
                            print("Looking at votes BEFORE answer is accepted")
                        elif VOTES_ACCEPT_ANSWER == 0:
                            print("Looking at accepted answers")
                        else:
                            print("Looking at votes AFTER answer is accepted")

                        #pool = Pool()
                        
                        if ALL_BOARDS:
                            print("Looking at ALL boards")

                            VotePBoards = list(map(ParallelWork, [[VotesOverTime[BoardNameIndex],AData[Boards[BoardNameIndex]],ACCEPT,VOTES_ACCEPT_ANSWER] for BoardNameIndex in range(len(Boards))]))
                        else:
                            print("Looking at BOTTOM boards")
                            if BoardType != "Tech":	
                                LargestBoardNameIndex = next(i for i,b in enumerate(Boards) if b == LargestBoard[BoardType])
                            else:
                                LargestBoardNameIndex = 99999
                                
                            VotePBoards = list(map(ParallelWork, [[VotesOverTime[BoardNameIndex],AData[Boards[BoardNameIndex]],ACCEPT,VOTES_ACCEPT_ANSWER] for BoardNameIndex in range(len(Boards)) if BoardNameIndex != LargestBoardNameIndex]))

                    
                        #pool.close()
                        #pool.join()

                        VotePLogitForm = ConvertToLogitForm(VotePBoards)
                        VotePBoards = []
                        
                        AcceptAnsStr=""
                        if not ACCEPT:
                            AcceptAnsStr="No"

                        AllBoardsStr=""
                        if not ALL_BOARDS:
                            AllBoardsStr = "_NoLargestBoard"
                        elif BoardType == "Tech": AllBoardsStr = "_SO"
        
                        if VOTES_ACCEPT_ANSWER == -1:
                            VoteStr = "_BeforeAnswerAccepted"
                        elif VOTES_ACCEPT_ANSWER == 0:
                            VoteStr = "_AcceptedAnswers"
                        else:
                            VoteStr = "_AfterAnswerAccepted"

                        file = directory + "Parsed Data/VoteP_" + BoardType + "_Logit_"+ AcceptAnsStr + "Accept" + VoteStr + AllBoardsStr +"_Normalized_AllDataCDF_AfterAug2009_" + str(SONumAns) + "Q_TrainedCDF.csv"

                        Export(VotePLogitForm,file)
                        VotePLogitForm = []

    print("DONE")
        
if __name__ == "__main__":
    main()

