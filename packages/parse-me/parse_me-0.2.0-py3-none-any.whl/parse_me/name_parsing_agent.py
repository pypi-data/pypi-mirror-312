from typing import List
from pydantic import BaseModel, Field
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from parse_me.name_parsing_prompts import BASIC_PROMPT, INSTRUCTIONS, EXAMPLE_HE, EXAMPLE_AR, BASIC_NAME_PARTS

# Define a Pydantic model to enforce the structure of the output
class ParsedName(BaseModel):
    original_name: str = Field(..., description="Provide the original name that was parsed.")
    name_parts: dict = Field(..., description="Provide the name parts as a dictionary.")
    explanations: List[str] = Field(..., description="Provide explanations and justifications for your parsing.")

# Agent that uses JSON mode
json_mode_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description=BASIC_PROMPT.format(language="Judeo-Arabic", name_parts=BASIC_NAME_PARTS, example=EXAMPLE_AR),
    response_model=ParsedName,
)
# # Agent that uses structured outputs
# structured_output_agent = Agent(
#     model=OpenAIChat(id="gpt-4o-2024-08-06"),
#     description="You write movie scripts.",
#     response_model=ParsedName,
#     structured_outputs=True,
# )

if __name__ == '__main__':
    # Run the agent
    res: ParsedName = json_mode_agent.run(message=INSTRUCTIONS.format(name="ʿAbd al-Dāʾim (al-Muwaffaq) b. ʿAbd al-ʿAzīz b. Maḥāsin ʾIsrāʾīlī al-Mutaṭabbib", background="From the Cairo Geniza, a Jewish physician and philosopher in the 11th century.")).content
    print(res)
# structured_output_agent.print_response("New York")