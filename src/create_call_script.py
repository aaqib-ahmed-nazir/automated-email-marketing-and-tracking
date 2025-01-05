from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from utils import set_api_key_env

# Load environment variables and API keys
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
set_api_key_env("OPENAI_API_KEY", openai_api_key)

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o")

# Define a simple call script prompt template
call_script_prompt_template = ChatPromptTemplate([
    ("system", "You are a professional sales assistant. Generate **only a short opening line** for a cold sales call that grabs the user's attention and sets a positive tone. Keep it to 3-4 lines max."),
    ("user", "Here is the email content: {email_content}. Generate a persuasive and concise call script for the sales representative.")
])

# Create an agent by combining the prompt and model
call_script_agent = call_script_prompt_template | llm

def generate_call_script(email_content: str) -> str:
    """
    Generate a call script based on the provided email content.

    Args:
        email_content (str): The content of the email to base the call script on.

    Returns:
        str: The generated call script.
    """
    try:
        # Invoke the model and get the response
        response = call_script_agent.invoke({"email_content": email_content})
        return response.content
    except Exception as e:
        print(f"Error generating call script: {e}")
        return "An error occurred while generating the call script."

# if __name__ == "__main__":
#     sample_email = """I hope this email finds you well.

#             My name is Fox, and I am the CEO at Vigilant Software. We provide healthcare institutions with advanced software solutions that optimize operations and enhance service efficiency.

#             At Vigilant Software, we offer two standout products that I believe could greatly benefit your organization. Our Customizable Medication Labels enhance patient safety and compliance by providing clear and standardized labeling for intravenous devices, reducing medication errors without additional costs or reprogramming. Additionally, our Verify ICU™ automates the creation of compliant IV tube labels on-demand, improving workflow for ICU nurses and ensuring adherence to best practices with minimal setup.

#             Our solutions are trusted by executives like Sarah Jones, Director of Operations at Community Memorial Healthcare, and the team at CHI St Joseph Regional Health Care Center to enhance efficiency and reduce errors. Their positive experiences underscore the significant impact our products can have.

#             We’d love to discuss how Vigilant Software can address your specific needs and improve your operations at Valley Healthlink. Would you be open to scheduling a brief call or meeting at your convenience?

#             Looking forward to connecting and assisting you in enhancing your hospital’s operational efficiency.

#             Best regards"""
#     call_script = generate_call_script(sample_email)
#     print("Generated Call Script:\n", call_script)