#this code needs jesus


# requirments to code> 
#C:\Users\Carol\Desktop\Rift helper\rift-explorer-master .... if it ever works


#To do 
#def didnt steal anything from here ever like never ever, innocent until proven guilty https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

#optionals
#make it more accesable
#give the code jesus


############
import json
import time
import csv
import threading
from lcu_driver import Connector
from pandas import read_csv
from numpy import array
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import getpass
import os
currentRow = [0,0,0,0,0]
#globals
rightGuess = 0
wrongGuess = 0
connector = Connector()
path = ""
model = "LR"
USER_NAME = getpass.getuser()
connected = False
lastGuess = "No guess made yet"
lastTimeSelect = False
lastTimeSelect2 = False
lastTimeSelect3 = False
lastTimeSelect4 = False
lastTimeSelect5 = False
def firstStart():
    setPath()
    fixBat()      
def setPath():
    global path
    path = os.path.dirname(os.path.realpath(__file__))+"\\"
def fixBat():
    global path
    #gets rid of installs 
    bat_path = path+"\\start.bat"
    py_path = path+"\\badGamble.py"
    with open(bat_path,"w+") as bat:
        bat.write("python "+py_path)    
def addToStartup():
    global path
    file_path = path+"start.bat"
    test = r'C:\Users\\'+ USER_NAME +"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\startLeagueRoll.bat"
    if os.path.exists(test) != True:
        bat_path = r'C:\Users\\'+ USER_NAME +"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        with open(bat_path + '\\' + "startLeagueRoll.bat", "w+") as bat_file:
            bat_file.write(r'cd '+os.path.dirname(os.path.realpath(__file__)))
            bat_file.write("\n"+r'start "New Window" cmd /c %s' % file_path)
        print("Successfully added to startup")
    else:
        print("Already added to startup")
    writeSettings()
def datasetWipe():
    with open(path+'league_dataset.csv',mode='w+') as ded:
        ded.truncate()
        ded.close()
def getGuesses():
    try:
        with open(path+'guessImGuessing.csv',mode='r') as bGS:
            csv_reader = csv.reader(bGS, delimiter=',')
            line_count = 0
            global rightGuess
            global wrongGuess
            for row in csv_reader:
                if line_count == 0:
                    rightGuess = int(row[0])
                if line_count == 1:
                    wrongGuess = int(row[0])
                line_count += 1             
    except:
        writeGuesses()
def writeGuesses():
    with open(path+'guessImGuessing.csv', mode='w') as GGS:
        writer = csv.writer(GGS)
        global rightGuess
        global wrongGuess
        writer.writerow([rightGuess])
        writer.writerow([wrongGuess])
def getSettings():
    global path
    global model
    try:
        with open(path+'badGambleSetting.csv',mode='r') as bGS:
            csv_reader = csv.reader(bGS, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    model = row[1]
                if line_count ==1:
                    path = row[1]
                line_count += 1             
    except:
        writeSettings()
def writeSettings():
    global model
    global path
    with open(path+'badGambleSetting.csv', mode='w') as bGS:
        writer = csv.writer(bGS)
        writer.writerow(['model',model])
        writer.writerow(['path',path])
def getDatabase():
    names = ['Players Analyzed','Matches Analyzed','(K/D)A/2','Total Damage','CS at 10','Win']
    return read_csv(path+'league_dataset.csv',names=names)
def predictCurrentChampSelect(modelN = "LR"):
    global model
    if modelN == "LR":
        model =LogisticRegression(solver='liblinear', multi_class='ovr')
    elif modelN == "LDA":
        model =LinearDiscriminantAnalysis()
    elif modelN == "KNN":
        model =KNeighborsClassifier()
    elif modelN == "CART":
        model =DecisionTreeClassifier()
    elif modelN == "NB":
        model =GaussianNB()
    elif modelN == "SVM":
        model =SVC(gamma='auto')
    else:
        print("Invalid model name")
    data = getDatabase()
    if data.size > 0:
        array = data.values
        X = array[:,0:5]
        y = array[:,5]
        model.fit(X,y)
        xnew = [currentRow]
        global lastguess
        lastguess = model.predict(xnew)
        lastguess = round(lastguess[0])
        if lastguess <= 0:
            print("Welp it looks like a loss to me, try and prove me wrong")
            lastguess = 0
        else:
            print("Welp looks like a win to me, try to not mess this up")
            lastguess = 1
    else:
        print("For live predictions it needs at least one example(previous game)")
    
def testMachineLearning(testsize = 0.50):
    data = getDatabase()
    sampleSize = data.size/6
    if sampleSize > 42:
        array = data.values
        X = array[:,0:5]
        y = array[:,5]
        X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=testsize, random_state=1, shuffle=True)
        models = []
        models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC(gamma='auto')))
        results = []
        names = []
        for name, model in models:
                kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
                cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
                results.append(cv_results)
                names.append(name)
                print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    else:
        print("for testing datasets you need to use portions, please have at least 50 games")
    getAnswer()
def printModels():
    print("|LR| -LogisticRegression(default)")
    print("|LDA| -LinearDiscriminantAnalysis")
    print("|KNN| -KNeighborsClassifier")
    print("|CART| -DecisionTreeClassifier")
    print("|NB| -GaussianNB")
    print("|SVM| -Support Vector Classification")
    
def addToDataset(averageRow):
    with open(path+'league_dataset.csv',mode='a') as LD:
        writer = csv.writer(LD)
        writer.writerow(averageRow)
        LD.close()

async def getAverage(connection,summoner):
    matchListHeader = await connection.request('get', '/lol-match-history/v1/products/lol/'+summoner+'/matches')
    matchList = json.loads(await matchListHeader.read())
    matchesAnalyzed = 0
    KDTotal = 0
    dmgTotal = 0
    csDiffTotal = 0
    try:
        for match in matchList['games']['games']:
            if match['gameMode'] == "CLASSIC" and match['gameType'] == "MATCHED_GAME":
                #find where they are in the match
                try:
                    K = match["participants"][0]["stats"]["kills"]
                    D = match["participants"][0]["stats"]["deaths"]
                    A = match["participants"][0]["stats"]["assists"]
                    totalDmg = match["participants"][0]["stats"]["totalDamageDealtToChampions"]
                    csDif = round(match["participants"][0]["timeline"]["csDiffPerMinDeltas"]["0-10"],2)
                    matchesAnalyzed +=1
                    if A > 0 :
                        KDTotal += round((K+(A/2))/2,2)
                    else:
                        KDTotal += round(K/D,2)
                    dmgTotal += totalDmg
                    csDiffTotal += round(csDif,2)
                except:
                    pass
                    #sometimes it just dosnt have it for some reason   
            else:
                pass
                #this is non classic (featured modes and non-rift games)
    except:
        try:
            print(match)
        except:
            print()
    if matchesAnalyzed > 0:
        KDTotal = round(KDTotal/matchesAnalyzed,2)
        dmgTotal = round(dmgTotal/matchesAnalyzed,2)
        csDiffTotal = round(csDiffTotal/matchesAnalyzed,2)
    return [matchesAnalyzed,KDTotal,dmgTotal,csDiffTotal]
async def getAverages(connection,summoners):
    playersAnalyzed = 0
    playersChecked = 0
    averages = []
    print("{:<37}{:<40}".format("PUU ID", "[Matches,KDA,DMGtoChamps,CS diff at 10]"))
    for summoner in summoners:
        playersAnalyzed+=1
        average = await getAverage(connection,summoner)
        print(str(summoner)+":"+str(average))
        averages.append(average)
    averageTotal = [0,0,0,0]
    playersChecked = playersAnalyzed
    for z in range(0,playersAnalyzed):
        if averages[z][0] == 0:
            playersChecked -= 1
    for i in range(0,playersAnalyzed):
        for j in range(0,4):
            averageTotal[j] += averages[i][j]
    if playersChecked > 1:
        for x in range(0,4):
            averageTotal[x] = round(float(averageTotal[x])/playersChecked,2)
    print()
    print("avg total:",averageTotal)
    print("player checked:",playersChecked)
    global currentRow
    currentRow[0] =playersChecked
    currentRow[1] =averageTotal[0]
    currentRow[2] =averageTotal[1]
    currentRow[3] =averageTotal[2]
    currentRow[4] =averageTotal[3]
    print("fed to machine learning:",currentRow)
    predictCurrentChampSelect()
async def getSummonerPuuIDS(connection,sumIDS):
    summoners = []
    for id in sumIDS:
        id = str(id)
        idHeader = await connection.request('get', '/lol-summoner/v1/summoners/'+id)
        idInfo = json.loads(await idHeader.read())
        summoners.append(idInfo["puuid"])
    await getAverages(connection,summoners)
        
async def getChampSelect(connection):
    global lastTimeSelect
    global lastTimeSelect2
    global lastTimeSelect3
    global lastTimeSelect4
    global lastTimeSelect5
    champSelect = await connection.request('get', '/lol-champ-select/v1/session')
    if champSelect.status != 200:
        pass
    else:
        #is in champselect
        test = json.loads(await champSelect.read())
        try:
            secPlayer = test["myTeam"][1]['summonerId']
        except:
            secPlayer = ""
        try:
            thirdPlayer = test["myTeam"][2]['summonerId']
        except:
            thirdPlayer = ""
        try:
            fourthPlayer = test["myTeam"][3]['summonerId']
        except:
            fourthPlayer = ""
        try:
            fifthPlayer = test["myTeam"][4]['summonerId']
        except:
            fifthPlayer = ""
        if test["myTeam"][0]['summonerId'] != lastTimeSelect and secPlayer != lastTimeSelect2 and thirdPlayer != lastTimeSelect3 and fourthPlayer != lastTimeSelect4 and fifthPlayer != lastTimeSelect5:
            print()
            print("Champ Select Entered")
            print("---------------------------")
            lastTimeSelect = test["myTeam"][0]['summonerId']
            lastTimeSelect2 = secPlayer
            lastTimeSelect3 = thirdPlayer
            lastTimeSelect4 = fourthPlayer
            lastTimeSelect5 = fifthPlayer
            sumIDS = []
            for player in test['myTeam']:
                sumIDS.append(player["summonerId"])
            await getSummonerPuuIDS(connection,sumIDS)
        else:
            pass
def importDataset():
    combinedList = []
    route = input("Path to file:")
    with open(path+'league_dataset.csv',mode='r') as new:
        csv_reader = csv.reader(new, delimiter=',')
        for row in csv_reader:
            combinedList.append(row)
    try:
        with open(route,mode='r') as old:
            csv_reader = csv.reader(old, delimiter=',')
            newAdditions = 0
            for row in csv_reader:
                if combinedList.count(row) == 0:
                    newAdditions +=1
                    combinedList.append(row)
        with open(path+'league_dataset.csv',mode='w') as LD:
                csvWriter = csv.writer(LD)
                for row in combinedList:
                    csvWriter.writerow(row)
        print("Import Complete: "+str(newAdditions)+" new addition(s)")
    except Exception as e:
        print("error well importing: " + str(e))
async def getEndGame(connection):
    end = await connection.request('get', '/lol-pre-end-of-game/v1/currentSequenceEvent')
    end = json.loads(await end.read())
    global rightGuess
    global wrongGuess
    global lastTimeSelect
    global lastTimeSelect2
    global lastTimeSelect3
    global lastTimeSelect4
    global lastTimeSelect5
    lastTimeSelect = False
    lastTimeSelect2 = False
    lastTimeSelect3 = False
    lastTimeSelect4 = False
    lastTimeSelect5 = False
    if end['priority'] == 3:
        print()
        print("End Game Entered")
        print("---------------------------")
        endInfo = await connection.request('get', '/lol-end-of-game/v1/eog-stats-block')
        endInfo = json.loads(await endInfo.read())
        currentTeam = 0
        win = 0
        if endInfo['teams'][0]['isPlayerTeam']:
            currentTeam = 0
        else:
            currentTeam = 1
        if endInfo['teams'][currentTeam]['isWinningTeam']:
            win = 1
        global currentRow
        log = currentRow.copy()
        log.append(win)
        if endInfo['gameMode'] == 'CLASSIC':
            if getDatabase().size > 0:
                if lastguess == win:
                    print("I told you so(correct guess)")
                    rightGuess +=1
                else:
                    print("Well you proved me wrong(incorrect guess)")
                    wrongGuess +=1
            addToDataset(log)
            writeGuesses()
        else:
            print("not a regular game: ",endInfo['gameMode'])
            print("not added to database and not guess checked")


def printIntro():
    print("before anything make sure to fully read the README file that was included in the folder            ")
    print("for this application to work have it run in the background to take test samples of live games        ")
    print("this application will provide live guesses in champ select and have some database exploring options")
    print("please note that machine learning programs up to a thousand of attempts to learn to walk efficiently   ")
def printMenu():
    print("COMMANDS:")
    print("|auto|- let the code do the stuff and stop the interaction with the code")
    print("|last guess|- shows the last update guess (0 = Lose) (1 = Win)")
    print("|last lobby|- shows the last update of lobby average (0,0,0,0 if no lobby entered since run)")
    print("|display guess| - will give you the amount of wrong and right + accuracy")
    print("|connection|- will tell you whether you are connected to league of legends")
    print("|display menu|- will print this menu")
    print("|dataset options|- print dataset options")
    print("|test| - will run multiple models against your database as partialy a test set(need min 42 datasetLength)")
    print("|manually set model|(to a hopefully more accurate model after viewing(testMachineLearning)")
    print("|display crappy intro| - lots of words removed from everytime you loaded this up")
    print("|run at start| - adds it to the start up folder so you dont have to start it every time your computer boots")
    getAnswer()
    
def setModel(modelN):
    global model
    if modelN == "LR":
        model = modelN
    elif modelN == "LDA":
        model = modelN 
    elif modelN == "KNN":
        model = modelN
    elif modelN == "CART":
        model = modelN
    elif modelN == "NB":
        model = modelN
    elif modelN == "SVM":
        model = modelN 
    else:
        print("Invalid model name")
    writeSettings()
    getAnswer()
def getAnswer():
    global lastGuess
    global currentRow
    print()
    data = getDatabase()
    answer = input("Command:")
    if answer == "display menu":
        printMenu()
    elif answer == "dataset options":
        print("|dataset wipe|- remove all entries in the dataset(remember that machine learning get more precise with more games)")
        print("|dataset length| - will see how many rows there are in the dataset")
        print("|dataset view|- will print out the entrie dataset")
        print("|dataset import|- give the exact path to another csv dataset to add new games from")
        getAnswer()
    elif answer == "connection":
        global connected
        if connected == True:
            print("you are connected")
        else:
            print("you are not connected")
        getAnswer()
    elif answer == "last guess":
        print(lastGuess)
        getAnswer()
    elif answer == "last lobby":
        print(currentRow)
        getAnswer()
    elif answer == "dataset length":
        print(round(data.size/6))
        getAnswer()
    elif answer == "dataset import":
        importDataset()
        getAnswer()
    elif answer == "dataset view":
        if data.size > 0:
            print(data)
        else:
            print("No Data In data set")
        getAnswer()
    elif answer == "test":
        testMachineLearning()
    elif answer == "manually set model":
        printModels()
        model = input("MODEL:")
        setModel(model)
    elif answer =="dataset wipe":
        sure = input("are you sure(y/n)")
        if sure.lower() == "y":
            datasetWipe()
        getAnswer()
        datasetWipe()
    elif answer =="run at start":
        addToStartup()
        getAnswer()
    elif answer == "display crappy intro":
        printIntro()
        getAnswer()
    elif answer == "display guess":
        global rightGuess
        global wrongGuess
        if int(rightGuess) > 0 or int(wrongGuess) > 0:
            print("Right: ", rightGuess)
            print("Wrong: ", wrongGuess)
            if int(wrongGuess) == 0:
                wrongGuess = 1
            acc = round(int(rightGuess)/int(wrongGuess),2)
            print("Accuracy: ",acc)
        else:
            print("No predictions checked yet")
        getAnswer()
    elif answer == "auto":
        return
    else:
        print("invalid Command")
        getAnswer()
                
def gui():
    print()
    print("-------------------------------------------------------------------------------------------")
    print("                             Welcome to the badGambler                                     ")
    print("-------------------------------------------------------------------------------------------")
    getSettings() #set some global variables
    firstStart()
    getGuesses()
    printMenu()
def backbone():
    @connector.ready
    async def connect(connection):
        global connected
        connected = True
    @connector.close
    async def disconnect(connection):
        global connected
        connected = False
    @connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
    async def updated(connection,event):
            await getChampSelect(connection)
    @connector.ws.register('/lol-pre-end-of-game/v1/currentSequenceEvent', event_types=('UPDATE',))
    async def endGame(connection,event):
        await getEndGame(connection)
    connector.start()
#live code area
#what a pain
#had to split front and back into diffrent threads to run at the same time
t2 = threading.Thread(target=gui, args=())
t1 = threading.Thread(target=backbone, args=())
t1.start()
t2.start()
t1.join()
t2.join()
