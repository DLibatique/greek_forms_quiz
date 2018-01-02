import os
import random
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

verbs = [
    ['ἄγω', 'ἄγεις', 'ἄγει', 'ἄγομεν', 'ἄγετε', 'ἄγουσι(ν)', 'ἄγομαι', 'ἄγῃ', 'ἄγεται', 'ἀγόμεθα', 'ἄγεσθε', 'ἄγονται', 'ἦγον', 'ἦγες', 'ἦγε(ν)', 'ἤγομεν', 'ἤγετε', 'ἦγον', 'ἠγόμην', 'ἤγου', 'ἤγετο', 'ἠγόμεθα', 'ἤγεσθε', 'ἤγοντο', 'ἄξω', 'ἄξεις', 'ἄξει', 'ἄξομεν', 'ἄξετε', 'ἄξουσι(ν)', 'ἄξομαι', 'ἄξῃ', 'ἄξεται', 'ἀξόμεθα', 'ἄξεσθε', 'ἄξονται', 'ἤγαγον', 'ἤγαγες', 'ἤγαγε(ν)', 'ἠγάγομεν', 'ἠγάγετε', 'ἤγαγον', 'ἠγαγόμην', 'ἤγαγου', 'ἠγάγετο', 'ἠγαγόμεθα', 'ἠγάγεσθε', 'ἠγάγοντο', 'ἦχα', 'ἦχας', 'ἦχε(ν)', 'ἤχαμεν', 'ἤχατε', 'ἤχασι(ν)', 'ἤχη', 'ἤχης', 'ἤχει(ν)', 'ἤχεμεν', 'ἤχετε', 'ἤχεσαν', 'ἦγμαι', 'ἦξαι', 'ἦκται', 'ἤγμεθα', 'ἦχθε', 'ἠγμένοι εἰσι(ν)', 'ἤγμην', 'ἦξο', 'ἦκτο', 'ἤγμεθα', 'ἦχθε', 'ἠγμένοι ἦσαν', 'ἦχθην', 'ἤχθης', 'ἤχθη', 'ἤχθημεν', 'ἤχθητε', 'ἤχθησαν', 'ἀχθήσομαι', 'ἀχθήσῃ/ήσει', 'ἀχθήσεται', 'ἀχθησόμεθα', 'ἀχθήσεσθε', 'ἀχθήσονται'],
    ['βαίνω', 'βαίνεις', 'βαίνει', 'βαίνομεν', 'βαίνετε', 'βαίνουσι(ν)', 'ἔβαινον', 'ἔβαινες', 'ἔβαινε(ν)', 'ἐβαίνομεν', 'ἐβαίνετε', 'ἔβαινον', 'βήσομαι', 'βήσῃ', 'βήσεται', 'βησόμεθα', 'βήσεσθε', 'βήσονται', 'ἔβην', 'ἔβης', 'ἔβη', 'ἔβημεν', 'ἔβητε', 'ἔβησαν', 'βέβηκα', 'βέβηκας', 'βέβηκε(ν)', 'βεβήκαμεν', 'βεβήκατε', 'βεβήκασι(ν)', 'ἐβεβήκη', 'ἐβεβήκης', 'ἐβεβήκει(ν)', 'ἐβεβήκεμεν', 'ἐβεβήκετε', 'ἐβεβήκεσαν'],
    ['βάλλω', 'βάλλεις', 'βάλλει', 'βάλλομεν', 'βάλλετε', 'βάλλουσι(ν)', 'βάλλομαι', 'βάλλῃ', 'βάλλεται', 'βαλλόμεθα', 'βάλλεσθε', 'βάλλονται', 'ἔβαλλον', 'ἔβαλλες', 'ἔβαλλε(ν)', 'ἐβάλλομεν', 'ἐβάλλετε', 'ἔβαλλον', 'ἐβαλλόμην', 'ἐβάλλου', 'ἐβάλλετο', 'ἐβαλλόμεθα', 'ἐβάλλεσθε', 'ἐβάλλοντο', 'βαλῶ', 'βαλεῖς', 'βαλεῖ', 'βαλοῦμεν', 'βαλεῖτε', 'βαλοῦσι(ν)', 'βαλοῦμαι', 'βαλῇ', 'βαλεῖται', 'βαλούμεθα', 'βαλεῖσθε', 'βαλοῦνται', 'ἔβαλον', 'ἔβαλες', 'ἔβαλε(ν)', 'ἐβάλομεν', 'ἐβάλετε', 'ἔβαλον', 'ἐβαλόμην', 'ἐβάλου', 'ἐβάλετο', 'ἐβαλόμεθα', 'ἐβάλεσθε', 'ἐβάλοντο', 'βέβληκα', 'βέβληκας', 'βέβληκε(ν)', 'βεβλήκαμεν', 'βεβλήκατε', 'βεβλήκασι(ν)', 'ἐβεβλήκη', 'ἐβεβλήκης', 'ἐβεβλήκει(ν)', 'ἐβεβλήκεμεν', 'ἐβεβλήκετε', 'ἐβεβλήκεσαν', 'βέβλημαι', 'βέβλησαι', 'βέβληται', 'βεβλήμεθα', 'βέβλησθε', 'βέβληνται', 'ἐβεβλήμην', 'ἐβέβλησο', 'ἐβέβλητο', 'ἐβεβλήμεθα', 'ἐβέβλησθε', 'ἐβέβληντο', 'ἐβλήθην', 'ἐβλήθης', 'ἐβλήθη', 'ἐβλήθημεν', 'ἐβλήθητε', 'ἐβλήθησαν', 'βληθήσομαι', 'βληθήσῃ/ήσει', 'βληθήσεται', 'βληθησόμεθα', 'βληθήσεσθε', 'βληθήσονται'],
    ['δίδωμι', 'δώσω', 'ἔδωκα', 'δέδωκα', 'δέδομαι', 'ἐδόθην'],
    ['ἔρχομαι', 'ἐλεύσομαι', 'ἦλθον', 'ἐλήλυθα', None, None],
    ['ἔχω', 'ἕξω', 'ἔσχον', 'ἔσχηκα', None, None],
    ['ἵστημι', 'στήσω', 'ἔστην/ἔστησα', 'ἕστηκα', 'ἕσταμαι', 'ἐστάθην'],
    ['ὁράω', 'ὄψομαι', 'εἶδον', 'ἑώρακα', 'ὦμμαι', 'ὤφθην'],
    ['τίθημι', 'θήσω', 'ἔθηκα', 'τέθεικα', 'τέθειμαι', 'ἐτέθην'],
    ['φημί', 'φήσω', 'ἔφησα', None, None, None]
]

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/quiz', methods = ['POST'])
def choose_number():
    number = request.form['number']
    print("Your answer was " + number + "questions.")
    return redirect('/')
'''
def index():

    def quiz():

        verbs = random.sample(verbs, len(verbs))

        no_of_questions = input('How many verbs would you like to quiz yourself on? --> ')

        while int(no_of_questions) > len(verbs):
            no_of_questions = input('You can choose up to ' + str(len(verbs)) + ' verbs. Choose again! --> ')

        incorrect = []
        correct = []
        for verb in verbs[0:int(no_of_questions)]:

            random_pp = verb[random.randint(1,int(len(verb)-1))]

            while random_pp == None:
                random_pp = verb[random.randint(1,int(len(verb)-1))]

            answer = input('What is the first principal part of ' + random_pp + '? --> ')

            while answer != verb[0]:
                if answer == 'I give up.':
                    print('οἴμοι! The correct answer is ' + str(verb[0]) + '.')
                    if verb[0] not in incorrect:
                        incorrect.append(verb[0])
                    break
                else:
                    if verb[0] not in incorrect:
                        incorrect.append(verb[0])
                    answer = input('οἴμοι! Try again! --> ')
            else:
                print('εὖγε!')
            
                if verb[0] not in incorrect:
                    correct.append(verb[0])
                pass

        print("You need to brush up on the following verbs: ",str(set(incorrect)))
        print("You got the following verbs correct: ",str(set(correct)))

    return quiz()
'''
if __name__ == '__main__':
    app.run()    