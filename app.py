import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from googleplaces import GooglePlaces, types, lang

# Flask app should start in global layout
app = Flask(__name__)

YOUR_API_KEY = 'AIzaSyDFYyH5YoKVlY0BmbFUl5YLU3NGy6POKl8'
google_places = GooglePlaces(YOUR_API_KEY)


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
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    bank = parameters.get("bank")
    address = parameters.get("address")
    
    query_result = google_places.nearby_search(location=address, keyword=bank,radius=2000, types=[types.TYPE_BANK])
    url_list=[]
    lat_long_list=[]
    for place in query_result.places:       
        url_list.append(place.url)
        lat_long_list.append(place.geo_location)
#    zone = parameters.get("shipping-zone")

#    cost = {'Europe':900, 'North America':1200, 'South America':1300, 'Asia':1400, 'Africa':1500}

    speech = "please click the urls " + bank + address

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
