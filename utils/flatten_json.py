import os
import json

# Define input and output directories
FLATTEN_INPUT_DIR = os.path.join(r"F:\vscode main\goodbug\data\raw\scraped_data")  # Directory containing scraped JSON files
FLATTEN_OUTPUT_DIR = os.path.join(r"F:\vscode main\goodbug\data\processed")       # Directory to store flattened JSON files

# Ensure the output directory exists
os.makedirs(FLATTEN_OUTPUT_DIR, exist_ok=True)

def transform_to_instruction_response(data):
    """
    Transforms structured JSON data into an instruction-response format.
    
    Args:
        data (list): List of sections from the structured JSON file.
    
    Returns:
        list: Transformed data with "instruction" and "response" keys.
    """
    transformed_data = []

    for section in data:
        heading = section.get("heading", "").strip()
        text_parts = []

        for item in section.get("content", []):
            if item.get("type") == "paragraph":
                text = item.get("text", "").strip()
                if text:
                    text_parts.append(text)

        # Combine all text parts into a single response string
        combined_text = " ".join(text_parts).strip()

        # Skip sections with missing or empty heading/response
        if not heading or not combined_text:
            continue

        transformed_data.append({
            "instruction": heading,
            "response": combined_text
        })

    return transformed_data

def merge_all_json_files(input_dir, output_dir):
    """
    Processes all JSON files in the input directory, transforms them into instruction-response format,
    and merges them into a single JSON file.
    
    Args:
        input_dir (str): Directory containing the input JSON files.
        output_dir (str): Directory to store the merged JSON file.
    """
    merged_data = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            print(f"Processing file: {filepath}")

            try:
                # Load the structured JSON file
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Transform the JSON data into instruction-response format
                transformed_data = transform_to_instruction_response(data)

                # Append the transformed data to the merged list
                merged_data.extend(transformed_data)

            except json.JSONDecodeError:
                print(f"Invalid JSON in file {filename}. Skipping.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    # Save the merged JSON data
    output_file = os.path.join(output_dir, "merged_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

    print(f"Merged data saved to: {output_file}")

# Merge all JSON files in the input directory
merge_all_json_files(FLATTEN_INPUT_DIR, FLATTEN_OUTPUT_DIR)