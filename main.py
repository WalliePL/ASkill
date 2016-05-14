"""
    This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
    The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
    as testing instructions are located at http://amzn.to/1LzFrj6

    For additional samples, visit the Alexa Skills Kit Getting Started guide at
    http://amzn.to/1LGWsLG
    """

from __future__ import print_function

import random
import re

""" from GameController import BaseGameExampleStrategy, GameConstroller
"""

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch

    return get_welcome_response()
    """return beginBaseQuiz(intent, session)"""

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print (intent_name)
    print (on_intent.gameStarted)
    # Dispatch to your skill's intent handlers
    if (on_intent.gameController == None):
        on_intent.gameController = InitializeGame()

    if on_intent.gameStarted:
        if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
            return handle_session_end_request()
        elif intent_name == "AnswearIntent":
            return on_intent.gameController.PlayGame(intent, session)
        elif intent_name == "StopIntent":
            return get_stop_response()
        else:
            cleanup()
            raise ValueError("Invalid intent when gameStarted true")
    else:
        if intent_name == "StartIntent":
            on_intent.gameStarted = True
            return on_intent.gameController.PlayGame(intent, session)
        elif intent_name == "StopIntent":
            return get_stop_response()
        else:
            cleanup()
            raise ValueError("Invalid intent")

on_intent.gameStarted = False
on_intent.gameController = None
on_intent.goodAnwer = ''

def beginBaseQuiz(intent, session):
    gameController = InitializeGame()
    return gameController.PlayGame(intent, session)

def InitializeGame():
    baseGameExampleStrategy = BaseGameExampleStrategy()
    return GameConstroller(baseGameExampleStrategy.PlayGame)

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
    cleanup()

def cleanup():
    on_intent.gameStarted = False
    on_intent.gameController = None
    on_intent.goodAnwer = ""

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Trivia Game. Say start to begin game, end to exit"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Say start to begin game, end to exit"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_stop_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    cleanup()
    session_attributes = {}
    card_title = "End"
    speech_output = "Game stopped."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for plaing the Alexa Hackathon Trivia Game. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}

def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

class Question:
    def __init__(self, questionType, question, rightAnswer, badAnswer):
        self.question = question
        self.rightAnswer = rightAnswer
        self.badAnswer = badAnswer
        self.questionType = questionType

class Questions:
    def __init__(self):
        self.Load()

    def Count(self):
        return self.questions.__len__()

    def Load(self):
        self.questions = []
        self.questions.append(Question("Movie", "How many oscars did the Titanic movie got?", "Eleven", "Five"))
        self.questions.append(Question("Movie", "How many Tomb Raider movies were made?", "Two", "Three"))
        self.questions.append(Question("Movie", "Which malformation did Marilyn Monroe have when she was born?", "Six toes", "Wings"))

    def GetQuestion(self):
        drawnQuestionId = random.randint(0, len(self.questions) - 1)
        print (drawnQuestionId)
        question = self.questions.pop(drawnQuestionId)
        return question

class Player:
    def __init__(self, startPoints = 0):
        self.points = startPoints

    def addPoints(self, pointsToAdd):
        self.points = self.points + pointsToAdd

class GameConstroller:
    def __init__(self, precessFunc):
        self.Users = []
        if precessFunc:
            self.precessFunc = precessFunc

    def StartGame(self):
        print("Start Game")

    def PlayGame(self, intent, session):
        return self.precessFunc(intent, session)

    def EndGame(self):
        print("EndGame")

class BaseGameExampleStrategy:
    def __init__(self):
        self.StateMachine = "Question"
        self.questions = Questions()
        self.score = 0

    def CheckAnswer(self, receivedAnswer):
        regex = re.compile('[^a-zA-Z]')
        receivedAnswer = regex.sub('', receivedAnswer)
        print(receivedAnswer.lower())
        print(on_intent.goodAnwer.lower())
        
        print(receivedAnswer.lower() == on_intent.goodAnwer.lower())
        return receivedAnswer.lower() == on_intent.goodAnwer.lower()

    def PlayGame(self, intent, session):
        session_attributes = {}
        reprompt_text = None

        if (self.questions.Count() == 0):
            self.endGame = True
            speech_output = self.validateAnswer(intent) + ". Your score is" + str(self.score) + ". No more questions. Game finished"
            should_end_session = True
            cleanup()
            return self.build_response(session_attributes, self.build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))

        if self.StateMachine == "Question":
            question =  self.questions.GetQuestion()
            speech_output = "To answer use phrase, my answer is a or b. First question. " + self.CreateQuestion(question)
            should_end_session = False

            self.StateMachine = "Answer"
            return self.build_response(session_attributes, self.build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))
        elif self.StateMachine == "Answer":
            self.endGame = False
            speech_output = self.validateAnswer(intent)
            if(not self.endGame):
                question =  self.questions.GetQuestion()
                questionoutput = self.CreateQuestion(question)
                should_end_session = False
                reprompt_text = questionoutput
                speech_output = speech_output + ". Next question, " + questionoutput
            else:
                speech_output = speech_output + ". Your score is" + str(self.score)
                should_end_session = True
                cleanup()

            return self.build_response(session_attributes,
                                       self.build_speechlet_response(intent['name'], speech_output, reprompt_text,
                                                                     should_end_session))

        else:
            speech_output = "You said unacceptable answer. You can answer by saying My answer is A or My answer is ."
            reprompt_text = "You can answer by saying My answer is A or My answer is."
            should_end_session = False
            return self.build_response(session_attributes,
                                       self.build_speechlet_response(intent['name'], speech_output, reprompt_text,
                                                                     should_end_session))
    def validateAnswer(self, intent):
        if 'Answer' in intent['slots']:
            answer = intent['slots']['Answer']['value']
            print("value " + answer)
            if(self.CheckAnswer(answer) == True):
                result = "Correct"
                self.score = self.score + 1
            else:
                self.endGame = True
                result = "Incorrect"

            return "Your answer is "+result


    def CreateQuestion(self, question):
        firstOption = random.randint(0, 1)
        if firstOption:
            on_intent.goodAnwer = "a"
            return question.question + "A," + question.rightAnswer + ", B, " + question.badAnswer
        else:
            on_intent.goodAnwer = "b"
            return question.question + "A," + question.badAnswer + ", B, " + question.rightAnswer

    def build_speechlet_response(self, title, output, reprompt_text, should_end_session):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': 'SessionSpeechlet - ' + title,
                'content': 'SessionSpeechlet - ' + output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }

    def build_response(self, session_attributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }

class DemoGameExampleStrategy:
    def PlayGame(self,intent, session):
        print("DemoGameExampleStrategy StartGame")

class MaxPoinstStrategy:
    def PlayGame(self,intent, session):
        print("MaxPoinstStrategy StartGame")