import os

from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent, Tool

from helpers import SCREENSHOTS_DIRECTORY, rename_and_move_screenshot
from helpers import list_categories, get_newest_screenshot, create_directory

newest_screenshot = get_newest_screenshot()
print(f"Newest Screenshot: {newest_screenshot}\n")

with open(os.path.join(SCREENSHOTS_DIRECTORY, newest_screenshot), "rb") as file:
    data = file.read()

class Description(BaseModel):
    description: str

describe_file_agent = Agent(
    model="google-gla:gemini-2.0-flash",
    # system_prompt="Come up with one descriptive filename for the following screenshot. Return just the name.",
    system_prompt="""Describe the contents of this screenshot in detail. 
    Include information about the interface, visible text, layout, colors, icons, user interactions and any other relevant elements. 
    Mention the context if it can be inferred (e.g., what app or website it might be, what action the user is performing). 
    Be objective and specific.""",
    output_type=Description
)

result = describe_file_agent.run_sync([BinaryContent(data=data, media_type="image/png")])

description = result.output.description
print(f"Description: {description}")

class Category(BaseModel):
    category: str

category_agent = Agent(
    "google-gla:gemini-2.5-flash-preview-05-20",
    system_prompt="""You will get a list of categories and then you will get a description for a screenshot. 
    Decide if the screenshot should be in an existing category or if a new category should be created for that screenshot. 
    Return the category.""",
    output_type=Category
)

results = category_agent.run_sync(f"""
    Categories: {list_categories()}
    Description: {description}
""")

category = results.output.category
print(f"\n\nList Categories: {list_categories()}\n")

print(f"\nSelected Category: {category}\n\n")

move_file_agent = Agent(
    "google-gla:gemini-2.5-flash-preview-05-20",
    system_prompt="You will get a filename and a category. Use the tools to first create a category and then move the file to that category.",
    tools=[Tool(create_directory, takes_ctx=False), Tool(rename_and_move_screenshot, takes_ctx=False)]
)

move_file_agent.run_sync(
    f"Filename: {newest_screenshot}\n" \
    f"Category: {category}\n"
)