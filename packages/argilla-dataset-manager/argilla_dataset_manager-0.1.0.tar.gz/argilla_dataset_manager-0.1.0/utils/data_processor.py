import re
import json
import pandas as pd

def extract_json_objects(text):
    """
    Extract JSON objects from text.

    Args:
        text (str): Text containing JSON objects.

    Returns:
        list: List of JSON objects.
    """
    try:
        json_matches = re.finditer(r'\{.*?\}(?=\s|$)', text, re.DOTALL)
        json_objects = []

        for match in json_matches:
            try:
                json_obj = json.loads(match.group())
                if json_obj.get("prompt") == "How can we improve our documentation based on the questions and answers we have?":
                    continue
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                continue

        return json_objects if json_objects else None
    except Exception:
        return None

def process_dataframe(df):
    """
    Process DataFrame to extract and expand JSON data.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df['parsed_json'] = df['result_value'].apply(extract_json_objects)
    df = df[df['parsed_json'].notna()]

    # Flatten parsed_json and expand fields
    records = []
    for _, row in df.iterrows():
        for json_obj in row['parsed_json']:
            record = row.to_dict()
            record.update(json_obj)
            records.append(record)

    processed_df = pd.DataFrame(records)
    return processed_df