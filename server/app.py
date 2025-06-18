import os
import requests
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import os
from langchain_google_community import GoogleSearchAPIWrapper
from flask import Flask, jsonify, request

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration from Environment Variables ---
# Your Twilio Account SID and Auth Token
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Your Langflow API URL (e.g., http://localhost:7860/api/v1/run)
# Replace with your actual Langflow flow's API endpoint
LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/run/753e288d-4880-415f-a42e-13961826bb8b" #os.getenv('LANGFLOW_API_URL')##
# Your Langflow API Key (if your flow requires authentication)
LANGFLOW_API_KEY = os.getenv('LANGFLOW_API_KEY')

# --- Helper Function to Call Langflow API ---
# --- Helper Function to Call Langflow API ---
# --- Helper Function to Call Langflow API ---
def call_langflow_api(user_input):
    """
    Sends the user's transcribed input to the Langflow API and returns the AI's response.
    """
    if not LANGFLOW_API_URL:
        print("Error: LANGFLOW_API_URL is not set.")
        return "I'm sorry, the AI service is not configured."

    headers = {
        "Content-Type": "application/json",
    }
    # Note: Remove API key header since your expected request doesn't use it
    # if LANGFLOW_API_KEY:
    #     headers["X-API-Key"] = LANGFLOW_API_KEY

    # Fixed payload structure to match expected format

    payload = {
        "input_value": user_input,  # Changed from nested "input" object
        "output_type": "chat",      # Keep as specified
        "input_type": "chat"        # Added missing input_type
    }

    try:
        print(f"Sending to Langflow: {user_input}")
        response = requests.post(LANGFLOW_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        langflow_response = response.json()
        print(f"Received from Langflow: {langflow_response}")

        # Extract the actual response text from the Langflow response structure
        try:
            # Navigate through the nested JSON structure
            outputs = langflow_response.get('outputs', [])
            if outputs and len(outputs) > 0:
                first_output = outputs[0]
                results = first_output.get('outputs', [])
                if results and len(results) > 0:
                    result = results[0]
                    # The actual text is nested deep in the structure
                    message_data = result.get('results', {}).get('message', {})
                    if isinstance(message_data, dict):
                        # Try multiple possible paths to the text
                        text = (message_data.get('data', {}).get('text') or 
                               message_data.get('text') or
                               result.get('artifacts', {}).get('message') or
                               result.get('outputs', {}).get('message', {}).get('message'))
                        
                        if text:
                            return text
            
            # Fallback: look for any 'message' field in the response
            if 'message' in str(langflow_response):
                # Try to extract from messages array
                outputs = langflow_response.get('outputs', [])
                if outputs:
                    messages = outputs[0].get('outputs', [{}])[0].get('messages', [])
                    if messages:
                        return messages[0].get('message', '')
            
            return "I received a response from the AI, but couldn't extract the message."
            
        except (KeyError, IndexError, TypeError) as parse_error:
            print(f"Error parsing response structure: {parse_error}")
            return "I received a response from the AI, but couldn't parse it properly."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Langflow API: {e}")
        return "I'm sorry, I'm having trouble connecting to the AI service right now."
    except ValueError as e:
        print(f"Error parsing Langflow response: {e}")
        return "I'm sorry, I received an invalid response from the AI service."

# --- Twilio Voice Webhook ---
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """
    Handles incoming Twilio voice calls.
    """
    response = VoiceResponse()
    speech_result = request.form.get('SpeechResult')
    

    if speech_result:
        print(f"User said: {speech_result}")
        # Process the user's speech with Langflow
        ai_response_text = call_langflow_api(speech_result)
        response.say(ai_response_text)
    else:
        # Initial greeting for a new call
        response.say("Hello! How can I help you today?")

    # Always gather more input after speaking
    # Set input='speech' to enable speech recognition
    # Set action to point back to this same endpoint for subsequent interactions
    # Set speechTimeout to control how long Twilio waits for speech (in seconds)
    response.gather(input='speech', action='/voice', speechTimeout='auto')

    # If the user doesn't say anything after the gather, or if there's an error
    # and the gather times out, Twilio will hit this endpoint again without SpeechResult.
    # We can add a fallback or simply hang up.
    if not speech_result:
        response.say("I didn't hear anything. Goodbye!")
        response.hangup()

    return str(response)


@app.route('/search')
def test_your_search():
    """Search only for S3 bucket interview questions"""
    
    try:
        # Initialize search
        search = GoogleSearchAPIWrapper(
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            google_cse_id=os.getenv('GOOGLE_CSE_ID'),
            k=3
        )
        
        print("🪣 Searching for S3 bucket interview questions...")
        
        # Simple, focused search query
        search_query = "S3 bucket interview questions AWS"
        
        # Perform search
        results = search.results(search_query, num_results=3)
        print(f"✅ Found {len(results)} S3 bucket results")
        
        # Prepare response
        response_data = {
            "status": "success",
            "message": f"Found {len(results)} S3 bucket interview questions",
            "results_count": len(results),
            "results": []
        }
        
        # Process results
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            link = result.get('link', 'No link')
            snippet = result.get('snippet', 'No snippet')
            
            print(f"{i}. {title}")
            print(f"   {link}")
            print()
            
            response_data["results"].append({
                "index": i,
                "title": title,
                "link": link,
                "snippet": snippet
            })
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        return jsonify({
            "status": "error",
            "message": str(e),
            "results_count": 0,
            "results": []
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Docker and load balancers."""
    return jsonify({
        "status": "healthy",
        "service": "hackathon-langflow-twilio",
        "timestamp": "2024-01-01T00:00:00Z"
    }), 200

# --- Main execution block ---
if __name__ == "__main__":
    # Ensure environment variables are set before running
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not LANGFLOW_API_URL:
        print("Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and LANGFLOW_API_URL environment variables.")
        print("You can create a .env file in the same directory as this script.")
        print("Example .env content:")
        print("TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("TWILIO_AUTH_TOKEN=your_auth_token")
        print("LANGFLOW_API_URL=http://localhost:7860/api/v1/run/your_flow_id")
        print("LANGFLOW_API_KEY=your_langflow_api_key_if_any")
    else:
        print("Flask app starting...")
        app.run(debug=True, port=5000) # Run in debug mode for development