import os

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

email_files = [f'email-{i}.txt' for i in range(1,21)]
spam_emails = emails_without_wave_information(email_files)
print ("Emails that not contain wave information are :")
for email in spam_emails:
  print (spam_emails[email])
spam_emails.update(emails_without_daiictid(email_files))
rename_files(spam_emails)
