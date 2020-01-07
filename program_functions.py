import datetime
import time
from math import ceil
import urllib.request
import ast
import random
track=0
curr_p=0.0
last_p=0.0
#current_date=datetime.datetime.now().strftime('%m/%d/%Y')
#current_time=datetime.datetime.now().strftime('%H:%M:%S')
#date=''
stockSymbol=''
URL=''

def webRead(URL,attempts):
    # Get a handle to the URL object
    try:
        h = urllib.request.urlopen(URL)
        response = h.read()

    except:
        attempts-=1
        print("Can't open "+URL)
        print("Trying Again")

        if(attempts==0):
            print("Cannot Load Page")
            quit()
        webRead(URL,attempts)
    return response

def addZeros(num):
    numS=str(num)
    if(num<10):
        numS='0'+numS
    return numS

def getStockPrice(IstockSymbol):

    URL='https://www.cnbc.com/quotes/?symbol='+IstockSymbol
    bighunk = webRead(URL,10)
    datatype = '<meta itemprop="price" content="'
    i = bighunk.find(datatype.encode())
    l= bighunk.find(('"').encode(),i+len(datatype))
    price=bighunk[i+len(datatype):l].decode()
    index=0
    for x in price:
        newPrice=price
        if(x==','):
            newPrice=price[0:index]
            newPrice=newPrice+price[index+1:]
            price=newPrice
        index+=1
    currentPrice=price

    return(currentPrice)

def getStockPriceHistory(IstockSymbol):
    URL='https://finance.yahoo.com/quote/'+IstockSymbol+'/history?ltr=1'
    priceList=[]
    bighunk = webRead(URL,10)
    datatype='HistoricalPriceStore'
    datatype2='"close":'
    datatype3='firstTradeDate'

    i = bighunk.find(datatype.encode())
    j = bighunk.find(datatype3.encode(),i)
    trimmed = bighunk[i:j]
    found=True
    start=0
    while found == True:

        j = trimmed.find(datatype2.encode(),start)
        if j != -1:
            start=j+len(datatype2)

            k = trimmed.find((',').encode(),j)
            result=trimmed[j+len(datatype2):k]
            priceList.append(getIntAvg(float(result.decode())))

        else:
            found = False

    return(priceList)

def getUpsDowns(priceList):
    ticker=0
    up_arr=[]
    down_arr=[]

    while(ticker!=len(priceList)-1):

        if(ticker>0):

            result=(priceList[ticker]-priceList[ticker-1])*-1
            if(result>=0):
                up_arr.append(result)
            else:
                down_arr.append(result)
        ticker+=1

    sum=0.0
    for num in up_arr:
        sum+=num
    avg_gain=sum/len(up_arr)
    sum=0.0
    for num in down_arr:
        sum+=num*-1
    avg_loss=sum/len(down_arr)

    up_len=len(up_arr)
    down_len=len(down_arr)

    return avg_gain, avg_loss,up_len,down_len
#print('Average gains to loss for '+stockSymbol+ ' is '+str(getIntAvg(avg_gain))+' with '+str(len(up_arr))+' days and '+str(getIntAvg(avg_loss*-1))+' with '+str(len(down_arr)))
#print('This means there is a '+str(getIntAvg(len(up_arr)/len(priceList))*100)+'% for upward movment and '+str(getIntAvg(len(down_arr)/len(priceList))*100)+'% for downward movment')
#print('This has on average had a yeild of '+str(getIntAvg((avg_gain*len(up_arr)/len(priceList))-(avg_loss*len(down_arr)/len(priceList))))+' per day')
#print('Max price was '+str(max(priceList))+' Low price was '+str(min(priceList)))

def getIntAvg(num):
    return ceil(num * 100) / 100.0

def getStockRev(stockSymbol):
    URL='https://finance.yahoo.com/quote/'+stockSymbol+'/financials?p='+stockSymbol
    bighunk = webRead(URL,10)
    lastSpot=0
    count=0
    numArray=[]
    while(count!=4):

        datatype = '"ebit"'
        i = bighunk.find(datatype.encode(),lastSpot)

        j = bighunk.find(('{').encode(),i-75)
        finding=bighunk[j+7:i-1].decode()
        numS=''
        lastSpot=i+10

        for c in finding:
            if(c!=','):
                numS=numS+c
            else:
                break
        if(len(numS)<20):
            numArray.append(numS)
        else:
            numArray.append('N/A')

        count+=1


    return numArray

def getStockIncome(stockSymbol):
    URL='https://finance.yahoo.com/quote/'+stockSymbol+'/financials?p='+stockSymbol
    bighunk = webRead(URL,10)
    lastSpot=0
    count=0
    numArray=[]
    while(count!=8):
        datatype = 'changeInCash'
        i = bighunk.find(datatype.encode(),lastSpot)

        j = bighunk.find(('{').encode(),i-75)
        finding=bighunk[j+7:i-1].decode()
        numS=''
        lastSpot=i+10

        if(count>3):

            for c in finding:
                if(c!=','):
                    numS=numS+c
                else:
                    break
            if(len(numS)<20):
                numArray.append(numS)
            else:
                numArray.append('N/A')
        count+=1



    return numArray

def getAvg(numArray):
    try:
        avgChange=[]
        changeArr=[]

        length=len(numArray)

        count=length-1
        while(count>0):

            change=(int(numArray[count])-int(numArray[count-1]))*-1
            changeArr.append(change)
            count-=1

        sum=0
        count=0
        for x in changeArr:
            sum+=x
            count+=1
        avgChange=sum//count
    except:
        print('Could Not Get Average in Array')
        print(numArray)
    return avgChange

def checkDowStrength(dowPrices,stockPrices):

    ticker=1
    combination=[]
    dowChange=[]
    stockChange=[]

    print('dow list has '+str(len(dowPrices)),'stock list has '+str(len(stockPrices)))

    while(ticker!=len(stockPrices)-1):

        result=(dowPrices[ticker]-dowPrices[ticker-1])*-1
        dowChange.append(result)
        result=(stockPrices[ticker]-stockPrices[ticker-1])*-1
        stockChange.append(result)
        ticker+=1
    i=0
    percentListD=[]
    percentListS=[]
    for x in range(0,len(stockPrices)):

        if i<len(dowChange):

            #Takes percent change from dow
            percent1=dowChange[i]/dowPrices[i+1]
            percent2=stockChange[i]/stockPrices[i+1]
            percentListD.append(percent1)
            percentListS.append(percent2)
            #gets the expected stock value using percentage from above
            #expects=stockPrices[x+1]+(percent1*stockPrices[x+1])

            #puts in to comb list the true value of stock subtracted by the expected value

            result=percent1-percent2

            #result=stockPrices[x]-expects
            if result<0:
                result*=-1
            combination.append(result)
        i+=1


    sum=0
    for y in combination:
        #print(y)
        sum+=y
    #getIntAvg(sum/len(combination))*-1)
    return str(getIntAvg((sum/len(combination)*100))),percentListD,percentListS

def getStockPE(stockSymbol):
    URL='https://www.macrotrends.net/stocks/charts/'+stockSymbol+'/'+stockSymbol+'/pe-ratio'
    htmlHunk=webRead(URL,10)
    datatype='PE ratio as of'
    datatype2='&gt;'
    datatype3='&'
    i=htmlHunk.find(datatype.encode())
    j=htmlHunk.find(datatype2.encode(),i)
    k=htmlHunk.find(datatype3.encode(),j+len(datatype2))
    pe=htmlHunk[j+len(datatype2):k].decode()
    #print(i,j,k)
    #print(htmlHunk[i:k])
    if(pe==''):
        return 'N/A'
    elif len(pe)>5:
        return 'Error'
    return pe

def randomStock():
   file=open('random_stocks.txt','r')
   string=file.read()
   randList=x = ast.literal_eval(string)
   return randList[random.randrange(0,len(randList))]

def getMarketCap(stockSymbol,price):
    htmlHunk=webRead('https://www.nasdaq.com/symbol/'+stockSymbol,10)
    datatype='Market Cap'
    datatype2='">'
    datatype3='<'
    i=htmlHunk.find(datatype.encode())
    j=htmlHunk.find(datatype2.encode(),i)
    k=htmlHunk.find(datatype3.encode(),j)

    numList=list(htmlHunk[j+2:k].decode().strip())
    newList=[]
    for num in numList:
        if num.isnumeric():
            newList.append(num)
    markCap=float(''.join(newList))
    outstandingShares=markCap/float(price)
    return markCap,getIntAvg(outstandingShares)

def getShortIntrest(stockSymbol):

    htmlHunk=webRead('http://shortsqueeze.com/shortinterest/stock/'+stockSymbol+'.htm',10)
    datatype='Shares Short'
    datatype2='">'
    datatype3='<'
    i=htmlHunk.find(datatype.encode())
    j=htmlHunk.find(datatype2.encode(),i)
    k=htmlHunk.find(datatype3.encode(),j)

    curShort=htmlHunk[j+len(datatype2):k].decode().strip()

    datatype='Shares Short'
    datatype2='">'
    datatype3='<'
    i=htmlHunk.find(datatype.encode(),k)
    j=htmlHunk.find(datatype2.encode(),i)
    k=htmlHunk.find(datatype3.encode(),j)

    prvShort=htmlHunk[j+len(datatype2):k].decode().strip()

    numList=list(curShort)
    newList=[]
    for num in numList:
        if num.isnumeric():
            newList.append(num)
    curShort=float(''.join(newList))

    numList=list(prvShort)
    newList=[]
    for num in numList:
        if num.isnumeric():
            newList.append(num)
    prvShort=float(''.join(newList))

    return curShort,prvShort

def addCommas(num):
    numL=len(str(num))
    num=str(num)

    numList=[]
    threeCount=0
    for x in range(numL,0,-1):


        if(threeCount%3==0 and threeCount!=0 and num[x-1]!='-'):
            numList.insert(0,',')
            numList.insert(0,num[x-1])
        else:
            numList.insert(0,num[x-1])

        threeCount+=1

        if num[x-1]=='.':
            threeCount=0
            numList=[]
        #if i==1:
           # numList.insert(0,num[0])

    return (''.join(numList))
