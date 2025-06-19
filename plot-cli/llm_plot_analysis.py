import google.generativeai as genai
from google import genai
import os
import argparse

# --- NOTES FOR USER: ---
    # To run this script, you need to obtain your own Google Gemini API Key
    # and set it as an environment variable named GOOGLE_API_KEY.
    #
    # How to obtain an API Key:
    # 1. Go to Google AI Studio: https://aistudio.google.com/
    # 2. Log in with your Google account.
    # 3. Create a new API key or use an existing one.
    #
    # How to set the GOOGLE_API_KEY environment variable:
    #
    # For Linux/macOS (add to your ~/.bashrc, ~/.zshrc, or similar, then `source` the file or restart terminal):
    #    export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    #
    # For Windows (Command Prompt, temporary for current session):
    #    set GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    #
    # For Windows (PowerShell, temporary for current session):
    #    $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    #
    # Replace "YOUR_API_KEY_HERE" with the actual API key you obtained.
    # It's highly recommended NOT to hardcode your API key directly in the script.
# ---------------------------------


def main():

    parser = argparse.ArgumentParser(description="Generate LLM anaylsis of plots.")
    parser.add_argument("--infile", help="Path to the first input image file.", required=True)
    parser.add_argument("--infile2", help="Path to the second input image file (optional, for comparison).")
    parser.add_argument("--outfile", help="Path to the output markdown file.", required=True)
    args = parser.parse_args()

    if not args.infile:
        raise ValueError("At least one input image file must be specified with --infile argument.")
    if not args.outfile:
        raise ValueError("Output file must be specified with --outfile argument.")
    
    print(f"Input file 1: {args.infile}")
    if args.infile2:
        print(f"Input file 2: {args.infile2}")
    print(f"Output file: {args.outfile}")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=google_api_key)

    uploaded_file1 = client.files.upload(file=args.infile)

    contents = [uploaded_file1]
    prompt_role = "Act as a data scientist to summarize the chart and provide a quantitative analysis of the key trends, relationships, and statistics of the provided chart. Be specific and mention any notable patterns or outliers. Calculate meaningful statistics from the plot."

    if args.infile2:
        uploaded_file2 = client.files.upload(file=args.infile2)
        contents = [uploaded_file1, uploaded_file2]
        prompt_role = "Act as a data scientist to compare and contrast the two provided charts. Provide a quantitative analysis of the key trends, relationships, and statistics, highlighting similarities and differences. Be specific and mention any notable patterns or outliers. Calculate meaningful statistics from the plots."

    gemma_response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=contents + [prompt_role],
    )

    gemma_response_md = args.outfile

    with open(gemma_response_md, 'w', newline='', encoding='utf-8') as mdfile:
        mdfile.write("# Plot Analysis\n")
        mdfile.write(gemma_response.text)


if __name__ == "__main__":
    main()