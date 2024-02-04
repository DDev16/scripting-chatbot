import json 
import random

# Get recent messages

def get_recent_messages():
   
   # Define the file name and learn instructions
    
    file_name = "stored_data.json"
    learn_instruction = {
    "role": "system",
    "content": "I am a Spanish teacher with experience in teaching Spanish as a second language. I am looking for students who want to improve their Spanish skills. I can provide lessons online or in-person. My teaching approach focuses on conversational skills, grammar, and cultural understanding. I am available for both individual and group lessons. Please assist me in finding students who are interested in learning Spanish and provide relevant information."
}





    # Initialize messages
    messages = []

    # Add a random element 
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include humor."
    # else:
    #     learn_instruction["content"] = learn_instruction["content"] + " Your response detailed repsonse. very human like."


    # Append instruction to messages
    messages.append(learn_instruction)

    # Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append last 5 items of data
            if data:
                if len(data) < 5:
                        for item in data:
                            messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass 

    # Return messages
    return messages

# Store messages
def store_messages(request_message, response_message):

    # Define the file name
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messsages to data
    user_message = {'role': 'user', 'content': request_message }
    assistant_message = {'role': 'assistant', 'content': response_message }
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file 
    with open(file_name, 'w') as f:
        json.dump(messages, f)

    # Reset Messages
def reset_messages():
      # Overwrite the file with nothing
      open("stored_data.json", "w")