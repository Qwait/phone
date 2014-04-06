import re

from pyramid.response import Response
from pyramid.view import view_config

from twilio import twiml

from phone.twilio.dbutils import get_mailbox_url

WELCOME_MESSAGE = """Welcome to the voice mail system. Please enter
the four digit extension of the person you're trying to reach followed
by the pound symbol, or, hit star for the menu.
"""

CREATE_A_MAILBOX = """Please select a four digit mailbox number between
1000 and 9999"""

MAILBOX_CREATED = """Your mailbox has been created, please select a four
digit passcode"""

NOT_A_VALID_MAILBOX = """I'm sorry, that is not a valid mailbox"""

ERROR_MESSAGE = """A system error has occurred"""

VOICE_PREFERENCE = 'woman'

is_a_mailbox = re.compile('[1-9]\d{3,}')

@view_config(route_name='twilio_index')
def index(request):
    response = twiml.Response()
    response.gather(method='GET',
        action=request.route_url('twilio_process_input',
        star='twilio_create_mailbox_ask',
        numeric='twilio_mailbox')) \
        .say(WELCOME_MESSAGE, voice=VOICE_PREFERENCE, loop=2)
    return Response(str(response))

"""
  This reads the digits and passes them onto other handlers.
"""
@view_config(route_name='twilio_process_input')
def process_input(request):
    print request.matched_route.name
    print request.params
    digits = request.params['Digits']
    star = request.matchdict['star']
    numeric = request.matchdict['numeric']
    response = twiml.Response()
    if digits == '*':
        response.redirect(request.route_url(star), method='GET')
    elif is_a_mailbox.match(digits):
        url = get_mailbox_url(digits)
        if url:
            response.redirect(request.route_url(numeric), method='GET')
        else:
            response.say(NOT_A_VALID_MAILBOX, voice=VOICE_PREFERENCE) \
                .redirect(request.route_url('twilio_index'), method='GET')
    else:
        response.say(ERROR_MESSAGE, voice=VOICE_PREFERENCE)
    return Response(str(response))

"""
mailbox number
greeting_url
"""

@view_config(route_name='twilio_mailbox')
def mailbox(request):
    print request.matched_route.name
    print request.params
    # if mailbox url, if not, play setup instructions
    response = twiml.Response()
    response.enqueue("Queue Demo")
    return Response(str(response))

@view_config(route_name='twilio_mailbox_admin')
def mailbox_admin(request):
    print request.matched_route.name
    print request.params
    response = twiml.Response()
    response.enqueue("Queue Demo")
    return Response(str(response))

@view_config(route_name='twilio_mailbox_admin_listen')
def listen(request):
    print request.matched_route.name
    print request.params
    response = twiml.Response()
    response.enqueue("Queue Demo")
    return Response(str(response))

@view_config(route_name='twilio_mailbox_create_ask')
def mailbox_create_ask(request):
    """
    1) ask for 4 digits
    2) see if they already exist
    3) if yes, try again
    4) if no, ask to select and verify password
    5) record greeting
    """
    print request.matched_route.name
    print request.params
    response = twiml.Response()
    response.gather(method='GET',
        action=request.route_url('twilio_process_input',
        star=None,
        numeric='twilio_mailbox_check')) \
        .say(CREATE_A_MAILBOX, voice=VOICE_PREFERENCE)
    return Response(str(response))

@view_config(route_name='twilio_mailbox_check')
def mailbox_check(request):
    url = get_mailbox_url(digits)
    if url is None:
        response = twiml.Response()
        response.gather(method='GET',
            action=request.route_url('twilio_process_input',
            star=None,
            numeric='twilio_mailbox_password')) \
            .say(MAILBOX_CREATED, voice=VOICE_PREFERENCE)
    return Response(str(response))

@view_config(route_name='twilio_mailbox_password')
def mailbox_password(request):
    url = get_mailbox_url(digits)
    if url is None:
        response = twiml.Response()
        response.gather(method='GET',
            action=request.route_url('twilio_process_input',
            star=None,
            numeric='twilio_mailbox_password_verify')) \
            .say(MAILBOX_CREATED, voice=VOICE_PREFERENCE)
    return Response(str(response))

@view_config(route_name='twilio_mailbox_password_verify')
def mailbox_password_verify(request):
    url = get_mailbox_url(digits)
    if url is None:
        response = twiml.Response()
        response.gather(method='GET',
            action=request.route_url('twilio_process_input',
            star=None,
            numeric='twilio_mailbox_record_greeting')) \
            .say(MAILBOX_CREATED, voice=VOICE_PREFERENCE)
    return Response(str(response))

@view_config(route_name='twilio_mailbox_record_greeting')
def mailbox_record_greeting(request):
    print request.matched_route.name
    print request.params
    #url = get_mailbox_url(digits)
    response = twiml.Response()
    response.enqueue("Queue Demo")
    return Response(str(response))

