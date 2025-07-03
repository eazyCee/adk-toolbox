#  Copyright 2025 Google LLC
 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
 
#       https://www.apache.org/licenses/LICENSE-2.0
 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from google.adk.agents import Agent
from google.adk.tools.toolbox_tool import ToolboxTool
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import DatabaseSessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types
import os
from flask import Flask, request, jsonify

TOOLBOX_URL = os.environ.get('TOOLBOX_URL')
DATABASE_URL = os.environ.get('DATABASE_URL')
toolbox_tools = ToolboxTool(TOOLBOX_URL)

# Ensure the toolset name matches what your tool server exposes
toolset = toolbox_tools.get_toolset("my-toolset") 

session_service = DatabaseSessionService(db_url=DATABASE_URL)
artifacts_service = InMemoryArtifactService()


app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "ADK Agent API is running."}), 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data.get('query')
    content = types.Content(role='user', parts=[types.Part(text=user_query)])
    user_id = data.get('user_id', 'default_user') # Get user_id or use a default
    session_id = data.get('session_id') # Optional: client can pass session_id to continue a conversation

    currentlyLoggedInCompany = data.get('company') # This could be dynamic per user/session in a real app

    prompt_template = f"""
        You're a helpful analytical assistant for the customers of ESB. You have access to a sql database and are only allowed to execute SELECT queries on the specified restaurant name. Get the data using the provided
        tools to ensure that the data is factual and relevant, and then condense it into a digestable form. Respond using the same language as the query. The current restaurant using you is {currentlyLoggedInCompany}.
    """


    root_agent = Agent(
        model='gemini-2.0-flash', # Using gemini-1.5-flash, as 2.0 isn't a valid model name
        name='sales_analytics_agent',
        description='A sales analytics assistant',
        instruction=prompt_template,
        tools=toolset
    )

    runner = Runner(
        app_name='sales_analytics_agent',
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    if session_id:
        current_session = session_service.get_session(session_id=session_id, app_name='sales_analytics_agent', user_id=user_id)
        if not current_session:
            # If session_id provided but not found, create a new one.
            # Or you could return an error: jsonify({"error": "Session not found"}), 404
            # logger.warning(f"Session ID {session_id} not found. Creating a new session.")
            current_session = session_service.create_session(
                state={}, app_name='sales_analytics_agent', user_id=user_id
            )
    else:
        current_session = session_service.create_session(
            state={}, app_name='sales_analytics_agent', user_id=user_id
        )
    try:
        events = runner.run(session_id=current_session.id,
                        user_id=user_id, new_message=content)
        responses=[]
        current_session.last_update_time = current_session.last_update_time * 1000
        for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        responses.append(part.text)
                    elif hasattr(part, 'function_call') and part.function_call:
                        # Log tool calls if needed, but don't send to user directly
                        # logger.info(f"Tool call: {part.function_call.name} with args {part.function_call.args}")
                        # The agent framework handles the tool call and response internally
                        pass 
        final_response = "\n".join(responses)
        return jsonify({"response": final_response, "session_id": current_session.id})
    except Exception as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))