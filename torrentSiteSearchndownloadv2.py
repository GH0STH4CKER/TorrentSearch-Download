from urllib.request import urlopen as uOpen
import bs4 , requests , time , socket , os , sys
from requests import Session
from bs4 import BeautifulSoup as bSoup 
import xml , webbrowser
from xml import etree
from xml.etree import ElementTree
from colorama import Fore , init
init()
lG = Fore.LIGHTGREEN_EX     # Colours
lY = Fore.LIGHTYELLOW_EX
lR = Fore.LIGHTRED_EX
cyan = Fore.CYAN
lC = Fore.LIGHTCYAN_EX
lB = Fore.LIGHTBLUE_EX

def slowprint(str):            # Slow print function
   for c in str :
     sys.stdout.write(c)
     sys.stdout.flush()
     time.sleep(0.4)

def rem_tags (st) :         # Removing html tag function

    return ''.join(xml.etree.ElementTree.fromstring(str(st)).itertext())

banner = """
▀█▀ █▀█ █▀█ █▀█ █▀▀ █▄░█ ▀█▀   █▀ █▀▀ ▄▀█ █▀█ █▀▀ █░█
░█░ █▄█ █▀▄ █▀▄ ██▄ █░▀█ ░█░   ▄█ ██▄ █▀█ █▀▄ █▄▄ █▀█"""
tagline = """
  [+] Tool by GH0STH4CK3R      [+] Site 1337x.to
-----------------------------------------------------"""

try:
    print(cyan + banner)
    print(lC + tagline)

    phrase = input("\nSearch Torrents : ")

    url = "https://1337x.to/srch?"           # Searching for film with get request
    param = {"search": phrase}

    res = requests.get(url , params=param)

    if res.status_code == 200 :          
        
        redir_url = res.url                 # Getting the redirected url
        #print(redir_url)    
        print("\nSearching",end="")
        time.sleep(0.5)
        slowprint("....")                #print dots slowly

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.95"
        }
        time.sleep(0.5)
        os.system('cls')
        print(cyan + banner)
        print(lC + tagline)
        print(lC + f"\nSearch Results For \"{phrase}\" : \n")
        resps = requests.get(redir_url , headers=headers)      # Get request to get html code
        
        if resps.status_code == 200 :
            
            link_list = []
            t_no = 0
            #print(resps.text)
            #uClient = uOpen(redir_url)
            page_html = resps.text #uClient.read()                     # Setting response text as page_html
            #uClient.close()
            page_soup = bSoup(page_html,"html.parser")

            names = page_soup.find_all("td",{"class":"coll-1 name"})         # Finding elements 
            seeds = page_soup.find_all("td",{"class":"coll-2 seeds"})
            leaches = page_soup.find_all("td",{"class":"coll-3 leeches"})
            times = page_soup.find_all("td",{"class":"coll-date"})
            sizes = page_soup.find_all("td",{"class":"coll-4"})
            uploaders = page_soup.find_all("td",{"class":"coll-5"})
            
            if len(names) == 0 :                                        # checking if theres no torrents found  
                os.system('cls')
                print(lR + f"No results for \"{phrase}\" ")
                time.sleep(4)
                exit()

            for i in range(len(names)) :    

                nameN = rem_tags(names[i])                 # Removing Html tags and assign to new variable
                seedN = rem_tags(seeds[i])
                leachN = rem_tags(leaches[i])
                timeN = rem_tags(times[i])
                sizeN = rem_tags(sizes[i])
                uploaderN = rem_tags(uploaders[i])
                links = names[i].find_all("a")    
                link = str(links[1])
                
                while True :                  # Getting site link of torrent
                    if link[0] == "\""  :
                        break
                    link = link[+1:]
                
                while True :
                    if link[-1] == "\""  :
                        break
                    link = link[:-1]
                
                while True :                  # removing useless tag inside torrent size
                    if sizeN[-1] == "B" : 
                        break
                    sizeN = sizeN[:-1]   
                t_no += 1
                link = link[:-1]        # Removing double quotes before and after the link
                link = link[+1:]
                linkN = "https://1337x.to" + link   # joining to make full url
                link_list.append(linkN)
                
                print(lC +"\n[",t_no,"] ",end="")       # Printing torrent list (for search phrase)
                print(lY + "",nameN)    
                print(lG +"Seeds :",seedN,end="  ")
                print("Leeches :",leachN,end="  ")
                print("Time :",timeN)
                print("Size :",sizeN,end="  ")
                print("Uploader :",uploaderN)
                #print("Link :",linkN)
                time.sleep(0.3)
            
            print(lC + "")
            
            try:
                #print(lC +"\nTorrent Link :\n",lY + link_list[int(choice)-1])
                choice = input("Enter torrent no : ")                          # Input torrent number 
                Torr_link = link_list[int(choice)-1]
            except Exception as e2:
                print(lR + "Error",e2)    
                print("Enter only displayed numbers !")                       # Error Handling

            resp3 = requests.get(Torr_link)    # Get request to get html data of selected torrent
            Down_links = []
            Down_sites = []

            page_html2 = resp3.text 
            page_soup2 = bSoup(page_html2,"html.parser")
            dropdown = page_soup2.find("li",{"class":"dropdown"})  #Getting download dropdown elements
            headerNM = page_soup2.find("h1")
            saveNM = rem_tags(headerNM)
            
            downsite_names = dropdown.find_all("a")
            for b in range(len(downsite_names)) :
                if b != 0 :
                    #print(rem_tags(downsite_names[b]))
                    Down_sites.append(rem_tags(downsite_names[b])) #append downloading site names to a list ex- itorrents 

            for a in dropdown.find_all('a', href=True):
                
                if a['href'] != "#" and a['href'] != "" :
                    #print("\n",a['href'])
                    Down_links.append(a['href'])    #append download links to a list 

            print(lC + "\n[1] Download Torrent File (Direct) \n[2] Open Torrent Client (Magnet Link) \n[3] Manual Download (links)")
            choice2 = input("\nChoose Download Method : ")     
            if choice2 == "1" :                               # Download direct method (.torrent)  
                print(lG + "\nDownloading...")
                time.sleep(1)
                direct_link = str(Down_links[0])

                #if "https" not  in direct_link :                       
                    #direct_link = direct_link.replace("http","https")                    

                saveNM = saveNM.replace("(","") # Removing illegal chars
                saveNM = saveNM.replace(")","")
                saveNM = saveNM.replace("[","")
                saveNM = saveNM.replace("]","")
                saveNM = saveNM.replace("-","")
                saveNM = saveNM.replace("/","")
                saveNM = saveNM.replace(".","")
                
                session = Session()
                session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
                
                r = session.get(direct_link)
                
                saveNM = saveNM + ".torrent"
                if r.status_code == 200 :
                    open(saveNM, 'wb').write(r.content)   # Saving file 
                    print("\nSaved Successfully > check current folder ")
    
                else:
                    print(lR + "Something went wrong, Error code ",r.status_code,"\nFailed to download :",direct_link)

                print(lC +"")
                downchoice = input("Didn't work ? \nTry another method ! (Y/n) : ")  # asking if downloaded or not 

                if downchoice == "Y" or downchoice == "y" :
                    webbrowser.open_new_tab(Down_links[0])    # open another link in web browser
                else:
                    print("")
                
            elif choice2 == "2":
                try:
                    webbrowser.open_new_tab(Down_links[-1])          # Torrent magnet download
                    print(lG + "Openning Torrent Client...")         # opening torrent client 
                except Exception as eee:
                    print(lR + "Error while opening torrent client")
                    print(eee)
                else:
                    print("")        
            elif choice2 == "3" :                                 #Manual method
                
                print(lG + f"Site link : {Torr_link} \n")        # Display all download links
                print("All Download links \n")
                for z in range(len(Down_sites)) :
                    print("\n",lC + Down_sites[z],":",lG + Down_links[z])
                    time.sleep(0.5)      

            else:
                print(lR + "Invalid option !")          

        else:                                                      
            print(lR + "Redirection Failed",resps.status_code)   # If Request error occrs these are printed
    else:
        print(lR + "Error occured while searching",res.status_code)    

except Exception as e :
    print(lR + "Something went wrong\n",e)

input("\nExit >")