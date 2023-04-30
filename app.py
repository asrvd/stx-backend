from flask import Flask, request
import mindsdb_sdk as mdb
import urllib.parse
import dotenv

app = Flask(__name__)

dotenv.load_dotenv()

EMAIL = dotenv.get_key(".env", "EMAIL")
PASSWORD = dotenv.get_key(".env", "PSWD")


def get_explanation(code: str) -> str:
    """Get explanation for a given code

    Args:
        code (str): code to get explanation for

    Returns:
        str: explanation for the given code
    """
    server = mdb.connect(login=EMAIL, password=PASSWORD)
    project = server.get_project("mindsdb")

    # replace double quotes with single quotes

    code = code.replace('"', "'")

    # // escape single quotes and double quotes and semicolons from code by adding \ before them

    escapedCode = code.replace("'", "\\'").replace('"', '\\"').replace(";", "\\;")

    q = project.query(
        f"""
        SELECT article, highlights
        FROM cex
        WHERE article = "{escapedCode}"
        USING max_tokens = 1000;
    """
    )

    df = q.fetch()
    result = df.iloc[0]["highlights"]
    print(result)
    return result


@app.route("/")
def explainer():
    print(EMAIL, PASSWORD)
    code = request.args.get("code")
    if code:
        decoded_code = urllib.parse.unquote(code)
        return get_explanation(decoded_code)

    return "No code provided"


if __name__ == "__main__":
    app.run(debug=True)
