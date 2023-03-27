# chatbot_diagnostics.py
import json
import numpy as np
import pandas as pd
import re
import os
import openai
import tiktoken
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
enc = tiktoken.get_encoding("cl100k_base")

# load questions as json data
def json_loader(folder, filename):
    with open(folder+filename) as fh:
        file = json.load(fh)
    return file

questionnaire_loader = lambda name: json_loader("questionnaires/", name)
index = questionnaire_loader("index.json")

### dict to become csv
results_dict = {}
results_dict['question'] = []
results_dict['text_response'] = []
results_dict['model_eval'] = []

messages = [{"role": "system", "content": "You're a kind therapist who acknowledges the previous statement in under 15 words, in a generic and supportive way"}]
# messages1 = [{"role": "system", "content": "You are politely introducing a survey about mental health in under 10 words."}]
messages2 = [{"role": "system", "content": "You're an nlp model that analyzes a string of text and evaluates it to an integer value of possible values in a provided scale. You only provide the integer response and nothing else."}]

def ask(question, scale):

    # ### introducting each question
    # messages1.append({"role": "user", "content": ""})
    # question_intro = openai.ChatCompletion.create(
    #     model = "gpt-3.5-turbo",
    #     messages = messages1)
    # print(f"\n{question_intro.choices[0].message.content}\n{question}\n")
    print (f"{question}\n")

    output = None
    while output is None:

        content = input("Answer: ")

        ### chatgpt's response to the user's input
        messages.append({"role": "user", "content": content})
        chat_test = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages)
        print(f"\n{chat_test.choices[0].message.content}")

        eval_text = f"""
        Given the question '{question}' and this response to the question '{content}', rate the response on the following scale: {scale}. 
        Return only the corresponding integer evaluation and nothing else.
        """

        ### chatgpt's int eval of the user's input
        messages2.append({"role": "user", "content": eval_text})
        eval_test = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            # model = "text-davinci-002",
            # model = "text-davinci-003",
            messages = messages2)
        
        integer_pattern = r'\d+'
        
        model_eval_text = eval_test.choices[0].message.content
        try:
            model_eval_int = int(re.search(integer_pattern, model_eval_text).group(0))
        except:
            AttributeError
            UnboundLocalError
            print ("Please provide a more relevant response to the question.")

        # print(model_eval_text)
        # print(model_eval_int)
        break
    
    # print("\n".join([f"{score} - {word}" for word, score in scale.items()]))

    results_dict['question'].append(question)
    results_dict['text_response'].append(content) # this will be text instead of an int
    results_dict['model_eval'].append(model_eval_int) # here will be the classifier's int result of the user's text input

    pd.DataFrame(results_dict).to_csv("survey_results.csv") # prints csv to working directory

    return model_eval_int

def evaluate_section(section, type="list"):
    prefix, questions, scale = section["prefix"], section["questions"], section["scale"]
    results = [ask(" ".join([prefix, q]), scale) for q in questions]
    match type:
        case "list": return results
        case "sum": return np.sum(results)

# ph9 questionnaire
def PHQ9(filename="phq-9.json"):
    questionnaire = questionnaire_loader(filename)
    sections = questionnaire["sections"]
    scoring_functions = questionnaire["scoring"]
    
    #  SECTION 1 - Get responses to section 1 questions
    s1 = sections[0]
    s1_labels = {v: k for k, v in s1["scale"].items()}
    s1_responses = evaluate_section(s1)
    s1_total = np.sum(s1_responses)
    s1_scoring = scoring_functions[0]

    #  SECTION 2 - If any responses positive in section 1, complete section 2
    s2 = sections[1]
    s2_labels = {v: k for k, v in s2["scale"].items()}
    s2_response  = evaluate_section(s2, "sum") if any(s1_responses) else 0

    #  SEVERITY AND ACTION - Use scale to get severity of symptoms and recommended action
    severity, action = "", ""
    scoring_ranges = [range(a, b) for a, b in s1_scoring["ranges"]]
    severity_scale = [severity for severity in s1_scoring["severity"]]
    action_scale = [action for action in s1_scoring["action"]]
    for i, score_range in enumerate(scoring_ranges):
        if s1_total in score_range:
            severity = severity_scale[i]
            action = action_scale[i]
            break

    #  MDD CHECK - Check for Major Depressive Disorder, or other depressive syndromes
    mdd, other = False, False
    if s1_responses[0] >= 2 or s1_responses[1] >= 2:
        n_more_than_half = len([i for i in s1_responses if i >= 2])
        if n_more_than_half >= 5: mdd = True
        elif n_more_than_half >= 2: other = True

    #  PRINT RESULTS - Format results to be readable
    print(f"\nDepression Severity: {severity}")
    print(f"Recommended action: {action}")
    print(f"Functional health: {s2_labels[s2_response]}") 
    if mdd: print(f"! Major Depressive Disorder suggested")
    if other: print(f"! Major depressive disorder not suggested, but other depressive syndrome suggested")

# gad7 questionnaire
def GAD7(filename="gad-7.json"):
    questionnaire = questionnaire_loader(filename)
    sections = questionnaire["sections"]
    scoring_functions = questionnaire["scoring"]
    
    #  SECTION 1 - Get responses to section 1 questions
    s1 = sections[0]
    s1_labels = {v: k for k, v in s1["scale"].items()}
    s1_responses = evaluate_section(s1)
    s1_total = np.sum(s1_responses)
    s1_scoring = scoring_functions[0]

    #  SECTION 2 - If any responses positive in section 1, complete section 2
    s2 = sections[1]
    s2_labels = {v: k for k, v in s2["scale"].items()}
    s2_response  = evaluate_section(s2, "sum") if any(s1_responses) else 0

    #  SEVERITY - Use scale to get severity of symptoms
    severity = ""
    scoring_ranges = [range(a, b) for a, b in s1_scoring["ranges"]]
    severity_scale = [severity for severity in s1_scoring["severity"]]
    for i, score_range in enumerate(scoring_ranges):
        if s1_total in score_range:
            severity = severity_scale[i]
            break

    #  PRINT RESULTS - Format results to be readable
    print(f"\nAnxiety Severity: {severity}")
    print(f"Functional health: {s2_labels[s2_response]}")

# ASRS5 questionnaire
def ASRS5(filename="asrs-5.json"):
    questionnaire = questionnaire_loader(filename)
    sections = questionnaire["sections"]
    scoring_functions = questionnaire["scoring"]
    
    #  SECTION 1 - Get responses to section 1 questions
    s1 = sections[0]
    s1_labels = {v: k for k, v in s1["scale"].items()}
    s1_responses = evaluate_section(s1)
    s1_total = np.sum(s1_responses)
    s1_scoring = scoring_functions[0]

    #  SEVERITY - Use scale to check if user screens positive
    result = None
    scoring_ranges = [range(a, b) for a, b in s1_scoring["ranges"]]
    severity_scale = [outcome for outcome in s1_scoring["severity"]]
    for i, score_range in enumerate(scoring_ranges):
        if s1_total in score_range:
            result = severity_scale[i]
            break

    #  PRINT RESULTS - Format results to be readable
    print(f"\nADHD Screening: {result}")

# ZFOCS questionnaire
def ZFOCS(filename="zf-ocs.json"):
    questionnaire = questionnaire_loader(filename)
    sections = questionnaire["sections"]
    
    #  SECTION 1 - Get responses to section 1 questions
    s1 = sections[0]
    s1_responses = evaluate_section(s1)

    #  SECTION 2 - If any responses positive in section 1, complete section 2
    s2 = sections[1]
    s2_response  = evaluate_section(s2, "sum") if any(s1_responses) else 0

    #  SEVERITY - Use scale to check if user screens positive
    result = True if any(s1_responses) and s2_response else False

    #  PRINT RESULTS - Format results to be readable
    print(f"\nPotential OCD: {result}")

# PCPTSD questionnaire
def PCPTSD(filename="pc-ptsd.json", cut_point=4):
    questionnaire = questionnaire_loader(filename)
    sections = questionnaire["sections"]
    
    #  SECTION 1 - Get responses to section 1 questions
    s1 = sections[0]
    s1_response = evaluate_section(s1, "sum")

    #  SECTION 2 - If any responses positive in section 1, complete section 2
    s2 = sections[1]
    s2_response = evaluate_section(s2, "sum") if s1_response else 0

    #  SEVERITY - Use scale to check if user screens positive
    result = True if s2_response >= cut_point else False

    #  PRINT RESULTS - Format results to be readable
    print(f"\nPotential PTSD: {result}")