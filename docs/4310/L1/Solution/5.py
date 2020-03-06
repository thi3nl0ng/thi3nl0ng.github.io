import nltk, re
from urllib import request

url="https://www.ntnu.edu/vacancies"
def LoadJobNTNU():
        response = request.urlopen(url)
        rawtext = response.read().decode('utf8')
        regex = r'<h3>*<a.*?>.*?<\/a><\/h3>'
        joblist = re.findall(regex,rawtext)
        return joblist
def PrintNumberOfJob(joblist):
         print('Number of avaiable jobs is', len(joblist))
def PrintJob(joblist):
        number = 0
        for job in joblist:
                jobtitle = re.findall(r"title=\".*\"",job)                
                if len(jobtitle) > 0:
                        number+=1
                        full = jobtitle[0].split(':')
                        print(number, full[0][7:-15])

def ExtractDeadline(joblist):
        number = 0
        for job in joblist:#3
                
                jobtitle = re.findall(r"title=\".*\"",job)
                if len(jobtitle) > 0:
                        number+=1
                        full = jobtitle[0].split(':')
                        print(number, full[0][7:-15])
                        print( ' Deadline ' , full[1][:-1])

if __name__ == '__main__':
        joblist = LoadJobNTNU()
        input("\nPress ENTER for task 5a")
        PrintNumberOfJob(joblist)
        
        input("\nPress ENTER for task 5b")
        PrintJob(joblist)

        input("\nPress ENTER for task 5c")
        ExtractDeadline(joblist)
