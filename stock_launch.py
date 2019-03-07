import tkinter as tk
from tkinter import *
from program_functions import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
root = Tk()

#frame=Frame(root,width=300,height=100)
#frame.grid()

theLable = Label(root, text='Enter Stock Symbol')
theLable.grid(row=0,column=0,sticky=NW)

T = Text(root,height=1,width=5)
T.grid(row=1,column=0,sticky=NW)

stockNameL=Label(root,text='Stock Symbol:')
stockNameL.grid(row=4,sticky=W)
stockpriceL=Label(root,text='Stock Price:')
stockpriceL.grid(row=5,sticky=W)
stockYearL=Label(root,text='Up/Down Over Year:')
stockYearL.grid(row=6,sticky=W)
stockHlL=Label(root,text='High: Low:')
stockHlL.grid(row=7,sticky=W)
stockPeL=Label(root,text='PE(TTM):')
stockPeL.grid(row=8,sticky=W)
stockPlL=Label(root,text='Chance Of Profit/Loss:')
stockPlL.grid(row=9,sticky=W)
stockdowL=Label(root,text='Dow Trend Break:')
stockdowL.grid(row=10,sticky=W)

stockMark=Label(root,text='Market Cap:')
stockMark.grid(row=11,sticky=W)
stockOut=Label(root,text='Outstanding Shares:')
stockOut.grid(row=12,sticky=W)
stockShort=Label(root,text='Percent Short: Prevous: ')
stockShort.grid(row=13,sticky=W)

stockRevsL=Label(root,text='Last Four Revenues: ')
stockRevsL.grid(row=14,sticky=W)

stockIncL=Label(root,text='Last Four Incomes: ')
stockIncL.grid(row=15,sticky=W)

priceList=[]
curPrice=0.0
revList=[]
incomeList=[]
dowMatch=''

print('Getting Dow Info')
dowList=getStockPriceHistory('%5Edji')
#dow_cur_price=float(getStockPrice('.DJI'))
#dowList.insert(0,dow_cur_price)
#print(dowList[0],dowList[1],dowList[2])
print('Done')

def stockInfo():
    print('Getting Stock Info')
    stockSymbol=T.get("1.0",'end-1c')
    stockNameL.config(text = 'Stock Symbol: '+stockSymbol.upper())

    priceList = getStockPriceHistory(stockSymbol)
    curPrice=priceList[0]
    #curPrice=float(getStockPrice(stockSymbol))
    #print(priceList[0],curPrice)
    #priceList.insert(0,curPrice)
    yestPrice=priceList[1]
    change=getIntAvg((yestPrice-curPrice)*-1)
    stockpriceL.config(text="Stock Price: $"+str(curPrice)+' ('+str(change)+')')

    rounded=getIntAvg(float(curPrice)-priceList[-1])
    rounded=rounded/(float(curPrice)+rounded*-1)
    stockYearL.config(text='Up/Down Over Year: $'+ str(getIntAvg(float(curPrice)-priceList[-1]))+' from $'+str(priceList[-1])+' at a '+str(getIntAvg(rounded)*100)+'% Change')
    stockHlL.config(text='High: $'+str(max(priceList))+'     Low: $'+str(min(priceList)))
    stockPeL.config(text='PE(TTM): ' + getStockPE(stockSymbol))

    avg_gain,avg_loss,up_len,down_len = getUpsDowns(priceList)
    stockPlL.config(text='Chance Of Profit/Loss: $'+str(getIntAvg(avg_gain))+' at a '+ str(getIntAvg(up_len/len(priceList))*100)+'% Upward and $'+str(getIntAvg(avg_loss)*-1)+' at a '+str(getIntAvg(down_len/len(priceList))*100)+'% Downward $'+str(getIntAvg((avg_gain*up_len/len(priceList))-(avg_loss*down_len/len(priceList))))+' Yeild Per Day')

    dowMatch,dowChange,stockChange=checkDowStrength(dowList,priceList)
    todayMatch=getIntAvg((stockChange[0]-dowChange[0])*100)
    if todayMatch<0:
        todayMatch*=-1
    stockdowL.config(text='Avg Dow Trend Break: '+str(float(dowMatch))+' Todays Break: '+ str(todayMatch))

    revList=getStockRev(stockSymbol)
    incomeList=getStockIncome(stockSymbol)
    finStr=''
    for x in revList:
        finStr=finStr+' ($'+addCommas(x)+')'
    finStr=finStr+' Average Movment: $'+addCommas(getAvg(revList))
    stockRevsL.config(text='Last Four Revenues: '+finStr)

    finStr=''
    for x in incomeList:
        finStr=finStr+' ($'+addCommas(x)+')'
    finStr=finStr+' Average Movment: $'+addCommas(getAvg(incomeList))
    stockIncL.config(text='Last Four Incomes: '+finStr)


    marCap,outShars=getMarketCap(stockSymbol,curPrice)
    stockMark.config(text='Market Cap: $'+addCommas(marCap))
    stockOut.config(text='Outstanding Shares: '+addCommas(outShars))

    curShort,prevShort=getShortIntrest(stockSymbol)
    stockShort.config(text='Percent Short: '+str(getIntAvg(curShort/outShars)*100)+ '% Prevous: '+str(getIntAvg(prevShort/outShars)*100)+'%')

    fig, axes= plt.subplots(figsize=(5,5))

    avgList=[]
    avgListD=[]
    avgSpred=[]

    lastFloat=dowChange[len(dowChange)-1]*100
    lastFloat2=stockChange[len(stockChange)-1]*100

    for i in range(len(stockChange)-1):
        avgListD.append(lastFloat)
        avgList.append(lastFloat2)
        if i > 10:
            if lastFloat-lastFloat2<0:
                avgSpred.append((lastFloat-lastFloat2)*-1)
            else:
                avgSpred.append((lastFloat-lastFloat2))
        x=len(stockChange)-i-1
        axes.plot([i,i+1],[lastFloat,lastFloat+(dowChange[x-1]*100)],'r')
        lastFloat=lastFloat+(dowChange[x-1]*100)
        axes.plot([i,i+1],[lastFloat2,lastFloat2+(stockChange[x-1]*100)],'b')
        lastFloat2=lastFloat2+(stockChange[x-1]*100)
    avgD=sum(avgListD)/len(avgListD)
    avg=sum(avgList)/len(avgList)
    axes.plot([0,len(stockChange)-1],[0,avg],'b')
    axes.plot([0,len(dowChange)-1],[0,avgD],'r')

    avgGap=sum(avgSpred)/len(avgSpred)
    print('That average gap is '+str(avgGap)+' and the current Gap is '+str(avgSpred[-1]))
    print(avgSpred[0])
    plt.show()


def getRandStock():
    T.delete(1.0, END)
    T.insert(END,randomStock())
    stockInfo()

button1 = Button(root,text='Submit',command=stockInfo)
button1.grid(row=2,sticky=NW)

button2 = Button(root,text='Random',command=getRandStock)
button2.grid(row=2,column=1,sticky=W)

root.mainloop()
