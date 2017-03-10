import ast
import functools
from multiprocessing import Pool
import math
from bisect import bisect_left
import pickle
import itertools

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



def VotesOverTimeLists(VotesOverTimeADataAcceptDataNames):

    VotesOverTimeBoardName,ADataBoardName,ACCEPT,DataNames = VotesOverTimeADataAcceptDataNames
    #print the board name
    print(ADataBoardName[0][0])
    Distributions = {}

    CDF_List = {}
    CDF_List['VotesPerAnswer'] = []
    CDF_List['VoteSharePerAnswer'] = []
    CDF_List['WordSharePerAnswer'] = []
    CDF_List['TimeSinceAnswer'] = []
    print("Parsing AData")
    ADataNumAnsPos = [[] for i in range(1,len(VotesOverTimeBoardName))]
    #print("len(ADataNumAnsPos)")
    #print(len(ADataNumAnsPos))
    for lineAnswerIndex in range(len(ADataBoardName)):
        Num = int(ADataBoardName[lineAnswerIndex][1]);
        if Num > 199 or Num < 2: continue
        #if ADataNumAnsPos[Num-2] == []:
        print(Num)
        ADataNumAnsPos[Num-2].append(lineAnswerIndex)
        #record the last position where NumAns is oberved
        #else: ADataNumAnsPos[Num-2][1] = lineAnswerIndex
    #parallelize?
    print("Parsing VotesOverTime")
    for TotalNumberOfAnswers in range(2,len(VotesOverTimeBoardName) + 1): #1, 2, 3, 4, ...
        print("Total Number Of Answers = %s" %str(TotalNumberOfAnswers))

        if len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1]) == 0: continue 

        Qids = []
        PrevQid = 0
        thread = 0
        indices = ADataNumAnsPos[TotalNumberOfAnswers-2]
        if len(indices) > 0:
            for lineAnswerIndex in indices:#range(indices[0],indices[1]+1):
                    Qid = ADataBoardName[lineAnswerIndex][3]
                    # if this is a new question...
                    if Qid != PrevQid:
                        
                        PrevQid = Qid
                        if len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread]) == 0: continue 

                        Aid = [int(ADataBoardName[lineAnswerIndex + i][2]) for i in range(TotalNumberOfAnswers)]
                        AidSortedIndices = sorted(range(len(Aid)),key=lambda x:Aid[x])
                        Aid = sorted(Aid)

                        # User ID associated with each answer (Aid)

                        pos = 4
                        if ACCEPT:
                            pos = 5
                        # Time each answer was made
                        Ta = [ADataBoardName[lineAnswerIndex + i][pos + 1] for i in range(TotalNumberOfAnswers)]
                        pos = 7
                        if ACCEPT:
                            pos = 8
                        # Number of Words
                        NumWords = [ADataBoardName[lineAnswerIndex + i][pos] for i in range(TotalNumberOfAnswers)]
 
                        VotesPerAnswer = [0] * TotalNumberOfAnswers


                        # for the current number of answers equal to 2, 3, 4,...Total Number Of Answers
                        for CurrentNumberOfAnswers in range(1,TotalNumberOfAnswers+1):
                            
                            # Dates are seconds since Jan. 1, 2008. Change Time(), or import time 
                            # If training we normalize  using data AFTER August 1 2009
                            if min(Ta)-(1230768000 -1199145600) - 18316800 < 0: continue
                            #	    Jan. 1 2009 - Jan. 1 2008 - (August - January) 2009

                            if max(Ta[:CurrentNumberOfAnswers]) < (1388534400 - 1199145600):

                                #Record the answer share as the number of answers visible changes
                                TotalNumWords = sum([n for n in NumWords[:CurrentNumberOfAnswers]])
                                if TotalNumWords > 0:
                                    WordShare = [n/TotalNumWords for n in NumWords[:CurrentNumberOfAnswers]]
                                    for share in WordShare:
                                        CDF_List['WordSharePerAnswer'].append(share)
                                else: print(NumWords)
                                if len(VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1]) > 0:
                                    #All votes made (in chronological order) in this timeframe
                                    CurrentVote = VotesOverTimeBoardName[TotalNumberOfAnswers - 1][thread][CurrentNumberOfAnswers - 1]
                                    #print(CurrentVote)
                                    # If CurrentVote = {a,b,c,d}, then it should be {{a,b,c,d}}
                                    for v in CurrentVote:
                                        if len(v) > 2:
                                             
                                            UpVote = v[2]
                                            if UpVote == 2:
                                                UpVote = 1
                                            elif UpVote == 3:
                                                UpVote = -1
                                            else: UpVote = 0 #ignore "upvotes" for accepted answers
                                            # Which Answer was voted
                                            VoteAid = v[1]
                                            Tv = v[3]
                                            #Ta = v[4]
                                            # Dates are seconds since Jan. 1, 2008. Change Time(), or import time  
                                            # if Tv < Jan. 1 2014
                                            if Tv < (1388534400 - 1199145600):
                                                #   Jan. 1 2014 - 2008
                                                #print(Aid)
                                                #print(VoteAid)

                                                Apos = Aid.index(VoteAid)
                                                if VoteAid in Aid[:CurrentNumberOfAnswers]:    

                                                    # we make a distribution of ALL votes seen at EVERY timestep, 
                                                    # because each of these values change with a new vote       
                                                    if CurrentNumberOfAnswers > 1:
                                                    #we never use this data, so we ignore from the CDF
                                                        if sum(VotesPerAnswer) > 0: 
                                                            VoteShare = [VotesPerAnswer[j]/sum(VotesPerAnswer) for j in range(CurrentNumberOfAnswers)]
                                                            for share in VoteShare:    
                                                                CDF_List['VoteSharePerAnswer'].append(share)    
                                                            for vote in VotesPerAnswer:  
                                                                CDF_List['VotesPerAnswer'].append(vote)
                                                        for j in range(CurrentNumberOfAnswers):
                                                            CDF_List['TimeSinceAnswer'].append((Tv - Ta[j])/86400)

                                                VotesPerAnswer[Apos] = VotesPerAnswer[Apos] + UpVote

                        #we look at the next thread number 
                        thread = thread + 1

        VotesOverTimeBoardName[TotalNumberOfAnswers - 1] = []

    return CDF_List


def NormalizeList(CDF_List):

    bin_width = 0.001
    print("VotesPerAnswer")
    CDF_List["VotesPerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["VotesPerAnswer"])),bin_width)
    print("VotesSharePerAnswer")
    CDF_List["VoteSharePerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["VoteSharePerAnswer"])),bin_width)
    print("TimeSinceAnswer")
    CDF_List["TimeSinceAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["TimeSinceAnswer"])),bin_width)
    print("WordsPerAnswer")
    CDF_List["WordsPerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["WordsPerAnswer"])),bin_width)
    print("WordSharePerAnswer")
    CDF_List["WordSharePerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["WordSharePerAnswer"])),bin_width)
    print("NumLinksPerAnswer")
    CDF_List["NumLinksPerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["NumLinksPerAnswer"])),bin_width)
    print("ReadabilityScorePerAnswer")
    CDF_List["ReadabilityScorePerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["ReadabilityScorePerAnswer"])),bin_width)
    print("ReputationPerAnswer")
    CDF_List["ReputationPerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["ReputationPerAnswer"])),bin_width)
    print("AnswererAgePerAnswer")
    CDF_List["AnswererAgePerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["AnswererAgePerAnswer"])),bin_width)
    print("MeanRepRatePerAnswer")
    CDF_List["MeanRepRatePerAnswer"] = Make_Binned(list(itertools.chain(*CDF_List["MeanRepRatePerAnswer"])),bin_width)

    return CDF_List

    
def Load(file):
    s = open(file,"r")
    print("Loading %s" %file)    
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

        for index in range(NumAns):
            #NumAnsData = DataString[PrevIndex:NumAnsPos[index] + 1]
            DataPos = [PrevIndex,NumAnsPos[index] + 1]
            Data[index] = ast.literal_eval(''.join(DataString[DataPos[0]:DataPos[1]]))
            #print(len(Data[index]))

        #    ThreadPos = []
        #    Thread = 0
        #    leftbracket = 0
        #    rightbracket = 0
        #    CharCount = 0

        #    for char in DataString[DataPos[0]:DataPos[1]][1:-1]:
        #        CharCount = CharCount + 1
        #        if char == '[': leftbracket = leftbracket + 1
        #        elif char == ']': rightbracket = rightbracket + 1
        #        if leftbracket - rightbracket == 0 and leftbracket > 0:
        #            ThreadPos.append(CharCount) # '[...]'
        #            Thread = Thread + 1
        #            leftbracket = 0
        #            rightbracket = 0
        #    PrevThread = 1
        #    for threads in range(Thread):
        #        Data[index].append(ast.literal_eval(''.join(DataString[DataPos[0]:DataPos[1]][PrevThread:ThreadPos[threads] + 1])))
        #        # "+ 2" below is to ignore the characters ', ' between '[...]'
        #        PrevThread = ThreadPos[threads] + 3  
            # "+ 2" below is to ignore the characters ', ' between '[...]'
            PrevIndex = NumAnsPos[index] + 3
        Data = [Data]

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

def Make_CDF_List(AData,ACCEPT,BoardType):
    #CDFs for AData
    CDF_List = {}
    DataNames=["VotesPerAnswer","VoteSharePerAnswer","TimeSinceAnswer","WordsPerAnswer","WordSharePerAnswer","ReputationPerAnswer","MeanRepRatePerAnswer","ReadabilityScorePerAnswer","AnswererAgePerAnswer","NumLinksPerAnswer"]

    for DataName in DataNames:
        CDF_List[DataName] = []
    pos_Ta = 5
    if ACCEPT:
        pos_Ta = 6
    minTa = (1230768000 -1199145600) + 18316800 # Aug. 1, 2009
    maxTa = (1388534400 - 1199145600)           # Jan. 1, 2014
    for board in AData:
        print(board)

        pos = 7
        if ACCEPT: pos = 8
        CDF_List['WordsPerAnswer'].append([line[pos] for line in AData[board] if line[pos] < 9999999999999999 and line[pos_Ta] > minTa and line[pos_Ta] < maxTa])

        if not ACCEPT and BoardType == "Meta" or BoardType == "NonTech":
            pos = pos + 1

        CDF_List['NumLinksPerAnswer'].append([line[pos + 1] for line in AData[board] if line[pos + 1] < 9999999999999999 and line[pos_Ta] > minTa and line[pos_Ta] < maxTa])
        CDF_List['ReadabilityScorePerAnswer'].append([line[pos + 4] for line in AData[board] if line[pos + 4] < 9999999999999999 and line[pos_Ta] > minTa and line[pos_Ta] < maxTa])
        Reputation = [line[pos + 5] for line in AData[board] if line[pos + 5] is not None and line[pos_Ta] > minTa and line[pos_Ta] < maxTa]
        CDF_List['ReputationPerAnswer'].append(Reputation)
        DaysSinceSignUp = [line[pos + 6]/86400 for line in AData[board] if line[pos_Ta] > minTa and line[pos_Ta] < maxTa]
        for i,d in enumerate(DaysSinceSignUp):
            if d <= 0: DaysSinceSignUp[i] = 9999999999999999999999999
        CDF_List['AnswererAgePerAnswer'].append([days for days in DaysSinceSignUp if days < 99999])
        CDF_List['MeanRepRatePerAnswer'].append([line[pos + 5]/(line[pos + 6]/86400) for line in AData[board] if line[pos + 6] > 0 and line[pos + 5] is not None and line[pos_Ta] > minTa and line[pos_Ta] < maxTa])


    for DataName in DataNames:
        CDF_List[DataName] = list(itertools.chain(*CDF_List[DataName]))

    return CDF_List

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
                    new_line = list(itertools.chain(*new_line))
                    if NumAns <= 40:
                        ConvertedData[NumAns - 2].append(new_line)
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


#==============================================================================
# MAIN.
#==============================================================================
def main():
    

    directory = '/export/data/ccbdata/keith/Local Stack Exchange Data/Files/'

    #Names of Data to normalize

    DataNames=["VotesPerAnswer","VoteSharePerAnswer","TimeSinceAnswer","WordsPerAnswer","WordSharePerAnswer","ReputationPerAnswer","MeanRepRatePerAnswer","ReadabilityScorePerAnswer","AnswererAgePerAnswer","NumLinksPerAnswer"]
    VotePLists = {}
    for DataName in DataNames:
        VotePLists[DataName] = []

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

    for BoardType in ["Meta","NonTech","Tech"]:

        if BoardType == "Meta":
                Boards = MetaBoards
        elif BoardType == "NonTech":
                Boards = NonTechnicalBoards
        else: Boards = TechnicalBoards
        
        for ACCEPT in [False,True]:
            for PickSO in [True,False]:
                if PickSO and BoardType != "Tech": continue
                if not PickSO: Boards = [BoardName for BoardName in Boards if BoardName != "SO"]
                else: Boards = ["SO"]
                print("BoardType: %s" %BoardType)
                print(Boards)
                print("ACCEPT: %s" %str(ACCEPT))
                print("PickSO: %s" %str(PickSO))


                ################################################################
                # Answer Data
                AData = {}
                if BoardType != "Tech" or not PickSO:
                    if ACCEPT:
                        s = open(directory + "Answer Data/Accepted Answers All Boards/AcceptedAnswers_"+ BoardType +"_NEW.csv","r")
                    else:
                        s = open(directory + "Answer Data/No Accepted Answers All Boards/NoAcceptedAnswers_"+ BoardType +".csv","r")

                else:
                    if ACCEPT:
                        s = open(directory + "Answer Data/Accepted Answers All Boards/AcceptedAnswers_SO.csv","r")
                    else:
                        s = open(directory + "Answer Data/No Accepted Answers All Boards/NoAcceptedAnswers_SO.csv","r")
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

                                #if AData[BoardName][-1][TaPos + 8] < 1:
                                #    AData[BoardName][-1][TaPos + 8] = 999999999999999999999999999999999

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
                if BoardType == "Tech" and PickSO:
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


                print("Starting Normalization")
 

                #pool = Pool()
                        
                if (not PickSO) and BoardType != "Tech":
                    LargestBoardNameIndex = next(i for i,b in enumerate(Boards) if b == LargestBoard[BoardType])
                else:
                    LargestBoardNameIndex = 99999

                # Make lists for all data in AData
                CDF_List = Make_CDF_List(AData,ACCEPT,BoardType)
                for DataName in DataNames:
                    if DataName not in ['VoteSharePerAnswer','WordSharePerAnswer','VotesPerAnswer','TimeSinceAnswer']:
                        VotePLists[DataName].append(CDF_List[DataName])
     
                for BoardNameIndex in range(len(Boards)):
                    if BoardNameIndex != LargestBoardNameIndex:
                        print(len(VotesOverTime[BoardNameIndex]))
                        NewList = VotesOverTimeLists([VotesOverTime[BoardNameIndex],AData[Boards[BoardNameIndex]],ACCEPT,DataNames])
                        for DataName in ['VoteSharePerAnswer','VotesPerAnswer','WordSharePerAnswer','TimeSinceAnswer']:
                            VotePLists[DataName].append(NewList[DataName])

                #pool.close()
                #pool.join()

                #Clear Lists (may help memory issue)
                NewList = {}
                VotesOverTime = []
                AData = []
                VotePLogitForm = []
                VotePBoards = []
            


    VotePNormalized = {}
    VotePNormalizedCDF = NormalizeList(VotePLists)
    #pickle
    file = directory + "Parsed Data/VoteP_Normalized_CDF_Training.p"
    pickle.dump(VotePNormalizedCDF,open(file,"wb"))


    print("DONE")
        
if __name__ == "__main__":
    main()

