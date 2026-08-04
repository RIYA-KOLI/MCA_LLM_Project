import subprocess
import tempfile
import os


def run_python(code):
    """
    Execute Python code locally and return stdout/stderr.
    """

    with tempfile.NamedTemporaryFile(
        suffix=".py",
        delete=False,
        mode="w",
        encoding="utf-8"
    ) as f:

        f.write(code)
        filename = f.name

    try:

        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.stdout:
            return result.stdout

        if result.stderr:
            return result.stderr

        return "Program executed successfully."

    except subprocess.TimeoutExpired:
        return "Execution timed out."

    finally:

        if os.path.exists(filename):
            os.remove(filename)


def run_code(code, language):

    language = language.lower()

    if language == "python":
        return run_python(code)

    return (
        f"{language.upper()} execution "
        "is coming soon."
    )