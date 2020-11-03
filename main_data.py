import random
import os

random.seed(53)

def details_about_DAIICT():
    with open('./About-DAIICT.txt', 'r') as ad:
        lines       = ad.readlines()

        structure = {'start':0,'end': 0}

        history     = structure.copy()
        environment = structure.copy()
        recognition = structure.copy()
        accredition = structure.copy()

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
                accredition['start'] = i

            i += 1

        with open('History.txt', 'w') as h:
            h.writelines(lines[history['start']:history['end']+1])

        with open('Environment.txt', 'w') as e:
            e.writelines(lines[environment['start']:environment['end']])

        with open('Recognition.txt', 'w') as r:
            r.writelines(lines[recognition['start']:recognition['end']])

        with open('Accreditation.txt', 'w') as a:
            a.writelines(lines[accredition['start']:])

def emails():
    student_name_list = []
    with open('student_names_list.txt', 'r') as s:
        student_name_list = s.readlines()

    student_name_list = list(map(lambda string: string.replace("\n", ""), student_name_list))

    string_filter = lambda string : False if string == "\n" else True

    recognition = []
    with open('Recognition.txt', 'r') as rec:
        recognition = list(filter(string_filter, rec.readlines()))

    environment = []
    with open('Environment.txt', 'r') as env:
        environment = list(filter(string_filter, env.readlines()))

    accreditation = []
    with open('Accreditation.txt', 'r') as acc:
        accreditation = list(filter(string_filter, acc.readlines()))

    history = []
    with open('History.txt', 'r') as hist:
        history = list(filter(string_filter, hist.readlines()))

    history = list(filter(
        lambda string : True if (
            string.startswith('The first wave') or 
            string.startswith('The second wave') or 
            string.startswith('The third wave') or
            string.startswith('It was in the fourth wave')
        ) else False, history))

    random_email_files = [
        f'email-{i}.txt' for i in random.sample(range(1, 21), 15)
    ]

    for random_email_file in random_email_files:
        with open(random_email_file, 'w') as remail:

            history_s = random.choice(history)
            env_s = random.choice(environment)
            rec_s = random.choice(recognition)
            acc_s = random.choice(accreditation)

            remail.writelines([
                    f'Recieved at 17:23 hrs on October 7, 2018 from {random.choice(student_name_list).replace(" ", "_")}@daiict.ac.in\n',
                    '\n',
                    history_s,
                    env_s,
                    rec_s,
                    acc_s
                ]
            )

def emails_with_modifications():
    files = list(filter(lambda string: True if string.startswith('email') else False, os.listdir())) 
    files = set(i for i in range(1,21)).difference(set(int(email.split('-')[1].split('.')[0]) for email in files))

    for file in files:
        with open(f'email-{file}.txt', 'w'):
            
emails_with_modifications()
