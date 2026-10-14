import os 
from dotenv import load_dotenv 
from flask import Flask, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_refresh_token_required, create_access_token\
    , JWTManager, create_access_token, create_refresh_token 
load_dotenv()

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
JWT_REFRESH_TOKEN_EXPIRES=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 604800))

app=Flask(__name__)
app.config["JWT_SECRET_KEY"]=JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"]=JWT_REFRESH_TOKEN_EXPIRES

jwt=JWTManager()

@app.route("/login", methods=["POST"])
def login():
    user_name="admin"
    password="secret"

    if user_name=="admin" and password=="secret":
        access_token=create_access_token(identity=user_name)
        refresh_token=create_refresh_token(identity=user_name)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    return jsonify({"msg":"Wrong creditial"}), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Привет, {current_user}! Это защищённый ресурс."}), 200


@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required()
def refresh():
    current_user=get_jwt_identity()
    new_access_token=create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

if __name__=="__main__":
    app.run(port=5000)