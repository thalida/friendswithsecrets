# Builtins
import logging
from pprint import pprint

# Third Party
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_cors import CORS

# Custom
import people
import spreadsheet
from thread import Thread

logger = logging.getLogger(__name__)
app = Flask(
    __name__,
    static_folder="./dist/static",
    template_folder="./dist"
)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

google_client = spreadsheet.create_gc()

realSession = [
    {'sender': 'robyn', 'message_text': 'hi, jennifer. are you around to talk?'},
    {'sender': 'jennifer', 'message_text': 'Hi, Robyn! Yes. What types of things should I know before we begin?'},
    {'sender': 'robyn', 'message_text': 'ok. some things about me... umm, well. i can kind of be an anxious person, i guess. i\'ve been previously diagnosed with a depersonalization… disorder thing? i don’t know where else to begin.'},
    {'sender': 'robyn', 'message_text': 'oh. i also have this annoying tendency to spiral at night but am trying to keep it more together.'},
    {'sender': 'jennifer', 'message_text': 'Could you tell me a little bit about yourself? What you do, what a typical day is like, etc?'},
    {'sender': 'robyn', 'message_text': 'a typical day involves waking up, heading into work, and then either going home or grabbing a drink with a friend.'},
    {'sender': 'jennifer', 'message_text': 'How long have you been diagnosed with that disorder? Have there been things in therapy that have worked well for you before? Things that you\'ve hated?'},
    {'sender': 'robyn', 'message_text': 'i\'ve felt depressed and have had anxiety on and off since I was young. last year i was diagnosed with the depersonalization thing. after a while of having walls up for so long i just stopped feeling like it was my body i was experiencing life in. i think i might have some trauma. i guess i don’t know where to begin.'},
    {'sender': 'jennifer', 'message_text': 'Talking is a great place to start -- even if it\'s just to have someone neutral to bounce ideas off of when you need to. That\'s what I\'m here for!'},
    {'sender': 'jennifer', 'message_text': 'I’m wondering if there is one that is "more" of a priority -- there\'s a lot of layers to each of the topics that you’ve mentioned!'},
    {'sender': 'robyn', 'message_text': 'i wonder if it\'s just best to begin on background? maybe i can just answer some questions?'},
    {'sender': 'jennifer', 'message_text': 'Sure -- so you\'ve been in therapy before? Why don\'t you tell me a little bit about yourself -- who you are, where you\'re from, etc'},
    {'sender': 'jennifer', 'message_text': 'What\'s bringing you into online therapy? Do you see an outside therapist? Take any medications? Live with people?'},
    {'sender': 'robyn', 'message_text': 'well, my name is robyn. i was born in ohio but i grew up in maine. i\'ve been a lot of things. historically i\'ve very much aligned who i am with work but i know i’m more than that. i also know my problems are deeper than like just work?'},
    {'sender': 'robyn', 'message_text': 'i live alone, in brooklyn.'},
    {'sender': 'robyn', 'message_text': 'i don’t take any medication.'},
    {'sender': 'jennifer', 'message_text': 'Who is in your support system?'},
    {'sender': 'robyn', 'message_text': 'the internet? '},
    {'sender': 'robyn', 'message_text': 'i\'ve got good friends.'},
    {'sender': 'robyn', 'message_text': 'i like to keep people at a distance.'},
    {'sender': 'jennifer', 'message_text': 'Why do you think it\'s hard to let people in?'},
    {'sender': 'robyn', 'message_text': 'i wish i knew'},
    {'sender': 'jennifer', 'message_text': 'It sounds like you have minimal family support? Friends that are more like family?'},
    {'sender': 'robyn', 'message_text': 'i\'m pretty close with my mother now - but it\'s a recent development. everything else is minimal, yeah.'},
    {'sender': 'robyn', 'message_text': 'letting people in feels complicated. i don\'t know. i guess i\'ve been hurt. isn\'t that why anyone won\'t let someone in?'},
    {'sender': 'jennifer', 'message_text': 'Normally, I would say yes. But sometimes there are organic reasons (especially with a depersonalization history) that can create difficulty in connecting with others'},
    {'sender': 'jennifer', 'message_text': 'When/who diagnosed you or started to talk with you about the depersonalization/derealization?'},
    {'sender': 'robyn', 'message_text': 'i thought that was going on for a while but it wasn\'t until last year i saw a therapist and she confirmed depersonalization stuff.'},
    {'sender': 'jennifer', 'message_text': 'How did you start to realize that it was happening?'},
    {'sender': 'robyn', 'message_text': 'well. hmm. ok, i think that for me there are just so many things from the past that i feel like i\'m still paying for. it\'s like i\'m always on fucking edge. then one day i just started feeling like i wasn\'t even living in the world anymore. it was like audio was playing over the speakers and i knew the sound was supposed to be bright but all i could hear was muffled sound.'},
    {'sender': 'jennifer', 'message_text': 'What was growing up sort of like? Your first listed topic is background/identity -- how do you identify yourself?'},
    {'sender': 'robyn', 'message_text': 'uh what do you mean by how do i identify myself?'},
    {'sender': 'jennifer', 'message_text': 'Some people identify themselves by their jobs -- but each of us have a lot of different "parts" that are connected and make us who we are -- are you able to identify some of your "parts" or pieces of your identity?'},
    {'sender': 'robyn', 'message_text': 'hmm'},
    {'sender': 'robyn', 'message_text': 'i feel like i know how to answer this question but i don\'t want to just yet'},
    {'sender': 'jennifer', 'message_text': 'OK -- that certainly is within your right and your powers. How did you get into your career?'},
    {'sender': 'robyn', 'message_text': 'well'},
    {'sender': 'robyn', 'message_text': 'i accidentally graduated high school early and started working late nights at a fast food place. i used to get off work and my mind would just be running miles and i couldn\'t sleep, i couldn\'t do anything but focus on my problems, you know? so, i started just fiddling with design as this way to like focus on something else.'},
    {'sender': 'robyn', 'message_text': 'then i just became obsessed with it. i wanted to learn and do every in and out of it. it just became this perfect distraction.'},
    {'sender': 'jennifer', 'message_text': 'seems like a positive way to identify and distract yourself -- before we get too far into anything, do you have any history of self harm? suicidal thoughts or actions?'},
    {'sender': 'robyn', 'message_text': 'umm. yes.'},
    {'sender': 'jennifer', 'message_text': 'One? Both? Frequently?'},
    {'sender': 'robyn', 'message_text': 'i mean. i haven\'t been suicidal in a while. but there were a few attempts in my early-mid twenties.'},
    {'sender': 'robyn', 'message_text': 'self-harm is a bit more casual'},
    {'sender': 'jennifer', 'message_text': 'Serious attempts? Hospitalized as a result?'},
    {'sender': 'robyn', 'message_text': 'there was one or two serious attempts that resulted in hospitalization but i\'m not sure at the time that i understood they were serious'},
    {'sender': 'jennifer', 'message_text': 'What types of things normally bring about the current bouts of self harm?'},
    {'sender': 'robyn', 'message_text': 'i spiral at night'},
    {'sender': 'robyn', 'message_text': 'during the day i have goals and life and meetings and everything but at night when i\'m alone i just start thinking about everything and it hurts'},
    {'sender': 'jennifer', 'message_text': 'What is "everything" consist of?'},
    {'sender': 'robyn', 'message_text': '\'everything\' consists of a lot. i have the things that i focus on but i don\'t even know if they\'re my problem anymore or if i\'ve just romanticized them to not focus on whatever the \'real\' problem is but i don\'t know what the real problem is. does that make any sense?'},
    {'sender': 'jennifer', 'message_text': 'It does.'},
    {'sender': 'robyn', 'message_text': 'i\'m starting to think that trauma has layers.'},
    {'sender': 'jennifer', 'message_text': 'Trauma absolutely has layers.'},
    {'sender': 'robyn', 'message_text': 'i wish i could just find the root without having to swim through all the other bad experiences.'},
    {'sender': 'jennifer', 'message_text': 'What types of things do you feel like you spend the most amount of time focusing on (even if they\'re distractions)?'},
    {'sender': 'robyn', 'message_text': 'it\'s almost always been design but lately i just don\'t care about it anymore.'},
    {'sender': 'robyn', 'message_text': 'i\'ve picked up guitar in the last couple years. i also like writing. and i get really into watching basketball too. in the summer i bike a lot.'},
    {'sender': 'jennifer', 'message_text': 'Intriguing that the things that you like to spend time on are also causing you stress and anxiety at night?'},
    {'sender': 'robyn', 'message_text': 'vices'},
    {'sender': 'jennifer', 'message_text': 'Indeed.'},
    {'sender': 'jennifer', 'message_text': 'Are there things you want to be spending more time on?'},
    {'sender': 'jennifer', 'message_text': 'Or thinking more consistently about?'},
    {'sender': 'robyn', 'message_text': 'there are a few things that i think about every single day'},
    {'sender': 'robyn', 'message_text': 'i\'d like to stop i just don\'t know how. i wish i did.'},
    {'sender': 'jennifer', 'message_text': 'Are they anxious thoughts? Depressive thoughts? Anything specific?'},
    {'sender': 'robyn', 'message_text': 'yes. ok, i tried to talk around this all session but the more i think about it the more i realize i can\'t talk to you about the things we should be talking about without giving you context on a thing that i\'ve already worked through but is part of my identity.'},
    {'sender': 'robyn', 'message_text': 'i\'m trans'},
    {'sender': 'robyn', 'message_text': 'and trust me, it\'s a thing i\'ve worked through. we don’t have to go into it. it\'s not a thing i need to necessarily talk about i\'m just telling you for context.'},
    {'sender': 'jennifer', 'message_text': 'OK -- it helps the context and the information'},
    {'sender': 'jennifer', 'message_text': 'Why did you feel like you needed to talk around that ?'},
    {'sender': 'robyn', 'message_text': 'i think for better or worse it changes everything'},
    {'sender': 'jennifer', 'message_text': 'Why do you think that?'},
    {'sender': 'robyn', 'message_text': 'if we were interacting in real life, you\'d know i\'m trans. and consciously or subconsciously our dynamic would change. it does with everyone. i guess i\'d just feel like i\'m lying to you if i didn\'t tell you. it also - it also just. not the identity itself but moments in life filtered through that lens is what makes everything hurt more.'},
    {'sender': 'jennifer', 'message_text': 'I can appreciate that the dynamic can certainly change with those you interact with. I would hope that with a therapist that the dynamic wouldn\'t change in a way that would make you feel uncomfortable or unsafe in any way.'},
    {'sender': 'robyn', 'message_text': 'i mean. i think with everyone, therapist or not, i\'m kind of looking out for if they can hurt me. and if they can, how can i go about protecting myself. trust is hard for me.'},
    {'sender': 'jennifer', 'message_text': 'Always feeling like you need to be on the lookout can certainly impact how you interact with the rest of the world'},
    {'sender': 'jennifer', 'message_text': 'And can definitely impact how you engage with your surroundings or your activities/life'},
    {'sender': 'robyn', 'message_text': 'you know how when you\'re in a situation that makes you feel a little bit uncomfortable you kind of go into a fight or flight mode? i\'m that way 24/7.'},
    {'sender': 'jennifer', 'message_text': 'So we are just about out of time, but I can certainly appreciate that the impact of feeling like you need to be in fight/flight mode would impact how you are able to interact or perceive your surroundings.'},
    {'sender': 'robyn', 'message_text': 'is it ok if i set up another session?'},
    {'sender': 'jennifer', 'message_text': 'Absolutely.'},
    {'sender': 'robyn', 'message_text': 'also, what do i do if i spiral at night? should i send a message on here?'},
    {'sender': 'jennifer', 'message_text': 'Using Lifeline or any other emergency service if you need something and are in a crisis and need to talk to someone will be important if you need it. I look forward to continuing getting to know you, Robyn!'},
    {'sender': 'robyn', 'message_text': 'thanks'},
]

threads = {
    'akilah': [
        [{'sender': 'akilah' if message['sender'] is 'robyn' else 'deb', 'message_text': message['message_text']} for index, message in enumerate(realSession) if index > 10 and index <= 30],
        [{'sender': 'akilah' if message['sender'] is 'robyn' else 'deb', 'message_text': message['message_text']} for index, message in enumerate(realSession) if index < 10],
        [{'sender': 'akilah' if message['sender'] is 'robyn' else 'deb', 'message_text': message['message_text']} for index, message in enumerate(realSession) if index > 30],
    ],
    'robyn': [
        realSession,
        [message for index, message in enumerate(realSession) if index > 5 and index <= 20],
        [message for index, message in enumerate(realSession) if index > 20 and index <= 45],
    ],
    'timothy': [
        [{'sender': 'timothy' if message['sender'] is 'robyn' else 'april', 'message_text': message['message_text']} for index, message in enumerate(realSession) if index > 15 and index <= 20],
        [{'sender': 'timothy' if message['sender'] is 'robyn' else 'april', 'message_text': message['message_text']} for index, message in enumerate(realSession) if index > 30 and index <= 35],
        [{'sender': 'timothy' if message['sender'] is 'robyn' else 'april', 'message_text': message['message_text']} for index, message in enumerate(realSession) if index > 35],
    ],
}

def get_n_thread_sessions(person, num_sessions):
    thread = Thread(google_client, person)
    return thread.get_n_sessions(num_sessions)

@app.route('/api/thread/<string:person>', methods=['GET'])
def get_thread(person):
    try:
        res = {
            'sessions': get_n_thread_sessions(person, 10),
            'participant': people.PARTICIPANTS[person],
            'therapist': people.PARTICIPANT_TO_THERAPIST[person],
        }
        return make_response(jsonify(res))
    except Exception:
        logger.exception('500 Error Fetching Thread Data')
        abort(500)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
