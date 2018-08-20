#Wesley Lasky



from bs4 import BeautifulSoup
import urllib
import re



cik = "0001166559" #the cik or ticker
#"0001569205"  
#"0001166559"


form=re.compile("^13F")# regex used to find the form needed
testn=re.compile("infoTable$",re.IGNORECASE) #regex used to find thre xml file
tag=re.compile(".<\/.*>")# regex used to find the Name of a tag
inside=re.compile(">.*<")# regex used to find the text from a tag

def getdoc(ticker):
    url=urllib.request.urlopen("https://www.sec.gov/cgi-bin/browse-edgar?CIK="+ticker+"&Find=Search&owner=exclude&action=getcompany")# goes to the link using the given ticker or cik
    soup = BeautifulSoup(url, 'html5lib')# gets the html
  
    link=soup.find("td",text=form).find_next_sibling().find("a")["href"]#looks for the tag td that wich has text that corresponds to the regex. then finds the sibling and gets the href from it's a tag
    link="https://www.sec.gov"+link #creates new link from the href

    
    url=urllib.request.urlopen(link)#opens the link
    soup = BeautifulSoup(url, 'html5lib')
    link=soup.findAll("tr",{"class":"blueRow"})[-1].find("a")["href"]#finds all tag tr with the corresponding class. takes the last tr and finds the href of tag a
    link="https://www.sec.gov"+link #creates new link from the href

    return getholdings(link)
    
    
def getholdings(link):
    url=urllib.request.urlopen(link)
    soup = BeautifulSoup(url, 'xml')
    holdings =soup.findAll(testn)#finds all info tables in the xml
    keys=[]#used to store a list of keys that will be used to make a dictionary
    holds=str(holdings[0]).splitlines()#splits the lines in the first info table
    
    for i in holds:#used to get all the tag names. These will be used as the keys
        k=re.search(tag,i)
        if k!=None:#skips any none values
            key=k.group(0)
            key=key[3:-1] #removes the first 3 chars used to find the name as well as the last 1
            keys.append(key)
    
    holdings2=[] #list for holding dictionaries
    
    for i in range(len(holdings)):#
        temp=str(holdings[i]).splitlines()#splits the lines in the first info table
        dic={}#dictionary
        c=0#counter
        for j in range(len(temp)):
            ins=re.search(inside,temp[j])#searchs for the text in the tag

            if ins!=None:#skips any none values
                text=ins.group(0)
                text=text[1:-1] #removes the first and last char use to find the text
                add=keys[c]
                dic[add]=text #creates the key value pair
                c+=1#increments by 1
        holdings2.append(dic)
    return holdings2


def write(hold):
    f=open("FundsHoldings.tsv","w+")#writes to the file
    for key in hold[0]:  
        f.write(key+"\t")
        
    for i in range(len(hold)):
        f.write("\n")
        for key in hold[i]:
            f.write(hold[i].get(key)+"\t")
    f.close

q=getdoc(cik)
write(q)