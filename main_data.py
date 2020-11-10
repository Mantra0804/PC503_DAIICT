import random
import os
from randomtimestamp import randomtimestamp

random.seed(53)

def initial_cleanup():
    to_be_kept = ['.git', '.gitignore', 'About-DAIICT.txt', 'main_data.py', 'main_test.py',  'readme.md', 'student_names_list.txt']
    to_be_deleted = set(os.listdir()).difference(to_be_kept)
    for file in to_be_deleted:
        os.remove(file)
    
def random_time():
    timestamp=randomtimestamp(2010,text=False)
    month = timestamp.strftime("%B") 
    year = timestamp.strftime("%Y")
    date = int(timestamp.strftime("%d"))     
    time = timestamp.strftime("%H")+":"+timestamp.strftime("%M")
    return str("Recieved at "+time+" hrs on "+month+" "+str(date)+", "+year+" from ")

def write_file(file_name, content):
    with open(file_name, 'w') as op:
        op.writelines(content) 

def filter_data(constraint, lst):
    string_filter = lambda string : False if string == "\n" else True
    lst = list(filter(constraint, list(filter(string_filter, lst))))
    return lst

def details_about_DAIICT():
    with open('./About-DAIICT.txt', 'r') as ad:
        lines       = ad.readlines()

        structure = {'start':0,'end': 0}

        history     = structure.copy()
        environment = structure.copy()
        recognition = structure.copy()
        accreditation = structure.copy()

        i = 0
        while i < len(lines):
            if lines[i] == 'History\n':
                history['start'] = i

            elif lines[i] == 'Environment\n':
                history['end'] = i-1
                environment['start'] = i

            elif lines[i] == 'Recognition\n':
                environment['end'] = i-1
                recognition['start'] = i

            elif lines[i] == 'Accreditation\n':
                recognition['end'] = i-1
                accreditation['start'] = i

            i += 1

        history_r = lines[history['start']:history['end']+1]
        write_file('History.txt', history_r)

        environment_r = lines[environment['start']:environment['end']+1]
        write_file('Environment.txt', environment_r)
        
        recognition_r = lines[recognition['start']:recognition['end']+1]
        write_file('Recognition.txt', recognition_r)

        accreditation_r = lines[accreditation['start']:]
        write_file('Accreditation.txt', accreditation_r)

        return {
            'history'      :     history_r, 
            'environment'  : environment_r, 
            'recognition'  : recognition_r, 
            'accreditation':accreditation_r
        }


def emails(student_name_list, random_email_files, content):

    history = content['history']
    environment = content['environment']
    recognition = content['recognition']
    accreditation = content['accreditation']

    for random_email_file in random_email_files:
        with open(random_email_file, 'w') as remail:

            history_s = random.choice(history)
            env_s = random.choice(environment)
            rec_s = random.choice(recognition)
            acc_s = random.choice(accreditation)

            remail.writelines([
                    f'{random_time()}{random.choice(student_name_list)}\n',
                    '\n',
                    history_s,
                    env_s,
                    rec_s,
                    acc_s
                ]
            )


def emails_original(content):

    content_l = content.copy()

    student_name_list = []
    with open('student_names_list.txt', 'r') as s:
        student_name_list = s.readlines()

    student_name_list = list(
        map(
            lambda string: string.replace("\n", "").replace(" ", "_") + "@daiict.ac.in", 
            student_name_list
        ))

    random_email_files = [
        f'email-{i}.txt' for i in random.sample(range(1, 21), 15)
    ]
    
    ready_to_go = lambda string: True
    content_l['environment']   = filter_data(ready_to_go, content_l['environment'])
    content_l['recognition']   = filter_data(ready_to_go, content_l['recognition'])
    content_l['accreditation'] = filter_data(ready_to_go, content_l['accreditation'])

    history_constraint = lambda string : True if (
            string.startswith('The first wave') or 
            string.startswith('The second wave') or 
            string.startswith('The third wave') or
            string.startswith('It was in the fourth wave')) else False

    content_l['history'] = filter_data(history_constraint, content_l['history'])
    emails(student_name_list, random_email_files, content_l)

    return random_email_files


def emails_with_modifications(content, files):

    content_l = content.copy()
 
    files = set(i for i in range(1,21)).difference(set(int(email.split('-')[1].split('.')[0]) for email in files))

    email_file_list = random.sample([f'email-{file}.txt' for file in files], 4)
    
    student_name_list = ['name1@gmail.com', 'A_X_y@yahoo.co.in', 'nm123@rediff.com', 'nam_4_e@160.com']

    ready_to_go = lambda string: True
    content_l['environment']   = filter_data(ready_to_go, content_l['environment'])
    content_l['recognition']   = filter_data(ready_to_go, content_l['recognition'])
    content_l['accreditation'] = filter_data(ready_to_go, content_l['accreditation'])

    history_constraint = lambda string : True if (
            string.startswith('The first wave') or 
            string.startswith('The second wave') or 
            string.startswith('The third wave') or
            string.startswith('It was in the fourth wave')) else False

    content_l['history'] = filter_data(history_constraint, content_l['history'])

    emails(student_name_list, email_file_list, content_l)

    return email_file_list

def email_with_another_modifications(content, files):

    content_l = content.copy()
 
    files = set(i for i in range(1,21)).difference(set(int(email.split('-')[1].split('.')[0]) for email in files))

    email_file_list = random.sample([f'email-{file}.txt' for file in files], 1)
    
    student_name_list = ['pc_503@daiict.ac.in']

    ready_to_go = lambda string: True
    content_l['environment']   = filter_data(ready_to_go, content_l['environment'])
    content_l['recognition']   = filter_data(ready_to_go, content_l['recognition'])
    content_l['accreditation'] = filter_data(ready_to_go, content_l['accreditation'])

    history_constraint = lambda string : True if not (
            string.startswith('The first wave') or 
            string.startswith('The second wave') or 
            string.startswith('The third wave') or
            string.startswith('It was in the fourth wave')) else False

    content_l['history'] = filter_data(history_constraint, content_l['history'])

    emails(student_name_list, email_file_list, content_l)
    return email_file_list

initial_cleanup()
content = details_about_DAIICT()
random_email_files = emails_original(content)
random_email_files = emails_with_modifications(content, random_email_files) + random_email_files
random_email_files = email_with_another_modifications(content, random_email_files) + random_email_files



