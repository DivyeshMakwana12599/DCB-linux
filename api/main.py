from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)
data = json.load(open("api/data.json"))
print(data[-1]["gameId"])

gameReqParser = reqparse.RequestParser()
gameReqParser.add_argument(
    "playerOne", type=str, help="Send Player 1 Name", required=False
)
gameReqParser.add_argument(
    "playerTwo", type=str, help="Send Player 2 Name", required=False
)
gameReqParser.add_argument(
    "currentPosition", type=str, help="Send current position fen", required=True
)


class WelcomePage(Resource):
    def get(self):
        return "Digital Chess Board"


class Games(Resource):
    def get(self):
        return data

    def post(self):
        args = gameReqParser.parse_args()
        args["gameId"] = int(data[-1]["gameId"]) + 1
        data.append(args)
        json.dump(data, open(r"api/data.json", "w"), indent=2)
        return args, 200


class GamesId(Resource):
    def get(self, gameId):
        for game in data:
            if game["gameId"] == gameId:
                return game
        return "gameId not valid...", 400

    def put(self, gameId):
        args = gameReqParser.parse_args()
        args["gameId"] = gameId
        for i, game in enumerate(data):
            if game["gameId"] == gameId:
                args["playerOne"] = game["playerOne"]
                args["playerTwo"] = game["playerTwo"]
                data[i] = args
                json.dump(data, open(r"api/data.json", "w"), indent=2)
                return args, 200
        return "game ID dose not exits", 400


api.add_resource(Games, "/api/games")
api.add_resource(WelcomePage, "/")
api.add_resource(GamesId, "/api/games/<string:gameId>")

if __name__ == "__main__":
    app.run(debug=True)
