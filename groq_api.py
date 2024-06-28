from groq import Groq

class GroqAPI :
    def __init__(self):
        self._conversation = [
            {
                "role" : "system",
                "content" : "You are a chat bot that only returns 1 sentence and your name is Rick Sanchez. Your response should only be in sentence format, no new line and fancy symbols, just normal marks."
            }
        ]
        
    def update_conversation(self, new_message) :
        return self._conversation.append(new_message)

    def request(self, message):
        client = Groq(
            api_key="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",
        )
        new_message = {
            "role" : "user",
            "content" : message
        }
        self.update_conversation(new_message)
        # print(self._conversation)
        chat_completion = client.chat.completions.create(
            messages=self._conversation,
            model="llama3-8b-8192",
        )
        new_system_message = {
            "role" : "system",
            "content" : chat_completion.choices[0].message.content
        }
        self.update_conversation(new_system_message)
        return chat_completion.choices[0].message.content
    
# def main():
#     api = GroqAPI()
#     while True:
#         user_input = input("You: ")
#         response = api.request(user_input)
#         print("AI: ", response)

# if __name__ == "__main__":
#     main()