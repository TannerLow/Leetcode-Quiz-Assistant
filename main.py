import os

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
import dotenv
import asyncio

from neetcode_plugin import NeetcodePlugin


dotenv.load_dotenv()


chat_completion_service = OpenAIChatCompletion(
    ai_model_id="gpt-5-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),
    service_id="openai"
)

# Initialize the kernel
kernel = Kernel()

# Create the plugin
neetcode_plugin = NeetcodePlugin('./data')

# Add the plugin to the kernel
kernel.add_plugin(neetcode_plugin)

kernel.add_service(chat_completion_service)

chat_history = ChatHistory()

execution_settings = OpenAIChatPromptExecutionSettings()
execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

def load_system_prompt(chat_history: ChatHistory) -> None:
    with open("prompt.txt", "r") as file:
        system_prompt: str = file.read().strip()
        chat_history.add_system_message(system_prompt)

async def main():
    load_system_prompt(chat_history)

    # AI starts the convo
    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
        kernel=kernel
    )
    print("Assistant > " + str(response))
    chat_history.add_message(response)

    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        if userInput == "exit and debug":
            with open('debug.txt', 'w') as file:
                file.write(chat_history.model_dump_json(indent=4))
        
        chat_history.add_user_message(userInput)

        response = await chat_completion_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel
        )

        # Print the results
        print("Assistant > " + str(response))

        # Add the message from the agent to the chat history
        chat_history.add_message(response)

if __name__ == "__main__":
    asyncio.run(main())
