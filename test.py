import tkinter as tk
import random
import google.generativeai as genai

# ==== SETUP GEMINI ====
# Paste your Gemini API key here or use your environment variable setup
genai.configure(api_key="AIzaSyDNNtflyRFPOTxVtOLFCmOQU6R0tvrX-1I")
model = genai.GenerativeModel("gemini-1.5-flash")

# ==== AI EXPLANATION FUNCTION ====
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

class GeminiChatbot:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Responder AI Chatbot")
        self.window.geometry("500x600")
        self.window.configure(bg="#f0f4f8")

        self.chat_area = tk.Text(self.window, wrap="word", font=("Segoe UI", 13), state="disabled", bg="#ffffff", fg="#222")
        self.chat_area.pack(padx=10, pady=10, expand=True, fill="both")

        self.entry = tk.Entry(self.window, font=("Segoe UI", 13))
        self.entry.pack(padx=10, pady=(0, 10), fill="x")

        send_btn = tk.Button(self.window, text="Send", font=("Segoe UI", 13), command=self.send_message)
        send_btn.pack(pady=(0, 10))

        # Set focus on entry field when the window opens
        self.entry.focus_set()

        # Bind <Return> to Entry, but also to window for robustness
        self.entry.bind("<Return>", self.send_message)
        self.window.bind("<Return>", self.send_message)

        self.post_message("ResponderBot", "Hi! I'm the Responder AI. How can I help you today?")

    def post_message(self, sender, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", f"{sender}: {message}\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see("end")

    def send_message(self, event=None):
        # Always set focus back to the entry after sending
        self.entry.focus_set()
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        self.post_message("You", user_msg)
        self.entry.delete(0, "end")
        self.root.after(100, lambda: self.get_bot_reply(user_msg))

    def get_bot_reply(self, prompt):
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip()
        except Exception as e:
            reply = f"Sorry, I couldn't process that: {e}"
        self.post_message("ResponderBot", reply)


# ==== MAIN PAGES ====
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

        chatbot_button = tk.Button(
            self.frame,
            text="Open AI Chatbot",
            font=("Segoe UI", 20, "bold"),
            width=25,
            command=self.open_chatbot,
            bg="#e6f0fa", fg="#004a99",
            activebackground="#a9cde9", activeforeground="#003366",
            relief="raised", bd=3, cursor="hand2"
        )
        chatbot_button.pack(pady=15, ipady=10)

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

    def open_chatbot(self):
        GeminiChatbot(self.root)

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
                text="Thanks for playing! Click below to return to the difficulty selection screen.",
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

# ==== MAIN APP ENTRY ====
if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")

    all_questions = [
        {
            "question": "A caller reports chest pain, shortness of breath, and sweating. What should be dispatched?",
            "options": ["Fire Engine", "Police Unit", "Ambulance", "Public Works"],
            "answer": "Ambulance"
        },
        {
            "question": "Which of these is NOT a priority for first responders at a hazardous material spill?",
            "options": ["Isolate the area", "Evacuate civilians", "Begin immediate cleanup", "Call for specialized units"],
            "answer": "Begin immediate cleanup"
        },
        {
            "question": "A 911 call comes in for a house fire with possible people trapped inside. What is your first action?",
            "options": ["Send one fire truck", "Dispatch fire, police, and ambulance", "Call the caller back", "Wait for more info"],
            "answer": "Dispatch fire, police, and ambulance"
        },
        {
            "question": "An unconscious person is found at a playground. What should you do first?",
            "options": ["Send an ambulance", "Send police", "Send animal control", "Ignore call"],
            "answer": "Send an ambulance"
        },
        {
            "question": "If a traffic accident has injuries and spilled fuel, who should be dispatched?",
            "options": ["Fire and ambulance", "Police only", "Animal control", "None"],
            "answer": "Fire and ambulance"
        }
        # Add more questions in this format
    ]

    StartPage(root, all_questions)
    root.mainloop()
