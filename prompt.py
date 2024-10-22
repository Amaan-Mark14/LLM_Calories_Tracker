from openai import OpenAI
import re

# Point to the local server
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")


def get_calories_from_llm(food_item):
    """
    Send a prompt to the LLM to estimate the calories for the given food item.

    Args:
    food_item (str): Description of the food item (e.g., "1 apple").

    Returns:
    str: The estimated calories from the LLM response.
    """

    # Create a completion request to the LM Studio API
    completion = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are BOB a robot that can only talk in numbers. Your task is to carefully analyze how many calories are there in the given food item. Dont state assumptions or provide any explaination. Do not give a range just a single number. Do not forget you can only talk in numbers no /n or new line or units."
            },
            {
                "role": "user",
                "content": food_item  # Directly using the food item
            }
        ],
        max_tokens=100,  # Limit to the expected number of tokens (just a number)
        temperature=0.6, # Ensure deterministic output
    )

    # Extract the LLM response
    llm_response = completion.choices[0].message.content.strip()

    return llm_response


# def get_calories_from_llm(string):
    
#     """
#     Llm is very weak with guessing calories of multiple food items
#     So just get calories of one and then multiply the response 
#     will also work with situations like 300gms of rice 
#     llm will give response for gm of rice and we can multiply that
#     Nmv llm too dumb and thinks 1gm rice is 100 calories and that just multiplies
#     """
    
#     match = re.match(r'(\d+)\s*(.*)', string)

#     if match:
#         number = int(match.group(1))  # Extract the number
#         stripped_string = match.group(2)  # Extract the rest of the string
        
#         # Call the provided function with the stripped string
#         response = llm_response(stripped_string)
        
#         calories = int(response) * int(number)
        
#         # Multiply the result by the extracted number
#         return calories
    
#     else:
#         response = llm_response(string)
#         return response
    
    
# Example usage
if __name__ == "__main__":
    food_item = "10gm of rice"  # Include quantity for better estimation
    calories = get_calories_from_llm(food_item)
    print(f"Calories in {food_item}: {calories}")
