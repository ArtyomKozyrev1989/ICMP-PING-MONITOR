# Before start using the program you should setup it for yourself. Find all comments which contain Attention word in the file
# and do the needfull steps which are described in the marked comments.
# Please do not use mailboxes, to send notiffication messages from, with two stage authentification.
# If you struggle any difficulties to setup the program for yourself, feel free to apply kozirev8@gmail.com
# If any other question, feel free to let me know, I'll do my best to help.


import threading
import ipaddress
import sys
import time
import os
import smtplib
import enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    '''This is main function of the program'''
    StartProgram=True # checks if the problem can be started without errors
    listToMonitor=Main_Menu.main_menu_program_setup()#as a result we get list of ips to use in monitoring
    if(listToMonitor==None): # check if the list exists, if there is no list we get error message
        print("File IpAdressList contains zero IPs, or is corrupted, or does not exist.\n\nThe program will be closed soon.")
        StartProgram=False
        time.sleep(7)
    elif(len(listToMonitor)==0):
        print("File IpAdressList contains zero IPs, or is corrupted, or does not exist.\n\nThe program will be closed soon.")
        StartProgram=False
        time.sleep(7)
    if  StartProgram:
        print(f"The following list is monitored: {listToMonitor}")
        time.sleep(3)
        print("\n\nMonitoring has started! \n\n")
    while(StartProgram):
        IpMonitorThreads=[]
        for i in listToMonitor:
            IpMonitorThreads.append(MyPing(ipaddress=str(i),pingInterval=3))
            #create independent thread for each ip address
            # i is ip address from ip list
        for i in IpMonitorThreads:
            i.start()
        time.sleep(2)
        #threading.active_count()
        for i in IpMonitorThreads:
            i.join() # since fuction iside thread is infinite, join will never happen
            
class Main_Menu:
    
    def ask_ip():
        '''The fuction is used to ask user to  provide IP address for the program.
        Returns tuple IP and Boolean if we want to add it to the list of ip in further'''
        doYouWantAddIp=True
        while(doYouWantAddIp):
            print("What ip address would you like to choose for monitoring?")
            print("If you do not want to add any ip address:\nPress any button and follow to next recommendations.\n")
            IP=str(input())
            try:
                address1=ipaddress.IPv4Address(address=str(IP))
            except  ipaddress.AddressValueError:
                #print(sys.exc_info()) #it is very useful command
                print("You entered incorrect ip address please try to enter ip address again. \n\n")
                print("If you do not want to enter ip address print no.")
                print("If you still want to add any other ip address, press any other key.")
                word=input()
                if str(word).upper()=="NO":
                    doYouWantAddIp=False 
                    doYouStillWantAddIP=False # we do not want to add any ip
                    IP=None # we retrun empty value instead of ip
                time.sleep(2)
            else:
                doYouWantAddIp=False
                doYouStillWantAddIP=True 
        return (IP,doYouStillWantAddIP)
    
    def remove_duplicated_ip_from_file(file, resultList):
        '''The function is used to remove duplicated ip addressess from IpAdressList'''
        try:
            with open(file+".txt","w") as f:
                for i in resultList:
                    f.write(i+"\n")
        except FileNotFoundError:
            print("The file IpAdressList.txt is not reachable or corrupted.")
            print("Try to delete IpAdressList.txt if it exists and do initial setup process.")
            print("The program will be closed soon.\n")

    def add_ip_tofile(file, IP):
        '''The function is used to add IP to the desired file'''
        if(IP[1]): # the result of ask_ip (IP,doYouStillWantAddIP)
            file=str(file)
            file_name=file+".txt"
            with open(file_name, mode="a") as f:
                f.write(f"{IP[0]}\n")
            
    def what_ip_ismonitored(file):
        '''The funtcion shows what IPs are monitored in file, The fuction returns tuple which composed of
        List of ip and booilean value which prevents the program internal error if the file is empty or corrupted'''
        ToContinueProgram=True # is used to detect internal error if file is corrupted or does not exist
        try:
            with open(file+".txt",mode="r") as f:
                ipList=[]
                for i in f:
                    ipList.append(i.strip())
                f.seek(0)
        except FileNotFoundError:
            print("The file IpAdressList.txt is not reachable or corrupted.")
            print("Try to delete IpAdressList.txt if it exists and do initial setup process.")
            print("The program will be closed soon.\n")
            ToContinueProgram=False
            time.sleep(3)
            ipList=[]
            return (ipList,ToContinueProgram)
        else:
            print("Do not worry if you see duplicated IPs,\nthey will be removed before monitoring start.")
            print("The following List of ip adresses will be monitored:\n")
            for i in ipList:
                print(i)
            print("\n")
            return (ipList,ToContinueProgram)
        
    def do_you_need_more_ip():
        '''Just asks whether the user want more IPs to monitor. Return True or False value'''
        print("Do yo want to add more IP? Print yes or no.\n")
        word=""
        while(str(word).lower()!="yes" or str(word).lower()!="no" ):
            word=input()
            if str(word).lower()=="yes":
                return True
            elif str(word).lower()=="no":
                return False
            else:
                print("You should print only yes or no\n")
                
    def do_you_need_remove_more_ip():
        '''Just asks whether the user want remove more IPs from monitoring'''
        print("Do yo want to remove more IP? Print yes or no.\n")
        word=""
        while(str(word).lower()!="yes" or str(word).lower()!="no" ):
            word=input()
            if str(word).lower()=="yes":
                return True
            elif str(word).lower()=="no":
                return False
            else:
                print("You should print only yes or no\n")
                
    def remove_ip_address(file,ipList): 
        #addressList is the list of ip which is read from file, we gonna removing ip from the list
        '''The function is used to remove Ip addressess from file'''
        print("Do you want to remove any ip addresses? Print only yes or no.")
        word=""
        WantRemoveIP=True
        while(WantRemoveIP==True):
            word=input()
            if str(word).lower()=="yes":
                print("You chose yes, please see below list of IP which can be removed.")
                Main_Menu.what_ip_ismonitored(file)
                print("Choose ip to remove and print it:")
                text=""
                IsIpToRemoveInList=True 
                removeMoreIP=True
                while(IsIpToRemoveInList):
                    text=str(input())
                    if(str(text) in ipList):             
                        ipList.remove(str(text))
                        with open(f"{file}.txt",mode="w") as f:
                            for i in ipList:
                                f.write(f"{i}\n")
                        WantRemoveIP=False
                        IsIpToRemoveInList=False
                        removeMoreIP=True
                    else:
                        print("The ip address should be in the list. Please try again.\n")
                        print("If you do not want to remove any IP print yes. If other is printed, it is considered as no.\n")
                        test=str(input())
                        if test.lower()=="yes":    
                            WantRemoveIP=False
                            IsIpToRemoveInList=False
                            removeMoreIP=False
                        else:
                            print("You chose no then try again please.\n")
                            removeMoreIP=True
                        
            elif str(word).lower()=="no":
                print("You chose no, no ip adressess will be removed.\n")
                WantRemoveIP = False
                removeMoreIP = False
            else:
                print("You should print only yes or no.\n")
                removeMoreIP=True
            return removeMoreIP
                     
    def read_ip_from_file(file):
        '''The function is used to read Ip addresses from file and return it as list'''
        try:
            with open(file+".txt",mode="r") as f:
                ipList=[]
                for i in f:
                    ipList.append(i.strip())
                f.seek(0)
        except FileNotFoundError:
            print("The file IpAdressList.txt is not reachable or corrupted.")
            print("Try to delete IpAdressList.txt if it exists and do initial setup process.")
            print("The program will be closed soon.\n")
        else:
            return ipList 
                  
    def main_menu_program_setup():
        '''This fuction is used to make initial setup'''
        print("******** The program is used for remote IPs ping monitoring ********")
        print("******** The program is designed only for Windows OS **********\n")
        print("Do you want to do any initial setup? If yes print yes, otherwise print no.\n")
        DoYouNeedSetup=True 
        while(DoYouNeedSetup):
            word=str(input())
            if(word.lower()=="yes"):
                DoNeedAddIPs=True 
                while(DoNeedAddIPs):
                    IPboolToAdd=Main_Menu.ask_ip() #is tuple which contains ip,boolean
                    Main_Menu.add_ip_tofile(IP=IPboolToAdd,file="IpAdressList") # adds ip address to file
                    if(IPboolToAdd[1]==True): # if user want more ip then
                        DoNeedAddIPs=Main_Menu.do_you_need_more_ip() # ask if user really want more ip
                    else:
                        DoNeedAddIPs=False
                    ipListDoExist=Main_Menu.what_ip_ismonitored(file="IpAdressList")
                      #returns list of ip and boolean which indicates whether the list really exists
                    if(ipListDoExist[1]==False):
                        DoYouNeedSetup=False # if the list is empty or corrupted  we will breal error and read error message                  
                DoYouNeedRemoveIP=True # checks if we want to remove any ip
                while(DoYouNeedRemoveIP and DoYouNeedSetup): 
                    # DoYouNeedSetup is used here since we do not want the operation if list (file) empty or  corrupted
                    removeMore=Main_Menu.remove_ip_address(file="IpAdressList",ipList=ipListDoExist[0]) 
                    # adressList is a list which was read from file to delete ip from
                    if(removeMore):
                        DoYouNeedRemoveIP=Main_Menu.do_you_need_remove_more_ip()
                    else:
                        DoYouNeedRemoveIP=False
                DoYouNeedSetup=False
            elif(word.lower()=="no"):
                print("You chose no, no initial setup will be made.\n")
                Main_Menu.what_ip_ismonitored(file="IpAdressList")  
                DoYouNeedSetup=False
            else:
                print("Incorrect input, you should press only yes or now. Try again please\n")
        resultList=Main_Menu.read_ip_from_file(file="IpAdressList")
        if(resultList!=None): #if the list in not empty and exists (is checked in read_ip_from_file)
            resultList=set(Main_Menu.read_ip_from_file(file="IpAdressList"))
            Main_Menu.remove_duplicated_ip_from_file(file="IpAdressList", resultList=resultList)
        time.sleep(1) 
        return resultList # as a result we get list of IPs to work with  

class MyMailActivity:
    '''This class is used to make mail activity for the program'''
    def send_negative_mail(ipAddress,email_sender,email_receiver):
        '''The method sends negative mail if ip is not reachable'''
        ipAddress=str(ipAddress)
        # Attention! write your own mail subject, do not delete words inside brackets str(MyTime(MyTimeMode.full))
        subject=f"MTT Oy error notification L1 {str(MyTime(MyTimeMode.full))}"
        msg = MIMEMultipart() 
        msg['From'] = email_sender
        msg['To'] = ", ".join(email_receiver)
        msg['Subject']= subject
        # Attention! write your own mail message, do not delete words inside brackets ipAddress and str(MyTime(MyTimeMode.full))
        body=f"""Dear Partner,\n\nWe observe that address {ipAddress} is not reachable within last 30 seconds.
Now {str(MyTime(MyTimeMode.full))}.
        
We ask you to investigate the issue and undertake all necessary steps to solve the problem.
        
Best Regards,\nMTT Oy Network Monitor Robot"""

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string() 
        try:
            connection = smtplib.SMTP('smtp.gmail.com', 587) # Attention! This should be settings of you smtp server
            connection.starttls()  
            connection.login(email_sender, 'YourMailBoxPassword')
            # Attention! Put password of your mailbox to send mails about alarms from
            connection.sendmail(email_sender, email_receiver, text)
            connection.quit()
        except:
            print("Connection to SMTP server failed.")
            errormessage1=(sys.exc_info())
            print(errormessage1)
            with open(file="ErrorLog.txt", mode="a") as f:
                f.write(str(MyTime(MyTimeMode.full)))
                f.write("Connection to SMTP server failed.")
                f.write(errormessage1)            
            
    def send_positive_mail(ipAddress,email_sender,email_receiver):
        '''The method sends positive mail if ip is reachable again'''
        ipAddress=str(ipAddress)
        # Attention! write your own mail subject, do not delete words inside brackets str(MyTime(MyTimeMode.full))
        subject=f"MTT Oy recovery notification L1 {str(MyTime(MyTimeMode.full))}"
        msg = MIMEMultipart() 
        msg['From'] = email_sender
        msg['To'] = ", ".join(email_receiver)
        msg['Subject']= subject
        # Attention! write your own message, do not delete words inside brackets ipAddress and str(MyTime(MyTimeMode.full))
        body=f"""Dear Partner,\n\nWe observe that address {ipAddress} has recovered and is stable within last 60 seconds.
Now {str(MyTime(MyTimeMode.full))}.
        
We ask you to investigate and provide us RFO.
        
Best Regards,\nMTT Oy Network Monitor Robot"""

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()  
        try:
            connection = smtplib.SMTP('smtp.gmail.com', 587) # Attention! This should be settings of you smtp server
            connection.starttls()  
            connection.login(email_sender, 'YourMailBoxPassword') 
            # Attention! Put password of your mailbox to send mails about alarms from
            connection.sendmail(email_sender, email_receiver, text)
            connection.quit()
        except:
            print("Connection to SMTP server failed.")
            errormessage1=(sys.exc_info())
            print(errormessage1)
            with open(file="ErrorLog.txt", mode="a") as f:
                f.write(str(MyTime(MyTimeMode.full)))
                f.write("Connection to SMTP server failed.")
                f.write(errormessage1)

class MyTimeMode(enum.Enum):
    '''This class is createc to be used in instances of MyTime class to determine options of __str__ format for that clls'''
    full = "Date: {2}.{1}.{0} Time UTC+3 {3}:{4}:{5}"
    middle = "date{2}_{1}_{0}_timeUTC3_{3}"
    short = "date{2}_{1}_{0}"

class MyTime:
    '''This class is used to display datetiem in the program'''
    def __init__(self,mode=MyTimeMode.middle):
        ''' Is used to create class instance'''
        self.timeNow=time.localtime()
        self.mode=mode

    def __str__(self):
        '''Is used to create string representation of the MyTime Class to be used in print, etc'''
        currentTime=map(lambda x: "0"+str(x) if x<10 else str(x),[self.timeNow.tm_mday,self.timeNow.tm_mon, self.timeNow.tm_year,
                                                        self.timeNow.tm_hour,self.timeNow.tm_min, self.timeNow.tm_sec])

        return self.mode.value.format(*currentTime) # value is an attribute of enum class
    def compare_dates(self,date_compare):
        '''The class is used to compare instance of MyTime Class'''
        if self.timeNow.tm_year>date_compare.timeNow.tm_year:
            return True
        elif self.timeNow.tm_year<date_compare.timeNow.tm_year:
            return False
        else:
            if self.timeNow.tm_mon>date_compare.timeNow.tm_mon:
                return True
            elif self.timeNow.tm_mon<date_compare.timeNow.tm_mon:
                return False
            else:
                if self.timeNow.tm_mday>date_compare.timeNow.tm_mday:
                    return True
                elif self.timeNow.tm_mday<date_compare.timeNow.tm_mday:
                    return False
                else:
                    if self.timeNow.tm_hour>date_compare.timeNow.tm_hour:
                        return True
                    else:
                        return False
                        
                        

class MyPing(threading.Thread):
    '''This class is derived form Thread and primary is used for ping itself and file operations to write ping results'''
    def __init__(self,ipaddress,pingInterval):
        '''Is used to create MyPing instances'''
        threading.Thread.__init__(self)
        self.ipaddress=ipaddress
        self.pingInterval=pingInterval
    def ping(self):
        ''' Is used to do one ping and retrun reults'''
        pingresult=os.system(f"ping -n 1 {self.ipaddress}")
        if pingresult==0:
            time.sleep(self.pingInterval)
            pingResult=(1,0) # successfull attempt
            return pingResult
        elif pingresult==1:
            pingResult=(0,1) # failed attempt
            return pingResult
        else:
            pass
    def write_ping_result_to_file(self,pingResult):
        '''Is used to wirte ping reults to file, return path to the file'''
        currentDirectory=os.getcwd()
        folderToSavePingResultsUpper=str(self.ipaddress)
        folderToSavePingResultsLower=str(self.ipaddress)+str(MyTime(MyTimeMode.short))
        folderToSavePingResults=os.path.join(currentDirectory,folderToSavePingResultsUpper, folderToSavePingResultsLower)
        if not os.path.exists(folderToSavePingResults): # if the path do not exist then 
            os.makedirs(folderToSavePingResults) # create it now!         
        with open(os.path.join(folderToSavePingResults,
                               f"ping_{str(MyTime(MyTimeMode.middle))}_{self.ipaddress}.txt"),mode="a") as f:
            if pingResult==(1,0):
                f.write(f"The remote destination {self.ipaddress} is reachable, everyting is OKAY. {str(MyTime(MyTimeMode.full))} \n")
            elif pingResult==(0,1):
                f.write(f"Ping {self.ipaddress} failed! {str(MyTime(MyTimeMode.full))} \n")
            else:
                pass
            FilePath=os.path.join(folderToSavePingResults,f"ping_{str(MyTime(MyTimeMode.middle))}_{self.ipaddress}.txt")
            return FilePath
                
    def write_ping_stats_to_file(self,positivePingsThisHourCounter,negativePingsThisHourCounter,previousFilePath):
        '''Writes percent of successfull attempts to file which was used to write ping reuslts in wuthin previous hour'''
        with open(previousFilePath,mode="a") as f:
            k=100*positivePingsThisHourCounter/(positivePingsThisHourCounter+negativePingsThisHourCounter)
            f.write("\n")
            f.write(f"{self.ipaddress}__positivePingAttempts_Number_is__{positivePingsThisHourCounter}\n")
            f.write(f"{self.ipaddress}__negativePingAttempts_Number_is__{negativePingsThisHourCounter}\n")
            f.write(f"{self.ipaddress}__Percent of_positivePingAttempts__is__{k}\n")
            f.write("\n")
                    
    def infinite_ping(self):
        '''Main method of the class, it is used to create infinite ping Thread'''
        pingFailedLetterWasSent=False
        positivePingsThisHourCounterC=0
        negativePingsThisHourCounterC=0
        positivePingsInRow=0
        negativePingsInRow=0
        lastAttemptTime=MyTime()
        previousFilePath=self.write_ping_result_to_file(pingResult=None)
        while(True):
            pingresult=self.ping()
            CurrentFilePath=self.write_ping_result_to_file(pingResult=pingresult)
            currentTime=MyTime()
            if currentTime.compare_dates(lastAttemptTime):
                self.write_ping_stats_to_file(positivePingsThisHourCounter=positivePingsThisHourCounterC,
                                              negativePingsThisHourCounter=negativePingsThisHourCounterC,
                                              previousFilePath=previousFilePath)
                previousFilePath=CurrentFilePath
                lastAttemptTime=currentTime
                positivePingsThisHourCounterC=0
                negativePingsThisHourCounterC=0
            positivePingsThisHourCounterC=positivePingsThisHourCounterC+pingresult[0]
            negativePingsThisHourCounterC=negativePingsThisHourCounterC+pingresult[1]
            if positivePingsInRow<positivePingsInRow+pingresult[0]:
                positivePingsInRow=positivePingsInRow+pingresult[0]
                negativePingsInRow=0
            if negativePingsInRow<negativePingsInRow+pingresult[1]:
                positivePingsInRow=0
                negativePingsInRow=negativePingsInRow+pingresult[1]                
            if negativePingsInRow==4 and pingFailedLetterWasSent==False:
                print("Negative mail was sent")
                # Attention! Put your own mail settings in the code below, do not remove f"{self.ipaddress}:
                MyMailActivity.send_negative_mail(f"{self.ipaddress}","SendFrom@gmail.com",
                                                  ["SendTo1@gmail.com","SendTo2@gmail.com","SendTo3@gmail.com"])
                pingFailedLetterWasSent=True
            if positivePingsInRow==20 and pingFailedLetterWasSent==True:
                print("Positive mail was sent")
                # Attention!Put your own mail settings in the code below, do not remove f"{self.ipaddress}:
                MyMailActivity.send_positive_mail(f"{self.ipaddress}","SendFrom@gmail.com",
                                                  ["SendTo1@gmail.com","SendTo2@gmail.com","SendTo3@gmail.com"])
                pingFailedLetterWasSent=False

                
    def run(self):
        '''The method is rewritten method of Thread class'''
        self.infinite_ping()
            
if __name__ == '__main__':
    main()



