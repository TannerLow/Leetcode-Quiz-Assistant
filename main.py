import os
import json

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
import dotenv
import asyncio

from src.neetcode_plugin import NeetcodePlugin


dotenv.load_dotenv()


chat_completion_service = OpenAIChatCompletion(
    ai_model_id="gpt-5-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),
    service_id="openai"
)

# Initialize the kernel
kernel = Kernel()

# Create the plugin
user_data_file = './user_data/stats.json'
neetcode_plugin = NeetcodePlugin('./data', user_data_file)

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


def setup_user_data(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):

        with open(path, 'w') as file:
            initial_data = {
                "levels": {},
                "skips": {}
            }
            json.dump(initial_data, file)
            

async def main():
    setup_user_data(user_data_file)

    load_system_prompt(chat_history)

    # AI starts the convo
    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
        kernel=kernel
    )
    print("Assistant > " + str(response), end='\n\n')
    chat_history.add_message(response)

    userInput = None
    while True:
        # Collect user input
        print("=" * 20)
        userInput = input("User > ")
        print()

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        if userInput == "exit and debug":
            with open('debug.txt', 'w') as file:
                file.write(chat_history.model_dump_json(indent=4))
        
        chat_history.add_user_message(userInput)

        print("[AI is thinking...]")
        response = await chat_completion_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel
        )

        print("=" * 20)
        print("Assistant > " + str(response), end='\n\n')

        # Add the message from the agent to the chat history
        chat_history.add_message(response)


if __name__ == "__main__":
    asyncio.run(main())
