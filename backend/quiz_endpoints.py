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
    """
    Downloads the dictionary of countries and capitals for use in the quiz. 
    Repeated in the question and answer step.
    @param user_id: user_id for the current quiz session
    @return user_path: path designated to save user quiz data
    @return country_dict: user-specific dictionary used for the quiz
    """
    user_path = os.path.join("/data",str(user_id) + "_country_dict.json")

    if os.path.exists(user_path):
        with open(user_path, "r") as f_user:
            country_dict = json.load(f_user)
    else:
        with open("/data/country-by-capital-city.json","r") as f_complete:
            country_dict = json.load(f_complete)

    return user_path,country_dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/question")
def get_question_value(user_id):
    """
    Downloads the dictionary of countries and capitals for use in the quiz. 
    Selects a random country to quiz the user.
    @param user_id: user_id for the current quiz session
    @return question_value: the country served as the next quiz question
    """
    _user_path,country_dict = get_country_dict_for_user(user_id)
    country_list = list(country_dict.keys())
    question_value = str(np.random.choice(country_list))
    return question_value

@app.post("/answer")
def check_answer_value(answer_request: AnswerRequest):
    """
    Downloads the dictionary of countries and capitals for use in the quiz. 
    Checks the user's quiz answer against the answer key.
    If a country has multiple capitals, any correct answer counts.
    If correct, deletes the question from the user's data so it isn't asked again.
    
    @param answer_request: request body containing user id, question, and answer
    @return True if answer is correct and False if answer is incorrect
    """

    user_id = answer_request.user_id
    user_path,country_dict = get_country_dict_for_user(user_id)

    question_value = answer_request.question_value
    answer_value = answer_request.answer_value.strip().title()

    correct_answers = country_dict[question_value]
    if answer_value in correct_answers:
        del country_dict[question_value]
        with open(user_path,"w") as f_user:
            json.dump(country_dict,f_user)
        return True
    else:
        return False

@app.post("/user_reset")
def reset_user_history(user_reset_request: UserResetRequest):
    """
    Resets the user's quiz data so that all countries are eligible to be asked.
    @param user_reset_request: request body containing the user id
    @return True if the user had quiz data that was deleted; False if the user had no data
    """
    user_id = user_reset_request.user_id.strip()
    user_path = os.path.join("/data",str(user_id)+"_country_dict.json")
    if os.path.exists(user_path):
        os.remove(user_path)
        return True
    else:
        return False
