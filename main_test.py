import os
from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

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

def gen_timestamp_name_dict(to_be_written, line):
    content = line.split()
    t_d, name = time_to_timestamp(content[2:8]), content[-1]
    if to_be_written.get(t_d):
        to_be_written[t_d].append(name)
    else:
        to_be_written[t_d] = [name.split('@')[0].replace("_", " ")]

# trial function - to remove redundant names mapped on different timestamps - can be optimized
def get_unique_dict(to_be_written):
    reverse_dict = dict()
    to_be_returned = dict()
    for k, v in to_be_written.items():
        for name in v:
            if reverse_dict.get(name):
                reverse_dict[name].append(k)
            else:
                reverse_dict[name] = [k]

    for k, v in reverse_dict.items():
        reverse_dict[k]= sorted(v)[-1]
    
    for k,v in reverse_dict.items():
        if to_be_returned.get(v):
            to_be_returned[v].append(k)
        else:
            to_be_returned[v] = [k]

    return to_be_returned



def write_ordered_dict(file, to_be_written, asc):
    if asc:
        Ordered = OrderedDict(sorted(to_be_written.items()))
    else:
        Ordered = OrderedDict(reversed(sorted(to_be_written.items())))
    
    with open(file, 'w') as ord:
        for k,v in Ordered.items():
            for name in v:
                ord.write(str(k)  + " " + name + "\n")    


def generate_ordered_names(lst):
    to_be_written = dict()
    for file in lst:
        with open(file, 'r') as fl:
            line = fl.readline()
            gen_timestamp_name_dict(to_be_written, line)

    write_ordered_dict('Ordered_names.txt', to_be_written, True)

            
def generate_ordered_names_wave(lst):
    to_be_written_f1 = dict()
    to_be_written_f2 = dict()
    to_be_written_f3 = dict()
    to_be_written_f4 = dict()
    for file in lst:
        with open(file, 'r') as f1:
            line = f1.readline()
            content = f1.read()
            if content.find("first wave") != -1:
                gen_timestamp_name_dict(to_be_written_f1, line)
            elif content.find("second wave") != -1:
                gen_timestamp_name_dict(to_be_written_f2, line)
            elif content.find("third wave") != -1:
                gen_timestamp_name_dict(to_be_written_f3, line)
            elif content.find("fourth wave") != -1:
                gen_timestamp_name_dict(to_be_written_f4, line)

    ordered_names_wave1 = get_unique_dict(to_be_written_f1)
    ordered_names_wave2 = get_unique_dict(to_be_written_f2)
    ordered_names_wave3 = get_unique_dict(to_be_written_f3)
    ordered_names_wave4 = get_unique_dict(to_be_written_f4)

    write_ordered_dict("ordered_names_wave1.txt", get_unique_dict(to_be_written_f1), False)
    write_ordered_dict("ordered_names_wave2.txt", get_unique_dict(to_be_written_f2), False)
    write_ordered_dict("ordered_names_wave3.txt", get_unique_dict(to_be_written_f3), False)
    write_ordered_dict("ordered_names_wave4.txt", get_unique_dict(to_be_written_f4), False)

    return ordered_names_wave1, ordered_names_wave2, ordered_names_wave3, ordered_names_wave4

def construct_BarPlot(ordered_names_wave1, ordered_names_wave2, ordered_names_wave3, ordered_names_wave4, spam_emails):
    number_of_wave1 = len(ordered_names_wave1)
    number_of_wave2 = len(ordered_names_wave2)
    number_of_wave3 = len(ordered_names_wave3)
    number_of_wave4 = len(ordered_names_wave4)
    number_of_spam = len(spam_emails)

    x = ['1st wave', '2nd wave', '3rd wave', '4th wave', 'Spam mails']
    y = [number_of_wave1, number_of_wave2, number_of_wave3, number_of_wave4, number_of_spam]

    xpos = np.arange(len(x))

    plt.bar(xpos,y)
    plt.xticks(xpos,x)
    plt.xlabel('Students category containing')
    plt.ylabel('Number of students')
    plt.title('Category vs Number of students')
    plt.show()
    plt.savefig('BarPlot.png')

email_files = [f'email-{i}.txt' for i in range(1,21)]

# TASK 9 - emails_without_wave_info => returns those files
spam_emails = emails_without_wave_information(email_files)
print ("Emails that not contain wave information are :")
for email in spam_emails:
  print (spam_emails[email])

#TASK 10 - emails_without_daiictid -> rename_files => update  spam with non-DA id, rename files
spam_emails.update(emails_without_daiictid(email_files))
print('Spam:', spam_emails.keys())
rename_files(spam_emails)

non_spam_emails = list(set(email_files).difference(set(spam_emails.keys())))
print('Non spam:', non_spam_emails)

#TASK 11 - gen_ordered_names -> gen_timestamp -> time_2_timestamp => create ordered_names.txt
generate_ordered_names(non_spam_emails)

# TASK 12 - gen_ordered_names_wave -> (gen_timestamp -> time2timestamp) -> get_unique_dict => 4 files created
ordered_names_wave1, ordered_names_wave2, ordered_names_wave3, ordered_names_wave4 = generate_ordered_names_wave(non_spam_emails)

#TASK 13 - construct_barplot
construct_BarPlot(ordered_names_wave1, ordered_names_wave2, ordered_names_wave3, ordered_names_wave4, spam_emails)