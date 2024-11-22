import openai
import re
import httpx

openai.api_key = "KEY"

class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        return completion.choices[0].message.content

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:
CoolerConditionDetectionML:
Runs a CoolerConditionDetectionML.pkl for the recent input and returns the prediction. 
Compare the prediction to the criterial below and generate the report to the user about the cooler condition

3: close to total failure
20: reduced effifiency
100: full efficiency

HydraulicAccumulatorDetectionML:
Runs a HydraulicAccumulatorDetectionML.pkl for the recent input and returns the prediction 
Compare the prediction to the criterial below and generate the report to the user about the Hydraulic accumulator 

130: optimal pressure
115: slightly reduced pressure
100: severely reduced pressure
90: close to total failure

InternalPumpLeakageML:
Runs a InternalPumpLeakageML.pkl for the recent input and returns the prediction
Compare the prediction to the criterial below and generate the report to the user about the Internal pump leakage

0: no leakage
1: weak leakage
2: severe leakage

ValveConditionDetectionML:
Runs a ValveConditionDetectionML.pkl for the recent input and returns the prediction 
Compare the prediction to the criterial below and generate the report to the user about the Valve condition

100: optimal switching behavior
90: small lag
80: severe lag
73: close to total failure

""".strip()