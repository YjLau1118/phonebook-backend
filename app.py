from flask import Flask, render_template, url_for, request, redirect, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient('localhost', 27017)
db = client.phonebookdb
phonebook = db.phonebook

# Add Contact
@app.route("/api/addContact", methods=['POST'])
def add_contact():
    if request.method == 'POST':
        data = request.json
        if 'name' in data and 'phone' in data:
            new_contact = {
                'name': data['name'],
                'phone': data['phone']
            }
            result = phonebook.insert_one(new_contact)
            return jsonify({"status": "Success", "message": {"id": str(result.inserted_id)}}), 201
        else:
            return jsonify({"status": "Error", "message": "Name and phone number are required"}), 400
        
# Get Contact List
@app.route("/api/contactList", methods=['GET'])
def get_contact_list():
    contacts = list(phonebook.find({}, {'_id': 1, 'name': 1, 'phone': 1}))
    formatted_contacts = []
    for contact in contacts:
        contact['_id'] = str(contact['_id'])
        formatted_contacts.append(contact)
    return jsonify({"status": "Success", "message": formatted_contacts}), 200

# Get Contact Detail by ID
@app.route("/api/contactDetail/<string:id>", methods=['GET'])
def get_contact_detail(id):
    if request.method == 'GET':
        contact = phonebook.find_one({'_id': ObjectId(id)}, {'_id': 1, 'name': 1, 'phone': 1})
        if contact:
            contact['_id'] = str(contact['_id'])
            return jsonify({"status": "Success", "message": contact}), 200
        else:
            return jsonify({"status": "Error", "message": "Contact not found"}), 404

# Edit Contact Detail
@app.route("/api/editContact/<string:id>", methods=['PUT'])
def edit_contact(id):
    if request.method == 'PUT':
        data = request.json
        if 'name' in data and 'phone' in data:
            updated_contact = {
                'name': data['name'],
                'phone': data['phone']
            }
            phonebook.update_one({'_id': ObjectId(id)}, {'$set': updated_contact})
            return jsonify({"status": "Success", "message": "Contact updated successfully"}), 200
        else:
            return jsonify({"status": "Error", "message": "Name and phone number are required"}), 400

# Delete Contact Detail
@app.route("/api/deleteContact/<string:id>", methods=['DELETE'])
def delete_contact(id):
    if request.method == 'DELETE':
        existing_contact = phonebook.find_one({'_id': ObjectId(id)})
        if existing_contact:
            phonebook.delete_one({'_id': ObjectId(id)})
            return jsonify({"status": "Success", "message": "Contact deleted successfully"}), 200
        else:
            return jsonify({"status": "Error", "message": "Contact not found"}), 404
        
if __name__ == "__main__":
    app.run(debug=True)
