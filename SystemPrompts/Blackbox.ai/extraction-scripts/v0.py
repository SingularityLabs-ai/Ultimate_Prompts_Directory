import re
import os

def extract_prompt_templates(filepath):
    """
    Extracts potential prompt templates (primarily multi-line template literals)
    from a JavaScript/TypeScript file.

    Args:
        filepath (str): The path to the .js or .ts file.

    Returns:
        list: A list of potential prompt template strings.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []

    # Regex to find template literals (strings enclosed in backticks `` ` ``)
    # It handles escaped backticks (\\`) and embedded expressions (${...}) within the literal.
    # It tries its best but might need refinement based on complex nested cases.
    # Using re.DOTALL so '.' matches newline characters as well.
    prompt_template_regex = r'`((?:\\`|[^`])*)`' # Simplified but effective for most cases
    
    # More robust regex handling potential nested structures (might be slower)
    # prompt_template_regex = r'`(?:[^`\\]*(?:\\.[^`\\]*)*)*`' 
    
    # Alternative focusing on structure (less likely if minified)
    # assignment_regex = r'(?:const|let|var)\s+([\w\$]+)\s*=\s*(`(?:\\`|[^`])*`);'

    found_templates = []

    matches = re.findall(prompt_template_regex, content, re.DOTALL)

    print(f"Found {len(matches)} potential template literals.")

    for match_content in matches:
        # The regex group captures the content *inside* the backticks
        template = match_content.strip()

        # Basic filtering: Keep templates that are multi-line, contain XML-like tags,
        # or are reasonably long, as these are more likely to be actual prompts.
        if '\n' in template or ('<' in template and '>' in template) or len(template) > 100:
             # Optional: Remove common JS/TS code patterns if they are mistakenly captured
             # (e.g., if a template literal *only* contains CSS or HTML)
             # This requires more sophisticated filtering. For now, we keep most long/complex ones.
            found_templates.append(template)

    return found_templates

# --- Main Execution ---
if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your extension.js file
    file_to_analyze = "extension.js" 
    # Or provide the full path:
    # file_to_analyze = "/path/to/your/project/extension.js" 

    print(f"Analyzing file: {file_to_analyze}")
    
    templates = extract_prompt_templates(file_to_analyze)

    if templates:
        print(f"\n--- Extracted {len(templates)} Potential Prompt Templates ---")
        for i, template in enumerate(templates):
            print(f"\n--- Template {i+1} ---")
            print(template)
            print("--------------------")
    else:
        print("\nNo likely prompt templates (long/multi-line/tagged template literals) found.")