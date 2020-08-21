from flask import Flask, jsonify
from flask_restful import Resource, Api
#from OpenSSL import SSL
import os

app = Flask(__name__)
api = Api(app)

app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return "보드게임좋아"

class game(Resource):
    def get(self):
        return jsonify({"method":"get", "room":"1", "player":"user1", "board":"010010101010100"})

api.add_resource(game, "/game")

# 로직 계산, 동기화 부분!important, 

if __name__ == "__main__":
    app.run(host="108.61.127.229", port=80)



# getMapStatus()
# setStone()
# getGameStatus()

'''
req ->


res ->
- board 정보 [[]]		
- 플레이어 1 or 2	
- 턴 수

'''
