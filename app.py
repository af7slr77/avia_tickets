from aviasales_requests import get_ticket, get_iata_code
from flask import Flask, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import timedelta, datetime
from flask import make_response
from flask_bcrypt import Bcrypt
from config import jwt_secret_key
from migrations.alembic_config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from models import User, bcrypt, Base
import secrets

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + (DB_USER or "") + ":" + (DB_PASSWORD or "") + "@" + (DB_HOST or "") + "/" + (DB_NAME or "")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)

Base.init_app(app)
bcrypt.init_app(app)

@app.route('/registration', methods=['POST'])
def registration():
	data = request.form
	username = data.get('username')
	password = data.get('password')
	stmt = Base.select(User).filter_by(username=username)
	user = Base.session.execute(stmt).first()
	if user is not None:
		return {'message': 'User already exists'}, 409
	new_user_salt = secrets.token_hex(8)
	new_user_password = bcrypt.generate_password_hash(password + new_user_salt).decode('utf-8')
	new_user = User(
		username=username,
		password=new_user_password,
		salt=new_user_salt
	)
	Base.session.add(new_user)
	Base.session.commit()
	return {'message': 'You are registered!'}, 200

@app.route('/login', methods=['POST'])
def login():
	form_data = request.form
	username = form_data.get('username')
	password = form_data.get('password')
	stmt = Base.select(User).filter_by(username=username)
	user = Base.session.execute(stmt).first()
	if user is not None and username == user[0].username:
		is_valid_password = bcrypt.check_password_hash(user[0].password, password + user[0].salt)
		if is_valid_password:
			access_token = create_access_token(identity=user[0].id)
			return access_token
		return {'message': 'Invalid password'}, 401
	else:
		return {'message': 'Invalid credentials'}, 401

@app.route("/ticket_search", methods=['POST'])
@jwt_required()
def ticket_search():
	data = request.form
	params = {
		"city_of_departure": get_iata_code(data.get('city_of_departure')), 
		"destination_city": get_iata_code(data.get('destination_city')), 
		"departure_at": datetime.strptime(
			data.get('departure_at'), 
			"%d.%m.%Y").strftime("%Y-%m-%d"
			), 
		"return_at": datetime.strptime(
			data.get('return_at'), 
			"%d.%m.%Y"
			).strftime("%Y-%m-%d"),
		"transfer": data.get('transfer'), 
		"get_calendar": data.get('get_calendar')
	}
	return get_ticket(params)

if __name__ == '__main__':
	app.run(debug=True)