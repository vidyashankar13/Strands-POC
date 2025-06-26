"""
Main application entry point for Strands Agent Web App
"""
import os
from strands import Agent
from strands_tools import calculator, use_aws, file_write
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Set environment variable to bypass tool consent
os.environ['BYPASS_TOOL_CONSENT'] = 'true'

agent = Agent(tools=[calculator, use_aws, file_write])

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Strands Agent Demo</title>
    <style>
        body {{ background: linear-gradient(135deg, #2d5a27, #4a7c59); font-family: Arial; margin: 0; padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; text-align: center; }}
        h1 {{ color: white; margin-bottom: 30px; }}
        .prompt-box {{ background: rgba(255,255,255,0.9); padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px; }}
        textarea {{ width: 100%; padding: 10px; border: 2px solid #4a7c59; border-radius: 5px; font-size: 14px; resize: vertical; box-sizing: border-box; }}
        input[type="submit"] {{ background: #4a7c59; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
        input[type="submit"]:hover {{ background: #2d5a27; }}
        .response-box {{ background: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: left; }}
        .error-box {{ background: rgba(255,200,200,0.95); border: 2px solid #d32f2f; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        .prompt-display {{ background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: left; }}
        .loading {{ text-align: center; padding: 20px; }}
        .robot {{ font-size: 24px; animation: typing 1.5s infinite; }}
        @keyframes typing {{ 0%, 50% {{ opacity: 1; }} 51%, 100% {{ opacity: 0.3; }} }}
        .note {{ color: rgba(255,255,255,0.8); font-size: 12px; margin-top: 10px; text-align: left; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Strands Agent Demo</h1>
        <div class="prompt-box">
            <form method="post" onsubmit="showLoading()">
                <textarea name="prompt" rows="6" placeholder="Enter your prompt here..."></textarea><br><br>
                <input type="submit" value="Submit">
            </form>
        </div>
        <div class="note">* Auto-approve mode: No confirmation requested before mutations</div>
        {prompt_display}
        {response}
    </div>
    <script>
        function showLoading() {{
            const existingPrompt = document.querySelector('.prompt-display');
            const existingResponse = document.querySelector('.response-box');
            if (existingPrompt) existingPrompt.remove();
            if (existingResponse) existingResponse.remove();
            
            const promptText = document.querySelector('textarea[name="prompt"]').value;
            if (promptText.trim()) {{
                const promptDiv = document.createElement('div');
                promptDiv.className = 'prompt-display';
                promptDiv.innerHTML = '<h3>Your Prompt:</h3><p>' + promptText + '</p>';
                document.querySelector('.note').after(promptDiv);
            }}
            
            setTimeout(function() {{
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'response-box loading';
                loadingDiv.innerHTML = '<div class="robot">🤖</div><p>Processing...</p>';
                document.querySelector('.container').appendChild(loadingDiv);
            }}, 100);
            
            setTimeout(function() {{
                document.querySelector('textarea[name="prompt"]').value = '';
            }}, 200);
        }}
    </script>
</body>
</html>
'''

class AgentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_FORM.format(prompt_display='', response='').encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        if 'prompt' in params:
            prompt = params['prompt'][0]
            prompt_display = f'<div class="prompt-display"><h3>Your Prompt:</h3><p>{prompt}</p></div>'
            
            try:
                print(f"Processing: {prompt}")
                response = agent(prompt)
                response_html = f'<div class="response-box"><h3>Response:</h3><pre>{response}</pre></div>'
            except Exception as e:
                print(f"Error: {e}")
                response_html = f'<div class="response-box error-box"><h3>Error:</h3><pre>{e}</pre></div>'
        else:
            prompt_display = ''
            response_html = '<div class="response-box error-box">No prompt provided</div>'
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_FORM.format(prompt_display=prompt_display, response=response_html).encode())

def main():
    """Main application entry point"""
    print("Initializing Strands Agent Web App...")
    server = HTTPServer(('localhost', 8018), AgentHandler)
    print('Server running on http://localhost:8018')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == '__main__':
    main()