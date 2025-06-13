from openai import OpenAI


# This class makes it very easy to use instances of ChatGPT with clearly
# defined roles and short-term memory
class EasyGPT:

    def __init__(self, instructions: str):
        self.client = OpenAI()
        self.instructs = instructions  # The role of this gpt instance
        self.history = ""              # Conversation history

    def send(self, data):

        self.history += f"User:\n\n{data}\n\n"

        # Retrieve the response from the instance
        response = self.client.responses.create(
            model="gpt-4o",
            instructions=self.instructs,
            input=self.history
        )

        # Create a log entry from the log and response, add the entry to the
        # conversation history
        self.history += f"ChatGPT:\n\n{response.output_text}\n\n"
        log = f"User:\n\n{data}\n\nChatGPT:\n\n{response.output_text}\n\n"

        # Write the entry to the log file
        with open("log.md", "a", encoding='utf-8') as f:
            f.write(log)

        print(response.output_text)

        # If the response is in code, remove the starting and ending flags to
        # make it writable
        if response.output_text[:3] == r"```":
            lines = response.output_text.splitlines()
            print(f"Removing: {lines[0]} and {lines[-1]}")
            return '\n'.join(lines[1:-1])
        
        return response.output_text