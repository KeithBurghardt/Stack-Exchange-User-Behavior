import pyodbc as p
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import stats
import csv
from datetime import datetime
# *********** Database variables **********
from data import server
from data import database

# *********** Connection **********
from data import connStr

# *********** SQL **********
from data import datasets
#datasets = ['academia', 'cs', 'cstheory', 'diy', 'graphicdesign', 'scifi', 'workplace', 'pets', 'sound']
del datasets[9]

conn = p.connect(connStr)
c = conn.cursor()
print 'connessione creata'
sep = ''
h = 0
tech = ["android", "apple", "arduino", "blender", "codegolf", "codereview", "comaskubuntu", "comserverfault", "comstackapps", "comsuperuser", "craftcms", "crypto", "datascience", "dba", "drupal", "dsp", "ebooks", "electronics", "expressionengine", "gamedev", "gis", "joomla", "magento", "mathematica", "networkengineering", "opendata", "programmers", "raspberrypi", "reverseengineering", "robotics", "salesforce", "security", "sharepoint", "SO", "softwarerecs", "sound", "space", "sqa", "stackoverflowpt", "startups", "tex", "tor", "tridion", "unix", "ux", "webapps", "webmasters", "windowsphone", "wordpress"]
no_tech = ["academia", "anime", "astronomy", "aviation", "avp", "beer", "bicycles", "biology", "bitcoin", "boardgames", "bricks", "buddhism", "chemistry", "chess", "chinese", "christianity", "cogsci", "cooking", "cs", "cstheory", "diy", "earthscience", "ell", "english", "expatriates", "fitness", "freelancing", "french", "gaming", "gardening", "genealogy", "german", "graphicdesign", "ham", "hermeneutics", "hinduism", "history", "homebrew", "islam", "italian", "japanese", "judaism", "linguistics", "martialarts", "Math", "matheducators", "mechanics", "moderators", "money", "movies", "music", "netmathoverflow", "outdoors", "parenting", "patents", "pets", "philosophy", "photo", "physics", "pm", "poker", "politics", "productivity", "quant", "rpg", "russian", "scicomp", "scifi", "skeptics", "spanish", "sports", "stats", "sustainability", "travel", "workplace", "writers"]
reputation_answers = [0, 15, 10, -2]
reputation_questions = [0, 0, 5, -2]


with open('Reputation_Meta.csv', 'w') as csvfile:
        fieldnames = ['Board', 'AnswerId', 'QuestionId', 'AcceptedAnswerId', 'UserId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for ds in datasets:
                try:
                        b = tech.index(ds)
                        type_b = 'Tech'
                except ValueError:
                        try:
                            b = no_tech.index(ds)
                            type_b = 'No-Tech'
                        except ValueError:
                            type_b = 'Meta'

                if type_b == 'Meta':
                        c.execute('SELECT answer.Id as aId, answer.ParentId as qId, PostId as aaId, answer.OwnerUserId as Owner, question.AnswerCount as numb_answers ' +
                                  'FROM ' + ds + '.Posts as answer, ' + ds + '.Posts as question, ( ' +
                                  '     SELECT ParentId, DATEADD(day, 1, CreationDate) as CreationDate, PostId ' +
                                  '     FROM ' + ds + '.Votes WHERE VoteTypeId = 1) as vote ' +
                                  'WHERE answer.PostTypeId = 2 AND vote.ParentId = answer.ParentId AND answer.CreationDate <= vote.CreationDate AND question.Id = answer.ParentId ' +
                                  'ORDER BY answer.ParentId, answer.CreationDate')

                        aId = []
                        qId = []
                        aaId = []
                        user = []
                        rep = []
                        numb_answers = []
                        
                        for row in c:
                                aId.append(int(row.aId))
                                qId.append(int(row.qId))
                                aaId.append(int(row.aaId))
                                user.append(int(row.Owner))
                                rep.append(1)
                                numb_answers.append(int(row.numb_answers))
                        
                        c.execute('SELECT v.Id as Id, v.PostId as PostId, v.ParentId as ParentId, v.PostTypeId as PostTypeId, VoteTypeId, v.CreationDate as CreationDate, p.OwnerUserId as OwnerUserId ' +
                                  'FROM ' + ds + '.Votes as v, ' + ds + '.Posts as p ' +
                                  'WHERE v.PostId = p.Id ' +
                                  'ORDER BY v.Id')

                        userId = []
                        reputation = []
                
                        for row in c:
                                try:
                                        index = userId.index(int(row.OwnerUserId))
                                except:
                                        userId.append(int(row.OwnerUserId))
                                        reputation.append(1)
                                        index = userId.index(int(row.OwnerUserId))

                                if row.VoteTypeId == 1:
                                        for i in range (0, numb_answers[qId.index(row.ParentId)]):
                                                try:
                                                        ind = i + qId.index(row.ParentId)
                                                        rep[ind] = reputation[userId.index(user[ind])]
                                                except:
                                                        pass
                                
                                if (row.VoteTypeId == 8) or (row.VoteTypeId == 9):
                                        reputation[index] += 50 #row.BountyAmount
                                else:
                                        if row.VoteTypeId <= 3:
                                                if row.PostTypeId == 1:
                                                        reputation[index] += reputation_questions[row.VoteTypeId]
                                                else:
                                                        reputation[index] += reputation_answers[row.VoteTypeId]
                                                        
                        for i in range (0, len(aId)):
                                writer.writerow({'Board': ds, 'AnswerId': aId[i], 'QuestionId': qId[i], 'AcceptedAnswerId': aaId[i], 'UserId': user[i], 'Reputation': rep[i]})

                print ds

        conn.commit()
        c.close()
        conn.close()

# For all the voted answers
path = 'C:/Users/Ema/Documents/Ricerca/Diversity/Model/Reputation/'
board_type = 'No-Tech' # 'Meta' 'Tech' 'No-Tech'

with open('Reputation_' + board_type + '.csv', 'w') as csvfile:
        fieldnames = ['Board', 'Id', 'PostId', 'VoteTypeId', 'CreationDate', 'AnswerCreationdate', 'OwnerUserId', 'Reputation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for ds in datasets:
                try:
                        b = tech.index(ds)
                        type_b = 'Tech'
                except ValueError:
                        try:
                            b = no_tech.index(ds)
                            type_b = 'No-Tech'
                        except ValueError:
                            type_b = 'Meta'

                answerId = []
                ownerId = []
                
                if type_b == board_type:                        
                        c.execute('SELECT v.Id as Id, v.PostId as PostId, VoteTypeId, v.CreationDate as CreationDate, p.CreationDate as answCreationDate, p.OwnerUserId as OwnerUserId ' +
                                  'FROM ' + ds + '.Votes as v, ' + ds + '.Posts as p ' +
                                  'WHERE v.PostId = p.Id AND v.PostTypeId = 2 ' +
                                  'ORDER BY v.Id')

                        userId = []
                        reputation = []

                        for row in c:
                                try:
                                        index = userId.index(int(row.OwnerUserId))
                                except:
                                        userId.append(int(row.OwnerUserId))
                                        reputation.append(1)
                                        index = userId.index(int(row.OwnerUserId))
                
                                if (row.VoteTypeId == 8) or (row.VoteTypeId == 9):
                                        reputation[index] += 50 #row.BountyAmount
                                else:
                                        if row.VoteTypeId <= 3:
                                                writer.writerow({'Board': ds, 'Id': row.Id, 'PostId': row.PostId, 'VoteTypeId': row.VoteTypeId, 'CreationDate': row.CreationDate,
                                                                 'AnswerCreationdate': row.answCreationDate, 'OwnerUserId': row.OwnerUserId, 'Reputation': reputation[index]})
                                                reputation[index] += reputation_questions[row.VoteTypeId]
                print ds
        
        conn.commit()
        c.close()
        conn.close()

# add the difference between user creation date and answercreation date
path = 'C:/Users/Ema/Google Drive/Stack Exchange Data/Files/Answer Data/No Accepted Answer All Boards/'
board_type = 'No-Tech' # 'Meta' 'Tech' 'No-Tech'

with open('NoAcceptedAnswers_' + board_type + '.csv', 'w') as csvfile:
        fieldnames = ['Board' , 'Answers', 'Id', 'PostParentId', 'CreationDate', 'LastEditDate', 'Words', 'Links', 'Code_lines', 'Images', 'Readability', 'Days_from_SignUp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
                
        with open(path + 'NoAcceptedAnswers_' + board_type + '.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                previousBoard = ''
                for row in reader:
                        if previousBoard != row['Board']:
                                userCreationDate = []
                                ownerId = []
                                postId = []
                                print row['Board'] + ' started'
                                c.execute('SELECT a.Id as postId, u.Id as userId, u.CreationDate as userCreationDate ' +
                                          'FROM ' + row['Board'] + '.Users as u, ' + row['Board'] + '.Posts as a ' +
                                          'WHERE a.OwnerUserId = u.Id AND a.PostTypeId = 2')

                                for riga in c:
                                        userCreationDate.append(riga.userCreationDate)
                                        ownerId.append(riga.userId)
                                        postId.append(riga.postId)
                        try:
                                index = postId.index(int(row['Id']))
                                user = ownerId[index]
                                answerCreation = datetime.strptime(row['CreationDate'], "%Y-%m-%d %H:%M:%S.%f")
                                delta = answerCreation - userCreationDate[index]
                                daysFrom = delta.days
                                userCreationDate.pop(index)
                                ownerId.pop(index)
                                postId.pop(index)
                                
                        except:
                                daysFrom = None                     
                                
                        writer.writerow({'Board': row['Board'], 'Answers': row['Answers'], 'Id': row['Id'], 'PostParentId':row['PostParentId'],
                                         'CreationDate': row['CreationDate'], 'LastEditDate': row['LastEditDate'],
                                         'Words': row['Words'],  'Links': row['Links'],
                                         'Code_lines': row['Code_lines'], 'Images': row['Images'], 'Readability': row['Readability'], 'Days_from_SignUp': daysFrom})
                        
                        previousBoard = row['Board']                   
        conn.commit()
        c.close()
        conn.close()

# add the OwnerUserId
path = 'C:/Users/Ema/Google Drive/Stack Exchange Data/Files/Answer Data/Accepted Answers All Boards/'
board_type = 'Tech' # 'Meta' 'Tech' 'No-Tech'

with open('AcceptedAnswers_' + board_type + '.csv', 'w') as csvfile:
        fieldnames = ['Board' , 'Answers_before', 'Id', 'PostParentId', 'OwnerUserId', 'CreationDate', 'LastEditDate', 'Days_to_acceptance', 'Words',  'Links', 'Code_lines', 'Images', 'Readability', 'Days_from_SignUp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
                
        with open(path + 'AcceptedAnswers_' + board_type + '.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                previousBoard = ''
                for row in reader:
                        if previousBoard != row['Board']:
                                ownerId = []
                                postId = []
                                print row['Board'] + ' started'
                                c.execute('SELECT Id as postId, OwnerUserId ' +
                                          'FROM ' + row['Board'] + '.Posts ' +
                                          'WHERE PostTypeId = 2')

                                for riga in c:
                                        #print str(riga.userId) + ';' + str(riga.postId)
                                        ownerId.append(riga.OwnerUserId)
                                        postId.append(riga.postId)
                        #try:
                        index = postId.index(int(row['Id']))
                        user = ownerId[index]
                        #print str(postId[index]) + ';' + str(ownerId[index])
                        ownerId.pop(index)
                        postId.pop(index)
                                
                        #except:
                        #        user = 0                  
                                
                        writer.writerow({'Board': row['Board'], 'Answers_before': row['Answers_before'], 'Id': row['Id'], 'PostParentId':row['PostParentId'], 'OwnerUserId': user,
                                         'CreationDate': row['CreationDate'], 'LastEditDate': row['LastEditDate'], 'Days_to_acceptance': row['Days_to_acceptance'], 
                                         'Words': row['Words'], 'Links': row['Links'],
                                         'Code_lines': row['Code_lines'], 'Images': row['Images'], 'Readability': row['Readability'], 'Days_from_SignUp': row['Days_from_SignUp']})
                        
                        previousBoard = row['Board']                   
        conn.commit()
        c.close()
        conn.close()

# add the OwnerUserId
# Change these paths to be your own.
pathAnswers = 'C:/Users/Ema/Google Drive/Stack Exchange Data/Files/Answer Data/Accepted Answers All Boards/'
pathReputation = 'C:/Users/Ema/Google Drive/Stack Exchange Data/Files/Reputation/All the answers/'

board_type = 'Meta' # 'Meta' 'Tech' 'No-Tech'

with open('NoAcceptedAnswers_' + board_type + '.csv', 'w') as csvfile:
        fieldnames = ['Board' , 'Answers', 'Id', 'PostParentId', 'OwnerUserId', 'CreationDate', 'LastEditDate', 'Words', 'Links', 'Code_lines', 'Images', 'Readability', 'Reputation', 'Days_from_SignUp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
                
        with open(pathAnswers + 'NoAcceptedAnswers_' + board_type + '.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                        board = row['Board']
                        userId = row['OwnerUserId']
                        creation_date = datetime.strptime(row['CreationDate'], "%Y-%m-%d %H:%M:%S.%f")
                        
                        with open(pathReputation + 'Reputation_' + board_type + '.csv') as csvfile:
                                readerRep = csv.DictReader(csvfile)
                                reputation = 1
                                found = 0

                                for riga in readerRep:
                                        if row['Board'] == board:
                                                found = 1
                                                if row['OwnerUserId'] == userId:
                                                        date2 = datetime.strptime(row['CreationDate'], "%Y-%m-%d %H:%M:%S.%f")
                                                        if date < date2
                                                                reputation = row['Reputation']
                                                        else:
                                                                if date >= date2:
                                                                        break
                                        else:
                                                if found == 1:
                                                        break                
                                
                        writer.writerow({'Board': row['Board'], 'Answers': row['Answers'], 'Id': row['Id'], 'PostParentId':row['PostParentId'], 'OwnerUserId': ['OwnerUserId'],
                                         'CreationDate': row['CreationDate'], 'LastEditDate': row['LastEditDate'],
                                         'Words': row['Words'], 'Links': row['Links'],
                                         'Code_lines': row['Code_lines'], 'Images': row['Images'], 'Reputation': reputation, 'Readability': row['Readability'], 'Days_from_SignUp': row['Days_from_SignUp']})
