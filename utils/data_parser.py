import base64
import io
import pandas as pd


def parse_uploaded_file(contents, filename):
    """
    Parse uploaded file and convert it to a DataFrame.

    Args:
        contents (str): File contents encoded in base64.
        filename (str): File name (for type determination).

    Returns:
        pd.DataFrame: Parsed DataFrame with `timestamp` and `value`.
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    else:
        raise ValueError("Unsupported file format")

    # Ensure required columns are present
    if 'timestamp' not in df or 'value' not in df:
        raise ValueError("File must contain 'timestamp' and 'value' columns")
    
    return df