import re
import os

def extract_prompt_templates(filepath, output_filepath="extracted_prompts.txt"):
    """
    Extracts potential prompt templates (primarily multi-line template literals)
    from a JavaScript/TypeScript file and saves them to an output file.

    Args:
        filepath (str): The path to the .js or .ts file.
        output_filepath (str): The path where the extracted templates will be saved.

    Returns:
        int: The number of potential templates saved to the file, or -1 on error.
    """
    if not os.path.exists(filepath):
        print(f"Error: Input file not found at {filepath}")
        return -1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file {filepath}: {e}")
        return -1

    # Regex to find template literals (strings enclosed in backticks `` ` ``)
    # Handles escaped backticks (\\`) and embedded expressions (${...})
    prompt_template_regex = r'`((?:\\`|[^`])*)`'

    found_templates = []
    templates_saved_count = 0

    try:
        matches = re.findall(prompt_template_regex, content, re.DOTALL)
        print(f"Found {len(matches)} potential template literals in the source.")

        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(f"--- Extracted Potential Prompt Templates from: {filepath} ---\n\n")

            for i, match_content in enumerate(matches):
                template = match_content.strip()

                # Basic filtering (multi-line, contains tags, or reasonably long)
                if '\n' in template or ('<' in template and '>' in template) or len(template) > 100:
                    outfile.write(f"--- Template {templates_saved_count + 1} ---\n")
                    outfile.write(template)
                    outfile.write("\n\n--------------------\n\n")
                    templates_saved_count += 1

        print(f"Successfully saved {templates_saved_count} potential templates to: {output_filepath}")
        return templates_saved_count

    except Exception as e:
        print(f"An error occurred during extraction or writing to file: {e}")
        return -1

# --- Main Execution ---
if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your extension.js file
    file_to_analyze = "extension.js" 
    # Or provide the full path:
    # file_to_analyze = "/path/to/your/project/extension.js"

    # Define the output file name
    output_file = "extracted_prompts.txt"

    print(f"Analyzing file: {file_to_analyze}")
    
    count = extract_prompt_templates(file_to_analyze, output_file)

    if count > 0:
        print(f"Extraction complete. Check the file '{output_file}' for results.")
    elif count == 0:
         print(f"\nNo likely prompt templates (long/multi-line/tagged template literals) found or saved to '{output_file}'.")
    else:
        print("Extraction failed due to an error.")