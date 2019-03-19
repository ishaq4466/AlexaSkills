
import json

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            'ssml': "<speak>" +output +"</speak>"
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
            "type": "SSML",
            'ssml': "<speak>" +output +"</speak>"
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
ONE = "Think a number in between one to ten <break time=\"500ms\"/>, and keep that number in mind<break time=\"500ms\"/>, dont tell it to anyone.<amazon:effect name=\"whispered\">I know<break time=\"500ms\"/> what you have thaught<break time=\"500ms\"/> I will reveal it at the end dont worry!<break time=\"500ms\"/></amazon:effect>. Now say next to proceed, and remember <break time=\"500ms\"/> in each step you have to say next keyword"
TWO = "Now, double that number which is in your mind."
THREE = "Simply, add five, to the total which you had, after you had doubled that number."
FOUR="Multiply the new total by fifty, do it very carefully, you can take the help of calculator.<break time=\"500ms\"/> Also if you wish than you can ask me to repeat"
FIVE = "Listen this step carefully,Ok! , if you already celebrated your birthday this year<break time=\"500ms\"/>, than add 1768 to the total which you got<break time=\"500ms\"/>, after multiplying by fifty<break time=\"500ms\"/>, or else, add  1767."
SIX = "Now<break time=\"500ms\"/> here's the magic happens, subtract from your total the year in which you were born.<break time=\"500ms\"/> For example, if you born in year 1997, and your total is 2318,<break time=\"500ms\"/> than substract 1997, from 2318."

stepDict = {"step":[ONE,TWO,THREE,FOUR,FIVE,SIX]}

def get_welcome_response():
    session_attributes = {"step_Number":0}
    card_title = "Age Predictor"
    speech_output = "Welcome to age predictor game.<break time=\"500ms\"/>I will guess your real age, you just  have to follow my instructions,<break time=\"500ms\"/>are you ready to begin?"
    reprompt_text = "Reply with yes to continue <break time=\"500ms\"/> or else reply repeat to hear again."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def yes_func():
    session_attributes = {"step_Number":0}
    card_title = "Game started"
    reprompt_text = "Reply with next to continue <break time=\"500ms\"/> or else reply repeat to hear again."
    should_end_session = False
    speech_output = "Great! Here are some tips before playing the game, you might have to use calculator for some small calculation<break time=\"500ms\"/> and please do remember that<break time=\"500ms\"/> after each step you are asked to say \"Next\" keyword for continuing with next step .<break time=\"500ms\"/>For proceeding the game now<break time=\"500ms\"/> say \"Next\" or for any help say \"help.\" "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_help_request():
    
    card_title = "Help"
    reprompt_text = "Please reply yes to continue or stop to exit"
    should_end_session = False
    speech_output = "Ok, here are some helping tips for playing the game, there wil be six questions in each steps, you will be asked to do some math task, after each step you will be ask to say Next for the next step, if you did not understand the step properly than you can repeat that step by saying repeat, you can also exit the skill by saying stop. If you got it and want to begin than reply yes, or else reply with repeat for listening the help again"
    session_attributes = {"speech_output":speech_output,
        "reprompt_text":reprompt_text
        }
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

    
    
def handle_repeat_request(intent, session):
    # """
    # Repeat the previous speech_output and reprompt_text from the session['attributes'].
    # If available, else start a new game session.
    # """
    if 'attributes' not in session or 'speech_output' not in session['attributes']:
        return get_welcome_response()
    else:
        attributes = session['attributes']
        speech_output ="Ok, repeating again, " + attributes['speech_output'] + "<break time=\"500ms\"/>now reply with next keyword for continuing the next step."
        reprompt_text = attributes['reprompt_text']
        should_end_session = False
        card_title="repeating the step"
        return build_response(
            attributes,
            build_speechlet_response(card_title,speech_output, reprompt_text, should_end_session)
        )
        
def handle_next_request(intent,session):
    session_attributes = {}
    card_title = "Game steps"
    reprompt_text = "Reply with next to continue <break time=\"500ms\"/> or else reply repeat to hear again."
    should_end_session = False
    current_step = int(session['attributes']['step_Number'])
    stepNum = current_step
    if stepNum == 0:
        say = stepDict["step"][stepNum]
        speech_output = "Okay! so here we begin. " + say 
        stepNum = stepNum+1
        session_attributes = {"speech_output":speech_output,
        "reprompt_text":reprompt_text,
        "step_Number":stepNum}
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    elif stepNum==6:
        LASTSTEP="Finally, you will be having a three digit number<break time=\"500ms\"/>, the first number is the one<break time=\"500ms\"/> which you have chosen at the beginning<break time=\"500ms\"/> and the remaining two numbers are your age.<break time=\"500ms\"/>"
        LAST = "<say-as interpret-as=\"interjection\">wow</say-as><break time=\"500ms\"/> right, if you are amazed by me than you can try me again, by replying me yes or for any feedback you can mail me at <break time=\"300ms\"/>shaikh<break time=\"200ms\"/>ishaq1996<break time=\"200ms\"/>@gmail.com <break time=\"500ms\"/> or else you can exit by saying stop,<break time=\"400ms\"/> want to try one more time? "
        #speech_output = "All steps are finished" 
        speech_output  =LASTSTEP + LAST
        stepNum = stepNum+1
        session_attributes = {"step_Number":stepNum}
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    elif stepNum>6:
        speech_output  = "Sorry!<break time=\"500ms\"/>want to start again? reply with yes <break time=\"500ms\"/> or else stop to exit. "
        stepNum = stepNum+1
        session_attributes = {"step_Number":stepNum}
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
    else:
        say = stepDict["step"][stepNum]
        speech_output =say 
        stepNum = stepNum +1
        session_attributes = {"speech_output":speech_output,
        "reprompt_text":reprompt_text,
         "step_Number":stepNum}
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    
    if intent_name == "AMAZON.YesIntent":
        return yes_func()
    if intent_name == "AMAZON.NextIntent":
        return handle_next_request(intent,session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()
    elif intent_name == "StartGameIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help_request()
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat_request(intent,session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def handle_session_end_request():
    card_title = "Thanks"
    speech_output ="Thanks for playing! "\
    "See you next time."
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


# --------------- Main handler ---------------------------------------
def lambda_handler(event, context):
    # if (event["session"]["application"]["applicationId"] !=
    #         "amzn1.echo-sdk-ams.app.bd304b90-xxxx-xxxx-xxxx-xxxxd4772bab"):
    #     raise ValueError("Invalid Application ID")   
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
