import json


def create_client(model: str, api_key: str):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model,generation_config={"response_mime_type": "application/json"})


def _build_prompt(command):
    return f"""
You are the world's best Ubuntu Linux expert.

Your goal is to help poor users who mistype their Linux commands.

The user entered the following command and received an error message.

[COMMAND]
{command.script}
[ERROR MESSAGE]
{command.output}

[INSTRUCTIONS]
To help the user resolve the error, suggest three fixed command candidates to the user in descending order of priority.
(The higher the priority number, the higher the suitability.)

Using this JSON schema:
  CommandCandidate = {{"priority": int, "command": str}}
Return a `List[CommandCandidate]`


<User> : aptget install git
<ASSISTANT> : [{{
    "priority": 3,
    "command": "sudo apt-get install git"
}}, {{
    "priority": 2,
    "command": "sudo apt install git"
}}, {{
    "priority": 1,
    "command": "sudo apt-get install git-core"
}}]

<User> : rf -rm /dir
<ASSISTANT> : [{{
    "priority": 3,
    "command": "rm -rf /dir"
}}, {{
    "priority": 2,
    "command": "rm -rf /dir/"
}}, {{
    "priority": 1,
    "command": "rm -rf /dir/*"
}}]

<User> : doker run ubuntu:22.04
<ASSISTANT> : [{{
    "priority": 3,
    "command": "docker run ubuntu:22.04"
}}, {{
    "priority": 2,
    "command": "sudo docker run ubuntu:20.04"
}}, {{
    "priority": 1,
    "command": "docker run ubuntu:18.04 /bin/bash"
}}]

<User> : berw install git
<ASSISTANT> : [{{
    "priority": 3,
    "command": "brew install git"
}}, {{
    "priority": 2,
    "command": "brew install git-lfs"
}}, {{
    "priority": 1,
    "command": "brew install git-flow"
}}]

<User> : {command.script}
<ASSISTANT> : 

"""


def get_new_commands(client, command):
    prompt = _build_prompt(command)
    response = client.generate_content(prompt)
    
    json_response = _parse_raw_json_response(response.text)
    return json_response

def _parse_raw_json_response(response:str):
    return json.loads(response)