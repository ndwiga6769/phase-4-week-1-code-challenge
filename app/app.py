#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db, Hero,Power,HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)
api =Api(app)
class Home(Resource):
    def get(self):
        response_dict = {
            "message":"Welcome to our API"
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response
    
api.add_resource(Home,"/")

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        hero_list = [{
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        } for hero in heroes]
        response = make_response(
            jsonify(hero_list),
            200,
        )
        return response
api.add_resource(Heroes,'/heroes')
class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_list = [{
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers':[]
        }]
            response =make_response(jsonify(hero_list),200)
            return response
        else:
            response_dict = {
            "error":"Hero not found"
            }
            response = make_response(
                jsonify(response_dict),
                200,
            )
            return response
api.add_resource(HeroesById,'/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        power_list = [{
            'id': power.id,
            'name': power.name,
            'description': power.description
        } for power in powers]
        response = make_response(
            jsonify(power_list),
            200,
        )
        return response
api.add_resource(Powers,'/powers')
class PowerById(Resource):
    def get(self,id):
        power = Power.query.filter_by(id=id).first()
        if power:
            power_dict = {
                "id":power.id,
                "name":power.name,
                "description":power.description,
            }
            response = make_response(jsonify(power_dict),200)
            return response
        else:
            response = make_response(jsonify({"error":"Power not found"}))
            return response
        
    def patch(self,id):
        power = Power.query.filter_by(id=id).first()
        if power:
            data= request.get_json()
            power.description = data['description']
            
            errors = power.validate()
            if errors:
                return jsonify({'errors': errors}), 400
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'errors': [str(e)]}), 400
            else:
                power_dict = {
                    "id":power.id,
                    "name":power.name,
                    "description":power.name
                }
                response = make_response(
                    jsonify(power_dict),
                    200
                )
                return response
            finally:
                response = make_response(jsonify({"success":f'{power.id} is successfully updated'}))
        else:
            response = make_response(jsonify({"Error" : "Power not found"},404))
            return response
api.add_resource(PowerById,'/powers/<int:id>')      

if __name__ == '__main__':
    app.run(port=5000,debug=True)
