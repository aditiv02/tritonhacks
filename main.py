import tkinter as tk
import random
import os
import google.generativeai as genai


# ✅ Configure Gemini API Key from environment variable
genai.configure(api_key="AIzaSyDNNtflyRFPOTxVtOLFCmOQU6R0tvrX-1I")
model = genai.GenerativeModel("gemini-1.5-flash")


# ✅ Gemini-powered explanation
def explain_incorrect_answer(question, wrong_answer, correct_answer):
   prompt = (
       f"A first responder quiz asked: '{question}'. "
       f"The user selected: '{wrong_answer}', but the correct answer is: '{correct_answer}'. "
       "Explain in 2-3 concise sentences why the selected answer is incorrect and why the correct answer is appropriate."
   )
   try:
       response = model.generate_content(prompt)
       return response.text.strip()
   except Exception as e:
       return f"The correct answer was: {correct_answer}. (Gemini explanation failed: {e})"


class StartPage:
   def __init__(self, root, all_questions):
       self.root = root
       self.all_questions = all_questions
       self.frame = None
       self.build_ui()


   def build_ui(self):
       self.root.title("Fast Dispatch")
       self.root.configure(bg="#f0f4f8")


       self.frame = tk.Frame(self.root, bg="#f0f4f8", padx=50, pady=50)
       self.frame.pack(expand=True, fill="both")


       label = tk.Label(
           self.frame,
           text="Welcome to Fast Dispatch Simulator",
           font=("Segoe UI", 30, "bold"),
           fg="#007acc",
           bg="#f0f4f8"
       )
       label.pack(pady=(0, 40))


       start_button = tk.Button(
           self.frame,
           text="Start Quiz",
           font=("Segoe UI", 20, "bold"),
           width=25,
           command=self.start_quiz,
           bg="#e6f0fa", fg="#004a99",
           activebackground="#a9cde9", activeforeground="#003366",
           relief="raised", bd=3, cursor="hand2"
       )
       start_button.pack(pady=15, ipady=10)


       exit_button = tk.Button(
           self.frame,
           text="Exit",
           font=("Segoe UI", 20, "bold"),
           width=25,
           command=self.root.quit,
           bg="#e6f0fa", fg="#004a99",
           activebackground="#a9cde9", activeforeground="#003366",
           relief="raised", bd=3, cursor="hand2"
       )
       exit_button.pack(pady=15, ipady=10)


   def start_quiz(self):
       self.frame.destroy()
       DifficultySelector(self.root, self.all_questions)


class DifficultySelector:
   def __init__(self, root, all_questions):
       self.root = root
       self.all_questions = all_questions
       self.frame = None
       self.build_ui()


   def build_ui(self):
       self.root.title("Select Difficulty")
       self.root.configure(bg="#f0f4f8")


       self.frame = tk.Frame(self.root, bg="#f0f4f8", padx=50, pady=50)
       self.frame.pack(expand=True, fill="both")


       label = tk.Label(
           self.frame,
           text="Choose Difficulty",
           font=("Segoe UI", 30, "bold"),
           fg="#007acc",
           bg="#f0f4f8"
       )
       label.pack(pady=(0, 40))


       for level, count in [("Easy (5 Questions)", 5), ("Medium (10 Questions)", 10), ("Difficult (20 Questions)", 20)]:
           btn = tk.Button(
               self.frame,
               text=level,
               font=("Segoe UI", 20),
               width=25,
               command=lambda c=count: self.start_quiz(c),
               bg="#e6f0fa", fg="#004a99",
               activebackground="#a9cde9", activeforeground="#003366",
               relief="raised", bd=3, cursor="hand2"
           )
           btn.pack(pady=15, ipady=10)


   def start_quiz(self, num_questions):
       self.frame.destroy()
       selected_questions = random.sample(self.all_questions, min(num_questions, len(self.all_questions)))
       DispatchSimulator(self.root, selected_questions, self.all_questions)


class DispatchSimulator:
   def __init__(self, root, questions, all_questions):
       self.root = root
       self.questions = questions
       self.all_questions = all_questions
       self.score = 0
       self.current_q = 0
       self.timer_id = None
       self.time_left = 5
       self.root.title("Fast Dispatch")
       self.root.configure(bg="#f0f4f8")




       self.frame = tk.Frame(root, bg="#f0f4f8", padx=30, pady=30)
       self.frame.pack(expand=True, fill="both")




       # Timer label at top-right corner inside a box
       self.timer_box = tk.Frame(self.root, bg="#ffcccc", padx=10, pady=5)
       self.timer_box.place(relx=0.95, rely=0.05, anchor="ne")
       self.timer_label = tk.Label(
           self.timer_box,
           text=f"Time Left: {self.time_left}s",
           font=("Segoe UI", 14),
           fg="red",
           bg="#ffcccc",
       )
       self.timer_label.pack()




       self.question_label = tk.Label(
           self.frame,
           text="",
           wraplength=650,
           font=("Segoe UI", 20, "bold"),
           fg="#007acc",
           bg="#f0f4f8",
           justify="center"
       )
       self.question_label.pack(pady=(0, 25))




       self.buttons = []
       for i in range(4):
           btn = tk.Button(
               self.frame,
               text="",
               width=55,
               font=("Segoe UI", 18),
               bg="#e6f0fa",
               fg="#004a99",
               relief="raised",
               bd=3,
               activebackground="#a9cde9",
               activeforeground="#003366",
               cursor="hand2",
               command=lambda i=i: self.check_answer(i)
           )
           btn.pack(pady=12, ipady=15)
           btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#a9cde9", fg="#003366"))
           btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#e6f0fa", fg="#004a99"))
           self.buttons.append(btn)




       self.next_button = tk.Button(
           self.frame,
           text="Next Question",
           font=("Segoe UI", 20, "bold"),
           bg="#b0c4de",
           fg="#003366",
           activebackground="#7a94bb",
           activeforeground="#e6f0fa",
           relief="raised",
           bd=3,
           cursor="hand2",
           command=self.next_question
       )
       self.next_button.pack(pady=20)
       self.next_button.config(state="disabled")




       self.feedback_label = tk.Label(
           self.frame,
           text="",
           wraplength=700,
           font=("Segoe UI", 17),
           fg="#004a99",
           bg="#f0f4f8",
           justify="center"
       )
       self.feedback_label.pack(pady=(10, 0))




       self.return_button = tk.Button(
           self.frame,
           text="Return to Start",
           font=("Segoe UI", 16, "bold"),
           bg="#cccccc",
           fg="#333333",
           relief="raised",
           bd=3,
           cursor="hand2",
           command=self.return_to_start
       )
       self.return_button.pack(pady=(20, 0))
       self.return_button.pack_forget()




       self.score_frame = tk.Frame(root, bg="#d9e6f2", pady=15)
       self.score_frame.pack(fill="x", side="bottom")




       self.score_label = tk.Label(
           self.score_frame,
           text="Score: 0",
           font=("Segoe UI", 20, "bold"),
           fg="#cc0000",
           bg="#d9e6f2"
       )
       self.score_label.pack()




       self.load_question()




   def load_question(self):
       if self.current_q >= len(self.questions):
           self.question_label.config(
               text=f"🎉 Quiz Complete! Final score: {self.score} / {len(self.questions)} 🎉"
           )
           for btn in self.buttons:
               btn.pack_forget()
           self.next_button.pack_forget()
           self.feedback_label.config(
               text="Click below to return to the difficulty selection screen.",
               fg="#004a99"
           )
           self.return_button.pack()
           return




       q = self.questions[self.current_q]
       self.question_label.config(text=f"Q{self.current_q + 1}: {q['question']}")
       for i, option in enumerate(q["options"]):
           self.buttons[i].config(text=option, state="normal")




       self.next_button.config(state="disabled")
       self.feedback_label.config(text="")
       self.return_button.pack_forget()
       self.time_left = 5
       self.update_timer()




   def update_timer(self):
       self.timer_label.config(text=f"Time Left: {self.time_left}s")
       if self.time_left == 0:
           self.time_out()
           return
       self.time_left -= 1
       self.timer_id = self.root.after(1000, self.update_timer)




   def time_out(self):
       for btn in self.buttons:
           btn.config(state="disabled")




       q = self.questions[self.current_q]
       correct = q["answer"]
       explanation = explain_incorrect_answer(q["question"], "No answer (Timed out)", correct)




       self.feedback_label.config(
           text=f"⏱️ Time's up! The correct answer is: {correct}\n\n{explanation}",
           fg="#cc6600"
       )




       self.next_button.config(state="normal", text="Next Question")
       self.score_label.config(text=f"Score: {self.score}")




   def check_answer(self, idx):
       if self.timer_id:
           self.root.after_cancel(self.timer_id)
           self.timer_id = None




       q = self.questions[self.current_q]
       selected = q["options"][idx]
       correct = q["answer"]




       for btn in self.buttons:
           btn.config(state="disabled")




       if selected == correct:
           self.score += 1
           self.feedback_label.config(text="✅ Correct! Great job!", fg="#228B22")
           self.score_label.config(text=f"Score: {self.score}")
           self.root.after(1500, self.next_question)
       else:
           explanation = explain_incorrect_answer(q["question"], selected, correct)
           self.feedback_label.config(
               text=f"❌ Incorrect! The correct answer is: {correct}\n\n{explanation}",
               fg="#cc0000"
           )
           self.score_label.config(text=f"Score: {self.score}")
           self.next_button.config(state="normal", text="Next Question")




   def next_question(self):
       if self.timer_id:
           self.root.after_cancel(self.timer_id)
           self.timer_id = None
       self.current_q += 1
       self.load_question()




   def return_to_start(self):
       self.frame.destroy()
       self.score_frame.destroy()
       StartPage(self.root, self.all_questions)








if __name__ == "__main__":
   root = tk.Tk()
   root.state("zoomed")




   all_questions = [
       {"question": "Caller reports a house fire. What’s your first step?",
        "options": ["Send fire department", "Send ambulance", "Send police", "Ask for more info"],
        "answer": "Ask for more info"},
       {"question": "Caller says someone is unconscious. What do you dispatch?",
        "options": ["Fire department", "Ambulance", "Police", "Animal control"],
        "answer": "Ambulance"},
       {"question": "Caller reports a burglary in progress. What do you send?",
        "options": ["Police", "Ambulance", "Fire department", "Neighborhood watch"],
        "answer": "Police"},
       {"question": "Caller reports a gas leak smell. What’s your response?",
        "options": ["Send police", "Send fire department", "Send ambulance", "Ignore"],
        "answer": "Send fire department"},
       {"question": "Caller says someone is having chest pain. What do you dispatch?",
        "options": ["Ambulance", "Fire department", "Police", "Animal control"],
        "answer": "Ambulance"},
       {"question": "Caller reports a road blocked by a tree. Who do you dispatch?",
        "options": ["Police", "Fire department", "Ambulance", "Public works"],
        "answer": "Fire department"},
       {"question": "Someone is stuck in an elevator. What do you send?",
        "options": ["Police", "Fire department", "Ambulance", "Tow truck"],
        "answer": "Fire department"},
       {"question": "Caller reports someone having a seizure. Who do you send?",
        "options": ["Ambulance", "Fire department", "Police", "Wait for more info"],
        "answer": "Ambulance"},
       {"question": "Caller reports suspicious package. What do you do?",
        "options": ["Send police", "Send fire department", "Send ambulance", "Ignore"],
        "answer": "Send police"},
       {"question": "Child locked in hot car. Who do you send?",
        "options": ["Ambulance", "Police", "Fire department", "Animal control"],
        "answer": "Fire department"},
       {"question": "What is the primary concern when responding to a mass casualty incident (MCI)?",
        "options": ["Treat the most severely injured first", "Ensure no more casualties occur", "Maintain traffic flow", "Establish a clear triage system"],
        "answer": "Establish a clear triage system"},
       {"question": "A person is experiencing severe anaphylaxis. What is your immediate action?",
        "options": ["Administer epinephrine", "Call for backup", "Administer oxygen", "Prepare for transport"],
        "answer": "Administer epinephrine"},
       {"question": "What should be the first step when responding to a hazardous materials spill?",
        "options": ["Identify the chemical", "Evacuate the area", "Call for special units", "Wear protective gear"],
        "answer": "Identify the chemical"},
       {"question": "You arrive at a scene with a victim suspected of a spinal injury. What should you do first?",
        "options": ["Start CPR", "Stabilize the head and neck", "Transport to the hospital", "Take vitals"],
        "answer": "Stabilize the head and neck"},
       {"question": "In a triage situation, what color tag would you assign to a patient who is not breathing but has a pulse?",
        "options": ["Black", "Green", "Red", "Yellow"],
        "answer": "Red"},
       {"question": "What is the best method for controlling severe external bleeding?",
        "options": ["Apply direct pressure", "Elevate the limbs", "Immobilize the limbs", "Give pain relief"],
        "answer": "Apply direct pressure"},
       {"question": "What should be your priority when responding to an active shooter incident?",
        "options": ["Evacuate casualties", "Neutralize the shooter", "Secure the perimeter", "Provide first aid"],
        "answer": "Neutralize the shooter"},
       {"question": "What is the main reason for establishing an Incident Command System (ICS)?",
        "options": ["To handle logistics", "To provide first aid", "To ensure clear communication and coordination", "To manage casualties"],
        "answer": "To ensure clear communication and coordination"},
       {"question": "What type of burn is characterized by blisters and intense pain?",
        "options": ["First-degree burn", "Second-degree burn", "Third-degree burn", "Chemical burn"],
        "answer": "Second-degree burn"},
       {"question": "How should you approach a patient with a suspected stroke?",
        "options": ["Give oxygen immediately", "Transport to a stroke center", "Administer aspirin", "Elevate the head and legs"],
        "answer": "Transport to a stroke center"},
       {"question": "When should a paramedic consider intubation?",
        "options": ["When the patient is not breathing", "When there is a need for medication", "When the airway is compromised", "When the patient is unconscious"],
        "answer": "When the airway is compromised"},
       {"question": "What should you do first when treating a patient with a gunshot wound to the chest?",
        "options": ["Seal the wound with an occlusive dressing", "Administer pain relief", "Transport to the hospital", "Perform CPR"],
        "answer": "Seal the wound with an occlusive dressing"},
       {"question": "What is the first step in performing CPR on an adult?",
        "options": ["Assess the victim", "Give rescue breaths", "Check the pulse", "Give chest compressions"],
        "answer": "Assess the victim"},
       {"question": "What is the proper treatment for heatstroke?",
        "options": ["Cool the patient with water and fans", "Give fluids", "Apply ice packs", "All of the above"],
        "answer": "All of the above"}
   ]




   StartPage(root, all_questions)
   root.mainloop()


