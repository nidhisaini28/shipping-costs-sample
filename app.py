#!/usr/bin/env python

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
    if req.get("result").get("action") != "geo-map":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    bank_name = parameters.get("bank")
    location_name = parameters.get("location")
# You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
    location=location_name, keyword=bank_name,
    radius=2000, types=[types.TYPE_BANK])
# If types param contains only 1 item the request to Google Places API
# will be send as type param to fullfil:
# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

    if query_result.has_attributions:
	print query_result.html_attributions

	
    url_list=[]
    lat_long_list=[]
    for place in query_result.places:
        url_list.append(place.url)
	lat_long_list.append(place.geo_location)
    speech = "please click the urls " + url_list [1]
#		print place.name
#		print place.geo_location
#		print place.place_id
#
#		# The following method has to make a further API call.
#		place.get_details()
#		# Referencing any of the attributes below, prior to making a call to
#		# get_details() will raise a googleplaces.GooglePlacesAttributeError.
#		print place.details # A dict matching the JSON response from Google.
#		print place.local_phone_number
#		print place.international_phone_number
#		print place.website
#		print place.url

    # Getting place photos

#    for photo in place.photos:
#        # 'maxheight' or 'maxwidth' is required
#        photo.get(maxheight=500, maxwidth=500)
#        # MIME-type, e.g. 'image/jpeg'
#        photo.mimetype
#        # Image URL
#        photo.url
#        # Original filename (optional)
#        photo.filename
#        # Raw image data
#        photo.data


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
