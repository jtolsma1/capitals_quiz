import os
from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np

class AnswerRequest(BaseModel):
    user_id: str
    question_value: str
    answer_value: str

class UserResetRequest(BaseModel):
    user_id: str

app = FastAPI()

def get_country_dict_for_user(user_id):
    user_path = os.path.join("/data",str(user_id) + "_country_dict.json")

    if os.path.exists(user_path):
        with open(user_path, "r") as f_user:
            country_dict = json.load(f_user)
    else:
        with open("/data/country_dict_complete.json","r") as f_complete:
            country_dict = json.load(f_complete)

    return user_path,country_dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/question")
def get_question_value(user_id):
    _user_path,country_dict = get_country_dict_for_user(user_id)
    country_list = list(country_dict.keys())
    question_value = str(np.random.choice(country_list))
    return question_value

@app.post("/answer")
def check_answer_value(answer_request: AnswerRequest):

    user_id = answer_request.user_id
    user_path,country_dict = get_country_dict_for_user(user_id)

    question_value = answer_request.question_value
    answer_value = answer_request.answer_value.strip().title()

    correct_answer = country_dict[question_value]
    if answer_value == correct_answer:
        del country_dict[question_value]
        with open(user_path,"w") as f_user:
            json.dump(country_dict,f_user)
        return True
    else:
        return False

@app.post("/user_reset")
def reset_user_history(user_reset_request: UserResetRequest):
    user_id = user_reset_request.user_id.strip()
    user_path = os.path.join("/data",str(user_id)+"_country_dict.json")
    if os.path.exists(user_path):
        os.remove(user_path)
        return True
    else:
        return False
