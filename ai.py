import google.generativeai as genai


# Set up Gemini API key (REPLACE with your actual key!)
genai.configure(api_key="AIzaSyDUu1ByaWZ7oHyhRBk7UpELnT7tzCl_J5g")
model = genai.GenerativeModel("gemini-1.5-flash")


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


 
