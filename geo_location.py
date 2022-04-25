from flask import Flask, request, jsonify,Response
import requests
import xml.etree.ElementTree as ET
app = Flask(__name__)

API_KEY = "AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw"

@app.route('/getAddressDetails',methods=["POST"])
def getAddressDetails():
    input_json = request.get_json(force=True)
    user_input = {'address':input_json['address'],'output_format':input_json['output_format']}
    params = {
        "key":API_KEY,
        "address": user_input['address']
    }
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    response = requests.get(base_url,params= params).json()

    try:
        response = response["results"][0]
        if user_input["output_format"].lower() == "json":
            output = {}
            output["coordinates"] = {}
            output["coordinates"]["lat"] = response["geometry"]["location"]["lat"]
            output["coordinates"]["lng"] = response["geometry"]["location"]["lng"]
            output["address"] = f'# {response["formatted_address"]}'
            return output
        elif user_input["output_format"].lower() == "xml":
            root = ET.Element(f"root")
            ET.SubElement(root,"address").text = f'\n # {str(response["formatted_address"])} \n'
            address = ET.SubElement(root,"coordinates")
            ET.SubElement(address,"lat").text = f'\n {str(response["geometry"]["location"]["lat"])} \n'
            ET.SubElement(address,"lng").text = f'\n {str(response["geometry"]["location"]["lng"])} \n'
            return ET.tostring(root, encoding='utf8', method='xml')
        else:
            return "Enter a valid return format for the response."

    except IndexError:
        output = {}
        output["address"] = f'# {user_input["address"]}'
        output["result"] = 'No results for the search.'
        return output

app.run(debug=True)