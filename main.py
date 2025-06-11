import os

from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, Tool

from helpers import SCREENSHOTS_DIRECTORY, rename_and_move_screenshot
from helpers import list_categories, get_newest_screenshot, create_directory

newest_screenshot = get_newest_screenshot()

with open(os.path.join(SCREENSHOTS_DIRECTORY, newest_screenshot), "rb") as file:
    data = file.read()

rename_file_agent = Agent(
    model="google-gla:gemini-2.0-flash",
    system_prompt="Come up with one descriptive filename for the following screenshot. Return just the name."
)

result = rename_file_agent.run_sync([BinaryContent(data=data, media_type="image/png")])

print(result.output)