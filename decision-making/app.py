from flask_restplus import Api, Resource
from flask import Flask

from webargs.flaskparser import use_args
from webargs import fields


app = Flask(__name__)
api = Api(app)


@api.route("/api/decision")
class DecisionMaker(Resource):
	@use_args({
		"temperature": fields.Float(required=True),
		"humidity": fields.Float(required=True),
		"summer": fields.Bool(required=True)
	})
	def post(self, args):
		temp = float(args["temperature"])
		hum = float(args["humidity"])
		summer = bool(args["summer"])
		cmd = {}
		temp_max = 0
		temp_min = 0
		hum_max = 0
		hum_min = 47
		critical_max_hum = 65
		critical_min_hum = 40
		room_dimension = 200 # mq
		cmd = {
			"heating": 0,
			"ventilaton": 0,
			"humidifier": 0,
			"dehumidifier": 0,
			"distance": 0,
			"people_cap": 0 
		}

		if summer:
			temp_max = 26
			temp_min = 24
			hum_max = 55
		else:
			temp_max = 23
			temp_min = 21
			hum_max = 50

		if temp < temp_min:
			cmd["heating"] = True
		elif temp > temp_max:
			cmd["ventilaton"] = True
		else:
			cmd["heating"] = False
			cmd["ventilation"] = False

		if hum < hum_min:
			cmd["humidifier"] = True
		elif hum > hum_max:
			cmd["dehumidifier"] = True
			# cmd["clock"] = True
		else:
			cmd["dehumidifier"] = False
			cmd["humidifier"] = False
		
		if hum < critical_min_hum or hum > critical_max_hum:
			cmd["distance"] = 2
		else:
			cmd["distance"] = 1.5

		cmd["people_cap"] = abs(room_dimension//(cmd["distance"] + 0.2))

		return cmd, 200


if __name__ == '__main__':
	flask.run()
