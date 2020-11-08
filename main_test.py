import os
from datetime import datetime
from collections import OrderedDict

def emails_without_wave_information(email_files):
    spam_emails = {}
    for email in email_files:
        with open(email, 'r') as s:
            lines = s.readlines()
            if lines[2].find("wave") == -1:
                spam_emails[email]=lines[0].split()[-1]
    return spam_emails

def emails_without_daiictid(email_files):
    spam_emails = {}
    for email in email_files:
        with open(email, 'r') as s:
            lines = s.readlines()
            if lines[0].split()[-1].find("daiict.ac.in") == -1:
                spam_emails[email]=lines[0].split()[-1]
    return spam_emails

def rename_files(spam_emails):
    i=1
    for email in spam_emails:
        with open(email,'r+') as s:
            content = s.read()
            s.seek(0)
            s.write("This email has been categorized as spam\n"+content)
        os.rename(email,"spam"+str(i)+".txt")    
        i += 1

def time_to_timestamp(t_d):
    months = {
        'January':1,
        'February':2, 
        'March':3,
        'April':4, 
        'May':5, 
        'June':6, 
        'July':7, 
        'August':8, 
        'September':9, 
        'October': 10, 
        'November':11, 
        'December':12
    }

    hr, minute = map(int, t_d[0].split(':'))  
    month = months[t_d[-3]] 
    day =  int(t_d[-2][:-1]) 
    year = int(t_d[-1])

    return datetime(year, month, day, hr, minute, 0, 0) 

def generate_ordered_names(lst):
    to_be_written = dict()
    for file in lst:
        with open(file, 'r') as fl:
            line = fl.readline()
            content = line.split()
            t_d, name = time_to_timestamp(content[2:8]), content[-1]

            if to_be_written.get(t_d):
                to_be_written[t_d].append(name)
            else:
                to_be_written[t_d] = [name]

    Ordered = OrderedDict(sorted(to_be_written.items()))
    with open('Ordered_names.txt', 'w') as ord:
        for k,v in Ordered.items():
            for name in v:
                ord.write(str(k)  + " " + name + "\n")
            

email_files = [f'email-{i}.txt' for i in range(1,21)]
spam_emails = emails_without_wave_information(email_files)
print ("Emails that not contain wave information are :")
for email in spam_emails:
  print (spam_emails[email])
spam_emails.update(emails_without_daiictid(email_files))
print('Spam:', spam_emails.keys())
rename_files(spam_emails)

non_spam_emails = list(set(email_files).difference(set(spam_emails.keys())))
print('Non spam:', non_spam_emails)

generate_ordered_names(non_spam_emails)

