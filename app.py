from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
print(os.getenv("MONGO_URI"))
mongo = PyMongo(app)

@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200

@app.route('/')
def index():
    items = mongo.db.items.find()
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    if name:
        mongo.db.items.insert_one({"name": name})
    return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            mongo.db.items.update_one({'_id': ObjectId(id)}, {'$set': {"name": name}})
        return redirect(url_for('index'))
    item = mongo.db.items.find_one({'_id': ObjectId(id)})
    return render_template('edit.html', item=item)


@app.route('/delete/<id>')
def delete_item(id):
    mongo.db.items.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
