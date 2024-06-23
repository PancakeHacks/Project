import cohere

co = cohere.Client("XjvcpqfPE4rb4v66IQObofnt5Y4tQa19QajYBgV4")

def get_response(prompt):
    response = co.chat(message=prompt)
    return response

def feedback(score):
    if score > 60:
        response = get_response("The person's workout did not go well, they went too low on each workout so it could cause them pain or give them an injury, give them feedback to correct that. LIMIT RESPONSE TO 25 WORDS")
    elif score > 40:
        response = get_response("The person's workout was not very good, but not terrible, they went a little too low on each rep of the workout, give them feedback to correct it. LIMIT RESPONSE TO 25 WORDS")
    elif score > 20:
        response = get_response("This person did almost perfect with their workout, they only went slightly too low, give them some feedback on how to do better! LIMIT RESPONSE TO 25 WORDS")
    else:
        response = get_response("This person did a perfect workout, give them some feedback on how well they did! LIMIT RESPONSE TO 25 WORDS")
    return response.text

if __name__ == "__main__":
    print(feedback(25))