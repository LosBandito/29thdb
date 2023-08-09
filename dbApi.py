from flask import Flask, request, jsonify, g
from flask_cors import CORS
from mdbTests import MilitaryDatabase

app = Flask(__name__)
CORS(app)


def get_db():
    if 'db' not in g:
        g.db = MilitaryDatabase('29awards.db')
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/soldiers', methods=['GET'])
def get_all_soldiers():
    db = get_db()
    soldiers = db.retrieve_all_soldiers()
    return jsonify(soldiers)


@app.route('/units/<int:parent_unit_id>', methods=['GET'])
def get_units_by_parent(parent_unit_id):
    db = get_db()
    units = db.retrieve_units_by_parent(parent_unit_id)
    return jsonify(units)


@app.route('/soldier', methods=['POST'])
def add_soldier():
    db = get_db()
    data = request.get_json()
    soldier_id = db.add_soldier(data['name'], data['age'], data['address'], data['rank'], data['ait'], data['unit_id'])
    return jsonify({'id': soldier_id}), 201


@app.route('/soldier', methods=['GET'])
def remove_soldier():
    db = get_db()
    data = request.get_json()
    db.remove_soldier(data['id'])
    return '', 204

@app.route('/soldiers/<int:unit_id>', methods=['GET'])
def get_soldiers_by_unit(unit_id):
    db = get_db()
    soldiers = db.get_soldiers_by_unit(unit_id)
    return jsonify(soldiers)


@app.route('/addunit', methods=['POST'])
def add_unit():
    db = get_db()
    data = request.get_json()
    unit_id = db.add_unit(data['name'], data['type'], data['image'], data.get('parent_unit_id'))
    return jsonify({'id': unit_id}), 201


@app.route('/assign', methods=['POST'])
def assign_soldier_to_unit():
    db = get_db()
    data = request.get_json()
    db.assign_soldier_to_unit(data['soldier_id'], data['unit_id'])
    return '', 204


@app.route('/units', methods=['GET'])
def get_all_units():
    db = get_db()
    units = db.retrieve_all_units()
    return jsonify(units)


@app.route('/addaward/<int:soldier_id>/<int:award_id>', methods=['GET'])
def add_award(soldier_id, award_id):
    db = get_db()
    db.add_award_to_soldier(soldier_id, award_id)
    return f'Award added for {soldier_id}', 204


@app.route('/removeaward/<int:soldier_id>/<int:award_id>', methods=['GET'])
def remove_award(soldier_id, award_id):
    db = get_db()
    db.remove_award_from_soldier(soldier_id, award_id)
    return f'Award removed for {soldier_id}', 204


@app.route('/getawards/<int:soldier_id>', methods=['GET'])
def get_award_by_solider(soldier_id):
    db = get_db()
    return jsonify(db.get_awards_by_soldier(soldier_id))


@app.route('/getallawards', methods=['GET'])
def get_all_awards():
    db = get_db()
    units = db.get_all_awards()
    return jsonify(units)


@app.route('/adddemerit/<int:soldier_id>', methods=['POST'])
def add_demerit(soldier_id):
    db = get_db()
    data = request.get_json()
    db.add_demerit_to_soldier(soldier_id, data['description'])
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
