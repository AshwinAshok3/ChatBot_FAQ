import azure.functions as func
import requests
import json
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("\U0001F41E Pirate FAQ Function has been triggered.")

    try:
        req_body = req.get_json()
        user_question = req_body.get('question')
        user_feedback = req_body.get('feedback')
        user_suggestion = req_body.get('suggestion')

        if not user_question:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'question' field in request."}),
                status_code=400,
                mimetype="application/json"
            )

        # TODO: Set your Azure AI Foundry model endpoint and API key here
        model_url = "https://foundry-pirated.cognitiveservices.azure.com/openai/deployments/gpt-4o-pirated/chat/completions?api-version=2025-01-01-preview"
        api_key = "3dcRXjlE1UToyOITcQeHn0ZhVSfw1ZZ9CM0hRgzB4ReGwtAFR56aJQQJ99BEACfhMk5XJ3w3AAAAACOG8SRk"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }

        response = requests.post(model_url, headers=headers, json=payload)

        if response.status_code != 200:
            logging.error(f"Model error: {response.text}")
            return func.HttpResponse(
                json.dumps({"error": "Failed to contact AI model."}),
                status_code=500,
                mimetype="application/json"
            )

        model_response = response.json()
        answer = model_response.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no answer found.")

        log_data = {
            "question": user_question,
            "answer": answer,
            "feedback": user_feedback,
            "suggestion": user_suggestion
        }
        logging.info(f"Log: {json.dumps(log_data)}")

        return func.HttpResponse(
            json.dumps({"answer": answer}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "An internal server error occurred."}),
            status_code=500,
            mimetype="application/json"
        )
