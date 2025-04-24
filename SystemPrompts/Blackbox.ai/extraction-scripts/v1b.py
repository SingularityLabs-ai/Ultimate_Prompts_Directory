import re
import os

def extract_prompt_templates(filepath, output_filepath="extracted_prompts.txt", min_length=200):
    """
    Extracts potential prompt templates from a JS/TS file, attempting to filter
    out non-prompt template literals (like HTML/CSS/JS code snippets).

    Args:
        filepath (str): Path to the .js or .ts file.
        output_filepath (str): Path to save the extracted templates.
        min_length (int): Minimum character length for a template to be considered.

    Returns:
        int: Number of potential templates saved, or -1 on error.
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

    # Regex for template literals
    template_literal_regex = r'`((?:\\`|[^`])*)`'

    # Keywords strongly suggesting a prompt template
    prompt_keywords = [
        'You are BLACKBOXAI', 'TOOL USE', 'RULES', 'Parameters:', 'Usage:',
        'SYSTEM INFORMATION', 'OBJECTIVE', 'CAPABILITIES', 'MCP SERVERS',
        'current working directory', 'execute_command', 'read_file',
        'create_file', 'edit_file', 'replace_in_file', 'browser_action',
        'ask_followup_question', 'attempt_completion', 'search_code',
        'search_files', 'list_files', 'tool_name', 'parameter1_name',
        'brainstorm_plan'
        # Add more specific keywords if needed
    ]
    # Convert to lowercase for case-insensitive matching
    prompt_keywords_lower = {kw.lower() for kw in prompt_keywords}

    # Keywords/patterns strongly suggesting it's *not* a prompt (HTML/CSS/JS boilerplate)
    noise_keywords = [
        '<!DOCTYPE html>', '<html lang=', '<head>', '<body>', '<script', '<style',
        'function(', '=> {', 'class extends', 'export class', 'import {', 'require(',
        'window.addEventListener', 'document.querySelector', '.CodeMirror',
        'acquireVsCodeApi', 'const vscode =', 'module.exports', 'props', 'state',
        'React.', 'Vue.', 'angular.', 'getElementById', 'createElement',
        'padding:', 'margin:', 'color:', 'background-color:', 'font-size:',
        'display: flex', 'position: absolute', 'z-index:', 'border-radius:',
        'webpack', 'eslint', 'JSON.stringify', 'JSON.parse', 'console.log',
        '# sourceMappingURL=' # Common in minified JS
        # Add more specific noise patterns if needed
    ]
    noise_keywords_lower = {kw.lower() for kw in noise_keywords}

    # Regex to find XML-like tool tags, e.g., <tool_name>
    tool_tag_regex = re.compile(r'<\w+(_\w+)*>')

    templates_saved_count = 0
    total_literals_found = 0

    try:
        matches = re.findall(template_literal_regex, content, re.DOTALL)
        total_literals_found = len(matches)
        print(f"Found {total_literals_found} total template literals in the source.")

        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(f"--- Extracted Potential Prompt Templates from: {filepath} ---\n")
            outfile.write(f"--- (Filtered from {total_literals_found} total template literals found) ---\n\n")

            for i, match_content in enumerate(matches):
                template = match_content.strip()
                template_lower = template.lower()
                is_potential_prompt = False

                # --- Filtering Logic ---
                if len(template) < min_length:
                    continue # Too short

                # Check for strong positive indicators
                has_prompt_keyword = any(kw in template_lower for kw in prompt_keywords_lower)
                has_tool_tag = bool(tool_tag_regex.search(template))

                # Check for strong negative indicators
                has_noise_keyword = any(kw in template_lower for kw in noise_keywords_lower)
                
                # More specific noise check (e.g., looks like pure HTML)
                is_likely_html_css = template_lower.startswith(('<!doctype', '<html', '<style', 'body {', 'div {', '.','#')) and not has_prompt_keyword

                # --- Decision ---
                # Keep if it has prompt keywords or tool tags, AND is not clearly noise
                if (has_prompt_keyword or has_tool_tag) and not has_noise_keyword and not is_likely_html_css:
                    is_potential_prompt = True
                # Keep if it's very long and doesn't have strong noise indicators (might catch prompts without keywords)
                elif len(template) > 1000 and not has_noise_keyword and not is_likely_html_css:
                     is_potential_prompt = True


                if is_potential_prompt:
                    templates_saved_count += 1
                    outfile.write(f"--- Template {templates_saved_count} (Original Index: {i+1}) ---\n")
                    outfile.write(template)
                    outfile.write("\n\n--------------------\n\n")
                    # --- End Filtering Logic ---

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

    output_file = "extracted_prompts_filtered.txt" # Changed output name

    print(f"Analyzing file: {file_to_analyze}")

    count = extract_prompt_templates(file_to_analyze, output_file)

    if count > 0:
        print(f"Extraction complete. Check the file '{output_file}' for results.")
    elif count == 0:
         print(f"\nNo likely prompt templates matching the criteria found or saved to '{output_file}'.")
         print("Consider adjusting filtering keywords or min_length if prompts are missed.")
    else:
        print("Extraction failed due to an error.")