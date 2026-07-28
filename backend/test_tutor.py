import sys, os, traceback
sys.path.append(os.path.dirname(os.getcwd()))
from dotenv import load_dotenv
load_dotenv()
from backend.agents.tutor import TutorAgent

try:
    t = TutorAgent()
    print("Agent init successful")
    result = t.respond([{'role': 'user', 'content': 'who are you'}], 'who are you')
    print("Result:", result)
except Exception as e:
    traceback.print_exc()
