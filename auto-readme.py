from openai import OpenAI
import sys
import os

"""
Make sure your OpenAI API key is correctly set in your environment variables before running this script. 
The script is designed to interactively refine the generated README based on your feedback.
"""

# Initialize OpenAI client with API key from environment variable 'OPENAI_API_KEY'
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_readme_from_code(code_content, note="", api_key=""):
    """
    Generates a README from a script using OpenAI's GPT-3 API.
    - code_content: String content of the script.
    - note: Additional note for refinement (optional).
    - api_key: OpenAI API key.
    """
    if not api_key:
        print("Error: OPENAI_API_KEY is not provided.")
        return None

    try:
        # Constructing the prompt for OpenAI's GPT-3 model
        prompt = (
            f"Analyze the following code and create a comprehensive README file. "
            f"The README should include:\n\n"
            f"1. An overview section that summarizes the purpose and functionality of the script.\n"
            f"2. Installation instructions, detailing any dependencies and steps to get the script running.\n"
            f"3. Usage instructions, explaining how to use the script.\n"
            f"4. Any additional notes or warnings that users should be aware of.\n"
            f"5. A brief section on how to contribute to the script.\n\n"
            f"Script:\n{code_content}\n\n"
            f"Note: {note}"
        )

        # Generating the README content using OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are going to help analyze my script to generate a README file."},
                {"role": "user", "content": prompt}
            ],
        )
        response_message = response.choices[0].message.content

        # Check if the response is empty
        if not response_message.strip():
            print("Received an empty response from OpenAI. Please try again.")
            return None

        return response_message.strip()
    except Exception as e:
        print(f"Error generating README: {e}")
        return None

def read_file(file_path):
    """
    Reads the content of a file and returns it.
    - file_path: Path to the file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python auto-readme.py <path_to_code_file>")
        sys.exit(1)

    code_path = sys.argv[1]
    code_content = read_file(code_path)

    readme_content = generate_readme_from_code(code_content, api_key=os.getenv('OPENAI_API_KEY'))

    while readme_content:
        print("\nGenerated README:\n")
        print(readme_content)
        feedback = input("\nIs this README acceptable? (yes/no): ").lower()
        if feedback == 'yes':
            with open('README.md', 'w') as readme_file:
                readme_file.write(readme_content)
            print("README.md written to the current directory.")
            break
        else:
            note = input("Enter your feedback note for improvement: ")
            readme_content = generate_readme_from_code(code_content, note, api_key=os.getenv('OPENAI_API_KEY'))

    if not readme_content:
        print("Failed to generate a README. Exiting.")