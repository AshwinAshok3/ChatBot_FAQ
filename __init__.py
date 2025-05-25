import azure.functions as func
import requests
import json
import logging

# Azure Function triggered by HTTP request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing an FAQ query request.")

    try:
        req_body = req.get_json()
        user_question = req_body.get('question')
        user_feedback = req_body.get('feedback')  # Optional feedback
        user_suggestion = req_body.get('suggestion')  # Optional new Q

        if not user_question:
            return func.HttpResponse("Missing 'question' field", status_code=400)

        # Call Azure AI Foundry model endpoint
        model_url = "https://YOUR_FOUNDATION_ENDPOINT"  # Replace with actual
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",      # Replace with actual
            "Content-Type": "application/json"
        }

        payload = {"input": user_question}
        response = requests.post(model_url, headers=headers, json=payload)

        if response.status_code != 200:
            return func.HttpResponse("Failed to contact AI model.", status_code=500)

        result = response.json()
        answer = result.get("answer", "Sorry, no answer found.")

        # Log feedback or suggestions if provided
        log_data = {
            "question": user_question,
            "answer": answer,
            "feedback": user_feedback,
            "suggestion": user_suggestion
        }

        logging.info(f"Log Data: {json.dumps(log_data)}")

        return func.HttpResponse(
            json.dumps({"answer": answer}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "An internal error occurred."}),
            status_code=500,
            mimetype="application/json"
        )
