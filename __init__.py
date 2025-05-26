import azure.functions as func
import requests
import json
import logging

# Entry point for the Azure Function
# This function is triggered when an HTTP POST request is made to the endpoint


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("\U0001F41E Pirate FAQ Function has been triggered.")

    try:
        # Try to parse the incoming JSON request body
        req_body = req.get_json()

        # Extract the question, feedback, and suggestion from the request
        user_question = req_body.get('question')
        user_feedback = req_body.get('feedback')  # Optional user feedback (yes/no)
        user_suggestion = req_body.get('suggestion')  # Optional user suggestion for better training

        # Return a 400 error if question is missing
        if not user_question:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'question' field in request."}),
                status_code=400,
                mimetype="application/json"
            )

        # Define your Azure AI Foundry endpoint and API key here
        model_url = "https://ashwi-mb2y0ewk-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o-FAQ/chat/completions?api-version=2025-01-01-preview"

        headers = {
            "Authorization": "Bearer 4YOSt1cZVegzeXAXtiHliGhkFBhlF9im8qcyjBoDgqAzSeBGsXJH",
            "Content-Type": "application/json"
        }

        # Format the request for OpenAI-compatible chat completion
        # You can modify temperature or max_tokens as needed
        payload = {
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }

        # Send the request to the Azure AI Foundry model
        response = requests.post(model_url, headers=headers, json=payload)

        # Handle failure in contacting model API
        if response.status_code != 200:
            logging.error(f"Model error: {response.text}")
            return func.HttpResponse(
                json.dumps({"error": "Failed to contact AI model."}),
                status_code=500,
                mimetype="application/json"
            )

        # Extract answer from the model's response
        model_response = response.json()
        answer = model_response.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no answer found.")

        # Log user inputs and model output for improvement
        log_data = {
            "question": user_question,
            "answer": answer,
            "feedback": user_feedback,
            "suggestion": user_suggestion
        }
        logging.info(f"Log: {json.dumps(log_data)}")

        # Return answer to client
        return func.HttpResponse(
            json.dumps({"answer": answer}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        # Catch any unexpected errors and return a 500 response
        logging.error(f"Exception occurred: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "An internal server error occurred."}),
            status_code=500,
            mimetype="application/json"
        )
