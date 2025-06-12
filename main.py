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

class Filename(BaseModel):
    filename: str

rename_file_agent = Agent(
    model="google-gla:gemini-2.0-flash",
    system_prompt="Come up with one descriptive filename for the following screenshot. Return just the name.",
    output_type=Filename
)

result = rename_file_agent.run_sync([BinaryContent(data=data, media_type="image/png")])

filename = result.output.filename

class Category(BaseModel):
    category: str

category_agent = Agent(
    "google-gla:gemini-1.5-flash-8b",
    system_prompt="""You will get a list of categories and then you will get a filename for a screenshot. 
    Decide if the screenshot should be in an existing category or if a new category should be created for that screenshot. 
    Return the category.""",
    output_type=Category
)

results = category_agent.run_sync(f"""
    Categories: {list_categories()}
    Filename: {filename}
""")

category = results.output.category

move_file_agent = Agent(
    "google-gla:gemini-1.5-flash",
    system_prompt="You will get a filename and a category. Use the tools to first create a category and then move the file to that category.",
    tools=[Tool(create_directory, takes_ctx=False), Tool(rename_and_move_screenshot, takes_ctx=False)]
)

move_file_agent.run_sync(
    f"Filename: {filename}\n" \
    f"Category: {category}\n"
)