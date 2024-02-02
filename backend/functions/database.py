import json 
import random

# Get recent messages

def get_recent_messages():
   
   # Define the file name and learn instructions
    
    file_name = "stored_data.json"
    learn_instruction = {
    "role": "system",
    "content": "I am a buyer looking for property in Lake Havasu City, Arizona. My budget is between $500,000 and $800,000. I prefer single-family homes, condos, or townhouses. I'm interested in properties with at least 3 bedrooms and 2 bathrooms, and I have a preference for a swimming pool. Location near Lake Havasu and local amenities is important. I can consider properties that are move-in ready or require minor renovations. I aim to find a property within the next 6 months and am open to price negotiation. As my real estate agent, please assist me in finding suitable properties and providing relevant information."
}




    # Initialize messages
    messages = []

    # Add a random element 
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include statements of unweary feelings about the move."
    # else:
    #     learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question."


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