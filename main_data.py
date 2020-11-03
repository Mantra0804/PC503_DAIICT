import random
import os

random.seed(53)

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

        environment_r = lines[environment['start']:environment['end']]
        write_file('Environment.txt', environment_r)
        
        recognition_r = lines[recognition['start']:recognition['end']]
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
                    f'Recieved at 17:23 hrs on October 7, 2018 from {random.choice(student_name_list)}\n',
                    '\n',
                    history_s,
                    env_s,
                    rec_s,
                    acc_s
                ]
            )


def emails_original(content):
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
    content['environment']   = filter_data(ready_to_go, content['environment'])
    content['recognition']   = filter_data(ready_to_go, content['recognition'])
    content['accreditation'] = filter_data(ready_to_go, content['accreditation'])

    history_constraint = lambda string : True if (
            string.startswith('The first wave') or 
            string.startswith('The second wave') or 
            string.startswith('The third wave') or
            string.startswith('It was in the fourth wave')) else False

    content['history'] = filter_data(history_constraint, content['history'])
    emails(student_name_list, random_email_files, content)


def emails_with_modifications(content):
    files = list(filter(lambda string: True if string.startswith('email') else False, os.listdir())) 
    files = set(i for i in range(1,21)).difference(set(int(email.split('-')[1].split('.')[0]) for email in files))

    email_file_list = [f'email-{file}.txt' for file in files]
    
    student_name_list = ['name1@gmail.com', 'A_X_y@yahoo.co.in', 'nm123@rediff.com', 'nam_4_e@160.com']

    ready_to_go = lambda string: True
    content['environment']   = filter_data(ready_to_go, content['environment'])
    content['recognition']   = filter_data(ready_to_go, content['recognition'])
    content['accreditation'] = filter_data(ready_to_go, content['accreditation'])

    history_constraint = lambda string : True if (
            string.startswith('The first wave') or 
            string.startswith('The second wave') or 
            string.startswith('The third wave') or
            string.startswith('It was in the fourth wave')) else False

    content['history'] = filter_data(history_constraint, content['history'])

    emails(student_name_list, email_file_list, content)

content = details_about_DAIICT()
emails_original(content)
emails_with_modifications(content)