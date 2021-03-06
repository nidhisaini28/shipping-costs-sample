import urllib2
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from googleplaces import GooglePlaces, types, lang

# Flask app should start in global layout
app = Flask(__name__)

#YOUR_API_KEY = 'AIzaSyBYYWozzInvfWpbyHZTlGEoJjpkpgn8BSk'

#google_places = GooglePlaces(YOUR_API_KEY)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    YOUR_API_KEY = 'AIzaSyAxA1j8Wea5db9mC00E4vCcZWSrVuwolGQ'
    google_places = GooglePlaces(YOUR_API_KEY)
    
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("bank-name")
    address = parameters.get("address")
    #try:
        #query_result = google_places.text_search("Restaurant in New York", lat_lng ={'lat':40.730610, 'lng':-73.935242}, location='New York, USA', radius=2000, types=[types.TYPE_FOOD])
        #for place in query_result.places:
         #   para=place.url
    query_result = google_places.nearby_search(location=address, lat_lng ={'lat':51.509865, 'lng':-0.118092}, keyword=zone,radius=20000, types=[types.TYPE_BANK])
    for place in query_result.places:
        para=place.url
    #except:
     #   para = 'empty'
        
    speech = "The cost of shipping to " + zone + " is " + address + para
    

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": "shipping",
        #"data": {},
        # "contextOut": [],
        #"source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
