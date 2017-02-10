import sys;
# used to make pymysql work correctly
sys.path.insert(0, '/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages');
import pymysql as db;
import time;from datetime import date, time, datetime;
import csv;
# All boards (had to be written by rote)
boards = ["academia", "academiameta", "android", "androidmeta","anime", "animemeta", "apple", "applemeta", "arduino","arduinometa", "askubuntumeta", "astronomy",
"astronomymeta","aviation", "aviationmeta", "avp", "avpmeta", "beer", "beermeta","bicycles", "bicyclesmeta", "biology", "biologymeta","bitcoin","bitcoinmeta",
"blender", "blendermeta", "boardgames","boardgamesmeta", "bricks", "bricksmeta", "buddhism","buddhismmeta", "chemistry", "chemistrymeta", "chess","chessmeta",
"chinese", "chinesemeta", "christianity", "christianitymeta","codegolf", "codegolfmeta", "codereview", "codereviewmeta","cogsci", "cogscimeta", "comaskubuntu",
"comserverfault","comstackapps", "comsuperuser", "cooking", "cookingmeta","craftcms", "craftcmsmeta", "crypto", "cryptometa", "cs","csmeta","cstheory",
"cstheorymeta", "datascience", "datasciencemeta","dba", "dbameta", "diy", "diymeta", "drupal", "drupalmeta","dsp","dspmeta", "earthscience", "earthsciencemeta",
"ebooks","ebooksmeta", "electronics", "electronicsmeta", "ell", "ellmeta","english", "englishmeta", "expatriates", "expatriatesmeta","expressionengine",
"expressionenginemeta", "fitness","fitnessmeta", "freelancing", "freelancingmeta", "french","frenchmeta", "gamedev", "gamedevmeta", "gaming", "gamingmeta",
"gardening", "gardeningmeta", "genealogy", "genealogymeta","german", "germanmeta", "gis", "gismeta", "graphicdesign","graphicdesignmeta", "ham", "hammeta",
"hermeneutics","hermeneuticsmeta", "hinduism", "hinduismmeta", "history","historymeta", "homebrew", "homebrewmeta", "islam","islammeta", "italian", "italianmeta",
"japanese","japanesemeta", "joomla", "joomlameta", "judaism", "judaismmeta","linguistics", "linguisticsmeta", "magento", "magentometa","martialarts",
"martialartsmeta", "Math", "matheducators","matheducatorsmeta", "mathematica", "mathematicameta","mathmeta","mathoverflowmeta", "mechanics", "mechanicsmeta",
"meta","moderators", "moderatorsmeta", "money", "moneymeta", "movies","moviesmeta", "music", "musicmeta", "mathoverflow","networkengineering",
"networkengineeringmeta", "opendata","opendatameta", "outdoors", "outdoorsmeta", "parenting","parentingmeta", "patents", "patentsmeta", "pets", "petsmeta",
"philosophy", "philosophymeta", "photo", "photometa","physics","physicsmeta", "pm", "pmmeta", "poker", "pokermeta","politics","politicsmeta",
"productivity", "productivitymeta","programmers","programmersmeta", "ptmeta", "puzzlingmeta", "quant","quantmeta","raspberrypi", "raspberrypimeta",
"reverseengineering","reverseengineeringmeta", "robotics", "roboticsmeta", "rpg","rpgmeta", "russian", "russianmeta", "salesforce","salesforcemeta",
"scicomp", "scicompmeta", "scifi", "scifimeta","security", "securitymeta", "serverfaultmeta", "sharepoint","sharepointmeta", "skeptics", "skepticsmeta",
"softwarerecs","softwarerecsmeta", "sound", "soundmeta", "space", "spacemeta","spanish", "spanishmeta", "sports", "sportsmeta", "sqa","sqameta",
"stackoverflowmeta", "stackoverflowpt", "startups","startupsmeta", "stats", "statsmeta", "superusermeta","sustainability", "sustainabilitymeta",
"tex", "texmeta","tor","tormeta", "travel", "travelmeta", "tridion", "tridionmeta","unix", "unixmeta", "ux", "uxmeta", "webapps",
"webappsmeta","webmasters", "webmastersmeta", "windowsphone","windowsphonemeta","wordpress", "wordpressmeta", "workplace", "workplacemeta","writers", "writersmeta"];tech_boards=["android", "apple", "arduino", "blender","codegolf", "codereview", "comstackapps", "comaskubuntu", "comserverfault","comsuperuser", 
"craftcms", "crypto", "datascience", "dba","drupal", "dsp", "ebooks", "electronics", "expressionengine","gamedev", "gis", "joomla", "magento", "mathematica",
"networkengineering", "opendata", "programmers", "raspberrypi","reverseengineering", "robotics", "salesforce", "security","sharepoint", "SO", "softwarerecs", 
"sound", "space", "sqa","stackoverflowpt", "startups", "tex", "tor", "tridion", "unix","ux", "webapps", "webmasters", "windowsphone", "wordpress"];
non_tech_boards = [board for board in boards if "meta" not in board and board not in tech_boards];
meta_boards = [board for board in boards if "meta" in board];
#change this directory to be whatever you wish
directory = '/Users/networklab/Desktop/Reputation/';
#user, password, and port can vary
conn = db.connect(host='localhost',port=3306,user='root',passwd='open');


for board_type in ['meta','non_tech','tech']:
    with open(directory + 'Reputation_'+ board_type +'8.csv', 'w') as csvfile:
        fieldnames = ['Board', 'UserId','AnswerId', 'reputation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        exec("datasets = "+board_type + '_boards');
        for ds in datasets:# what is the data/datasets?
                print(ds)
                cur = conn.cursor()
                query = 'SELECT vote.Id as vId,'
                query = query +'question.Id as qId,'
                query = query+'answer.Id as aId,'
                query = query+'vote.PostId as vPostId,'
                query = query+'vote.VoteTypeId as VoteTypeId,'
                query = query+'vote.CreationDate as vCreationDate,'
                query = query+'vote.BountyAmount as vBountyAmount,'
                query = query+'vote.UserId as vUserId,'
                query = query+'answer.OwnerUserId as AnswererID,'
                query = query+'question.OwnerUserId as AskerID '
                query = query+'FROM '
                query = query+ds+'.Posts as answer,'
                query = query+ds+'.Posts as question,'
                query = query+ds+'.Votes as vote '
                query = query+'WHERE '
                #is an answer
                query = query+'answer.PostTypeId = 2 '
                # ...or a question
                query = query+'AND question.PostTypeId = 1 '
                # and the answers are to the specific questions, or answer Id is a fixed (arbitrary) value if no answers exist
                query = query+'AND (question.Id = answer.ParentId OR (question.AnswerCount = 0 AND question.Id = vote.PostId AND answer.Id < 10)) '
                # and votes are for given answers...
                query = query+'AND (answer.Id = vote.PostId '
                # or given questions (where we might vote for a question with no answers)
                query = query +'OR question.Id = vote.PostId) '
                #order by votes (ascending)
                query = query+'ORDER BY '
                query = query+'vote.Id  ASC'#ordered by when votes appear
                cur.execute(query)
                        
                        
                        
                        
                # Each row has the following:
                #   - aId (answer ID)
                #   - qId (question ID)
                #   - vId (vote ID)
                #   - vPostId (either an answer ID or question ID the voter voted on)
                #   - VoteTypeId (upvote, downvote, accept, flag, etc.)
                #   - vCreationDate (creation date of vote (12:00 a.m. of the day voted)
                #   - vBountyAmount (bounty amount IF AVAILABLE on bounties)
                #   - vUserId (who voted or gave the bounty)
                #   - AnswererID
                #   - AskerID
                #   - num_answers (total number of answers to a question, NOT the number visible to a given voter)
                #   - aCreationDate (creation date + time of the answer)
                #   - qCreationDate (creation date + time of the question)
                # From
                #   - board answer, question, & votes 

                # what we do not reconstruct:
                #   - Bounty/2 code (if no bounty given away)
                #   - user ID of upvoter/downvoter (usually not available)
                #   - reputation for answer accepter if user ID not given

                aId = []
                AnswererId = []
                UniqueAnswerId = []
                ADate = []
                UserReputation = []
                UserReputationToday = []
                UserReputationDate = []
                UserFlagCount = []
                        
                AnswerReputation = []
                #for row in c:
                row = cur.fetchone()
                count = 0;
                lastVId = 0;
                while row != '' and row != None:
                    # if the same Vote ID was not seen before and not None
                    if row[0] == None:
                            row[0] = 0;
                    if lastVId != row[0]:
                            
                            # all answers before October 1, 2014 (this is the only data we care about)
                            CurrentVId = row[0]
                            CurrentQId = row[1]
                            CurrentAId = row[2]
                            CurrentVPostId = row[3]
                            CurrentVoteTypeId = row[4]
                            CurrentVCreationDateTime = row[5]
                            vCreationDate = datetime.strptime(CurrentVCreationDateTime,'%Y-%m-%dT%H:%M:%S.%f').date()
                            CurrentVBountyAmount = row[6]
                            CurrentVUserId = row[7]
                            CurrentAnswererId = row[8]
                            CurrentAskerId = row[9]
                            #Currentnum_answers = row[10]
                            #CurrentACreationDateTime = row[11]
                            #CurrentAdate = datetime.strptime(row[11],'%Y-%m-%dT%H:%M:%S.%f').date();
                            #CurrentCreationDateTime = row[12]
                            #CurrentCreationDate = datetime.strptime(row[12],'%Y-%m-%dT%H:%M:%S.%f').date();
                            # N.B.:
                            #   - We continuously update the reputation for each user
                            #   - We FREEZE the reputation for each answer just before answer appears

                            # as we build up reputations, we check whether users with answers or questions voted on
                            # have had their reputation recorded before.
                            # if not, we add them to our list
                            if CurrentAnswererId not in UniqueAnswerId or CurrentAskerId not in UniqueAnswerId:
                                # if we voted on an answer
                                if CurrentVPostId == CurrentAId:
                                    UniqueAnswerId.append(CurrentAnswererId)
                                # if we voted on a question
                                elif CurrentVPostId == CurrentQId:
                                    UniqueAnswerId.append(CurrentAskerId)
                                # user's current reputation
                                UserReputation.append(1)
                                # user's reputation so far today
                                UserReputationToday.append(1)
                                # what we define as "today": the date a user voted on an answer/question
                                UserReputationDate.append(vCreationDate)
                                # this records how many answers were flagged
                                UserFlagCount.append(0)
                            # NewAnswer checks if this vote is for a new answer (in which case, we record the answerer's reputation)
                            # N.B.: it is possible other user's answers are voted on before this one.
                            # This is a compromise between reputations users might see (a social signal)
                            # and the underlying quality of a user when he or she first posts an answer. They should not diverge strongly
                            NewAnswer = False
                            # if answer not voted on previously...
                            if CurrentAId not in aId and CurrentVPostId == CurrentAId:
                                #this is a new answer
                                NewAnswer = True
                                #add answer to list of answers voted on
                                aId.append(CurrentAId)
                                #record answer's answerer, date, and current reputation
                                AnswererId.append(CurrentAnswererId)
                                #ADate.append(CurrentAdate)
                                AnswerReputation.append(UserReputation[UniqueAnswerId.index(CurrentAnswererId)])
                        
                            #the following records the baseline increases and decreases in reputation due to votes...
                            DownVoteVal = -2;
                            DownVoteAnAnswer = -1
                            DownVoteAQuestion = -1
                            # downvoting an answer had no effect past May, 2011
                            if vCreationDate > date(2011,5,1):
                                DownVoteAQuestion = 0
                            AcceptAnswerVal = 15;
                            AcceptedAnAnswerVal = 2
                            UpVoteAnswerVal = 10;
                            UpVoteQuestionVal = 5;
                            ApproveEditVal = 2;
                            FlaggedVal = -100
                            MaxRep = 200;
                            DeltaScore = 0
                            #record the ID of the user voted on for later use.
                            if CurrentVPostId == CurrentAId:
                                UserIdIndex = UniqueAnswerId.index(CurrentAnswererId)
                            else:
                                UserIdIndex = UniqueAnswerId.index(CurrentAskerId)
                            # we check whether we have voted on this user today or not
                            # (n.b., only 200 points max can be gained in a day)
                            # If not...
                            if UserReputationDate[UserIdIndex] < vCreationDate:
                                #we set the reputation gained so far today to 0
                                UserReputationToday[UserIdIndex] = 0
                                #...and set the date we record reputation to today
                                UserReputationDate[UserIdIndex] = vCreationDate
                                
                                # else ReputationSameDate is vCreationDate, CumReputationInADay is not (necessarily) 0
             
                                # for all votes on user Id BEFORE answer creation
                                # and votes on questions, answers, and bounty related to user
                           
                            if True:#vCreationDate < CurrentAdate:  # if vote was made before answer was created
                                     #voter votes on a question and asker user ID is same as answerer ID of current answer
                                     # (if vote is on a question answerer made)
                                     if (CurrentVPostId == CurrentQId):
                                            
                                            # if this is an upvote
                                            if CurrentVoteTypeId == 2:
                                                # if we have not reached max reputation in a day
                                                # the change in reputation is the basline value
                                                if UserReputationToday[UserIdIndex] < MaxRep - UpVoteAnswerVal:
                                                    DeltaScore = UpVoteAnswerVal
                                                # if we are reaching max reputation in a day
                                                # we stop once the reputation is 200
                                                else: DeltaScore = MaxRep - UserReputationToday[UserIdIndex] #possibly greater than 0
                                            # if downvote 
                                            if CurrentVoteTypeId == 3:
                                                DeltaScore = DownVoteVal
  
                                     # else if a voter votes on an answer
                                     elif CurrentVPostId == CurrentAId:
                                            #if answer accepted 
                                            if CurrentVoteTypeId == 1:
                                                # if reputation in a day <= 200
                                                if UserReputationToday[UserIdIndex] < MaxRep - AcceptAnswerVal:
                                                    DeltaScore = AcceptAnswerVal
                                                # else max out at 200
                                                else: DeltaScore = MaxRep - UserReputationToday[UserIdIndex]#possibly greater than 0
                                            #if upvote 
                                            if CurrentVoteTypeId == 2:
                                                # if reputation in a day <= 200
                                                if UserReputationToday[UserIdIndex] < MaxRep - UpVoteQuestionVal:
                                                    DeltaScore = UpVoteQuestionVal
                                                # else max out at 200
                                                else: DeltaScore = MaxRep - UserReputationToday[UserIdIndex] #possibly greater than 0
                                            # if downvote 
                                            if CurrentVoteTypeId == 3:
                                                DeltaScore = DownVoteVal
                                     # else if a voter accepts an answer, they gain reputation
                                     elif (CurrentVoteTypeId == 1):
                                         # if reputation in a day is <= 200
                                         if UserReputationToday[UserIdIndex] < MaxRep - AcceptedAnAnswerVal:
                                             DeltaScore = AcceptedAnAnswerVal
                                         # else reputation in a day -> 200
                                         else: DeltaScore = MaxRep - UserReputationToday[UserIdIndex]#possibly greater than 0
             
                                     # current answerer ID previously downvoted an answer or question
                                     elif (CurrentVoteTypeId== 3):
                                         # if answer was downvoted
                                         if (CurrentVPostId == CurrentAId):
                                             #if reputation[UniqueaIdIndex] > DownVoteAnAnswer:
                                             DeltaScore = DownVoteAnAnswer

                                         # if qyestion was downvoted
                                         elif (CurrentVPostId == CurrentQId):
                                             #if reputation[UniqueaIdIndex] > DownVoteAQuestion:
                                             DeltaScore = DownVoteAQuestion

             
                                     # bounty, flag, or approval of user
                                     elif True:#(vUserId[row_num] == AnswererId[aId.index(UniqueaId)]):
                                         # flagged
                                         if CurrentVoteTypeId in [4,12]:
                                             #count flags for each user up until that time
                                             UserFlagCount[UserIdIndex] = UserFlagCount[UserIdIndex] + 1
                                             if UserFlagCount[UserIdIndex] == 6:
                                                 #if reputation[UniqueaIdIndex] > FlaggedVal:
                                                 DeltaScore = FlaggedVal
                                                 #else:
                                                 #reputation[UniqueaIdIndex] = 1;
                                         # if user who wrote answer offered bounty 
                                         elif CurrentVoteTypeId == 8:
                                                 DeltaScore = -50
                                                 if CurrentVBountyAmount is not None:
                                                     DeltaScore = -CurrentVBountyAmount
                                         # if user who wrote answer gets bounty
                                         elif CurrentVoteTypeId == 9:
                                                 DeltaScore = 50
                                                 if CurrentVBountyAmount is not None:
                                                     DeltaScore = CurrentVBountyAmount
                                         # approval of edit
                                         elif CurrentVoteTypeId== 16:                                            
                                                #if we have not reached max daily reputation
                                                if UserReputationToday[UserIdIndex] < MaxRep - ApproveEditVal:
                                                    DeltaScore = ApproveEditVal
                                                # else if we reached maximum daily reputation
                                                else: DeltaScore = MaxRep - UserReputationToday[UserIdIndex] #possibly greater than 0
                                     # if reputation were to dip below 1, we fix the reputation to be 1
                                     if UserReputation[UserIdIndex] + DeltaScore <= 0:
                                        DeltaScore = 1 - UserReputation[UserIdIndex]
                                     #cumulative reputation is upto 200 points in a day (but no greater)
                                     UserReputationToday[UserIdIndex] = UserReputationToday[UserIdIndex] + DeltaScore
                                     # add the reputation
                                     UserReputation[UserIdIndex] = UserReputation[UserIdIndex] + DeltaScore
                                     # write: ['Board', 'AnswererId', 'UserId','reputation'] as csv
                            #if answer was not voted on before
                            if NewAnswer == True:
                                if UniqueAnswerId[UserIdIndex] != None:
                                    DataStr=[ds,str(UniqueAnswerId[UserIdIndex]),str(CurrentAId),str(AnswerReputation[-1])]
                                #if we do not know who wrote the answer, then we do not know the reputation
                                else:
                                    DataStr=[ds,str(UniqueAnswerId[UserIdIndex]),str(CurrentAId),str(None)]
                                #print(str(DataStr))
                                w = writer.writerow({'Board': DataStr[0], 'UserId': DataStr[1],'AnswerId': DataStr[2],'reputation': DataStr[3]})
                            
                            #count number of lines
                            count = count + 1;
                    # last Vote ID seen
                    lastVId = CurrentVId;
                    # next row
                    row = cur.fetchone()
                cur.close()                            
                            

conn.close()
