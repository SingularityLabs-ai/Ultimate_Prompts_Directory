import re
import os

def is_likely_code_or_markup(text, text_lower):
    """
    Heuristically checks if a string is more likely code, HTML, or CSS
    than a natural language prompt.
    """
    # 1. Check for common code keywords/patterns (increase sensitivity)
    code_keywords = [
        'function(', '=> {', 'class ', 'constructor(', ' Symbol(', '.prototype',
        'addEventListener', 'querySelector', 'getElementById', 'createElement',
        'Object.assign', 'Object.defineProperty', 'Promise.resolve', 'Promise.reject',
        'async (', 'await ', 'require(', 'import {', 'export default', 'module.exports',
        'console.log', 'console.error', 'try {', '} catch (', ' for (', ' while (',
        'arguments.length', 'this.', '.call(null', '.bind(this', '.map(', '.filter(', '.reduce(',
        '.forEach(', '.test(', '.exec(', '.match(', '.replace(', '.split(', '.join(',
        'JSON.stringify', 'JSON.parse', 'new Error(', 'throw new ', '# sourceMappingURL=',
        'static {' # Added from example
    ]
    if any(kw in text_lower for kw in code_keywords):
        # Check ratio if a keyword is found, maybe it's just mentioned in a prompt
        code_symbols = len(re.findall(r'[{}()\[\];=.,+\-*/&|!<>?:%]', text))
        words = len(re.findall(r'\b\w+\b', text))
        if words == 0 or code_symbols / (code_symbols + words) > 0.25: # High ratio of symbols
             return True
        # Low ratio might still be a prompt mentioning a keyword

    # 2. Check for common HTML/CSS patterns
    html_css_keywords = [
        '<!DOCTYPE html>', '<html', '<head>', '<body', '<script', '<style',
        'padding:', 'margin:', 'color:', 'background-color:', 'font-size:',
        'display: flex', 'position: absolute', 'z-index:', 'border-radius:',
        '.CodeMirror', 'w-button', 'w-form' # From examples
    ]
    if any(kw in text_lower for kw in html_css_keywords):
        return True # Pretty likely not a prompt

    # Check for high density of HTML tags
    html_tags = len(re.findall(r'<[/!]?\s*\w+', text))
    if html_tags > 5 and html_tags / len(text.split()) > 0.1: # More than 1 tag per 10 words
        return True

    # Check for high density of CSS rules
    css_rules = len(re.findall(r'[{};:]', text))
    if css_rules > 10 and css_rules / len(text) > 0.05: # High density of CSS characters
         # Check if it *also* lacks prompt keywords to be more sure
         prompt_keywords_check = ['tool use', 'rules', 'parameters', 'usage', 'objective', '<tool_name>']
         if not any(pk in text_lower for pk in prompt_keywords_check):
             return True

    # Check for the HTML entity list pattern (like Template 4)
    html_entities = len(re.findall(r'&[#a-zA-Z0-9]+;', text))
    if html_entities > 20 and html_entities / len(text) > 0.02: # High density of entities
        return True

    return False

def extract_prompt_templates(filepath, output_filepath="extracted_prompts_filtered_v2.txt", min_length=150):
    """
    Extracts potential prompt templates, attempting to strongly filter out non-prompts.
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

    template_literal_regex = r'`((?:\\`|[^`])*)`'

    # Increased specificity for prompt keywords/structures
    strong_prompt_keywords = [
        'You are BLACKBOXAI', '====\nTOOL USE\n====', '====\nRULES\n====',
        '====\nSYSTEM INFORMATION\n====', '====\nOBJECTIVE\n====',
        '<execute_command>', '<read_file>', '<create_file>', '<edit_file>',
        '<replace_in_file>', '<ask_followup_question>', '<attempt_completion>',
        'brainstorm_plan' # Added from example
    ]
    other_prompt_keywords = [
        'Parameters:', 'Usage:', 'Description:', 'current working directory',
        'search_code', 'search_files', 'list_files', 'browser_action',
        'tool_name', 'parameter1_name', 'MCP SERVERS', 'CAPABILITIES'
    ]
    strong_prompt_keywords_lower = {kw.lower() for kw in strong_prompt_keywords}
    other_prompt_keywords_lower = {kw.lower() for kw in other_prompt_keywords}

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
                    continue

                # Check for strong positive indicators
                has_strong_prompt_keyword = any(kw in template_lower for kw in strong_prompt_keywords_lower)
                has_other_prompt_keywords_count = sum(1 for kw in other_prompt_keywords_lower if kw in template_lower)

                # Check for strong negative indicators (more aggressively)
                if is_likely_code_or_markup(template, template_lower):
                    continue # Skip if it looks like code/markup

                # --- Decision ---
                # Require at least one strong keyword OR multiple (e.g., 3+) other keywords
                if has_strong_prompt_keyword or has_other_prompt_keywords_count >= 3:
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
    file_to_analyze = "extension.js"
    output_file = "extracted_prompts_filtered_v2.txt" # New output name

    print(f"Analyzing file: {file_to_analyze}")
    count = extract_prompt_templates(file_to_analyze, output_file)

    if count > 0:
        print(f"Extraction complete. Check the file '{output_file}' for results.")
    elif count == 0:
         print(f"\nNo likely prompt templates matching the more stringent criteria found or saved to '{output_file}'.")
         print("Consider adjusting filtering keywords or min_length if prompts are missed.")
    else:
        print("Extraction failed due to an error.")