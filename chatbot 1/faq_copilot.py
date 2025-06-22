# importing libraries
import requests

# Assigning the azure function app url to the variable
AZURE_FUNCTION_URL = "https://pirates-functions.azurewebsites.net/api/faq_copilot"


# take the prompt from the user through endpoint into the model
def send_question_to_backend(question, feedback=None, suggestion=None):
    """Send a question (optionally with feedback/suggestion) to Azure Function."""
    payload = {
        "question": question,
        "feedback": feedback,
        "suggestion": suggestion
    }

    try:
        response = requests.post(
            AZURE_FUNCTION_URL,
            headers={"Content-Type": "application/json"},
            json=payload
        )

        if response.status_code == 200:
            return response.json().get("answer", "No answer found.")
        else:
            return f"Error {response.status_code}: Unable to get answer."

    except Exception as e:
        return f"Exception occurred: {str(e)}"


def main():
    """Main loop to interact with the FAQ Copilot."""
    print("\nWelcome to the Pirate's FAQ Jack Sparrow's Copilot!")
    print("Type your question or 'exit' to quit.\n")

    while True:
        question = input(" You: ").strip()
        if question.lower() == "exit":
            print(" Goodbye!")
            break

        answer = send_question_to_backend(question)
        print(f" Copilot: {answer}")

        feedback = input("Was this answer helpful? (yes/no): ").strip().lower()
        if feedback in ['yes', 'no']:
            suggestion = None
            if feedback == 'no':
                suggestion = input("Suggest a better question to train the model : ").strip()
            send_question_to_backend(question, feedback=feedback, suggestion=suggestion)


if __name__ == "__main__":
    main()
