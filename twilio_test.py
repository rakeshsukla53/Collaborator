__author__ = 'rakesh'

from twilio.rest import TwilioRestClient


ACCOUNT_SID = "AC976f8a49a80efa6b3080e7316a43376e"
AUTH_TOKEN = "130891e26dd1555afa339289188dbc1d"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(to="+13024385450",  #9292389138
    from_="+13024070522", body="My profile perfectly matches with you. Let's connect")



