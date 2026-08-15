import subprocess
import tempfile
import os
import re


def execute_command(command, timeout=10):

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.stdout:
            return result.stdout

        if result.stderr:
            return result.stderr

        return "Program executed successfully."

    except subprocess.TimeoutExpired:
        return "Execution timed out."


# ---------------- PYTHON ---------------- #

def run_python(code):

    with tempfile.NamedTemporaryFile(
        suffix=".py",
        delete=False,
        mode="w",
        encoding="utf-8"
    ) as f:

        f.write(code)
        filename = f.name

    try:
        return execute_command(
            ["python", filename]
        )

    finally:
        if os.path.exists(filename):
            os.remove(filename)


# ---------------- JAVASCRIPT ---------------- #

def run_javascript(code):

    with tempfile.NamedTemporaryFile(
        suffix=".js",
        delete=False,
        mode="w",
        encoding="utf-8"
    ) as f:

        f.write(code)
        filename = f.name

    try:
        return execute_command(
            ["node", filename]
        )

    finally:
        if os.path.exists(filename):
            os.remove(filename)


# ---------------- JAVA ---------------- #

def run_java(code):

    temp_dir = tempfile.mkdtemp()

    match = re.search(
        r"public\s+class\s+(\w+)",
        code
    )

    class_name = (
        match.group(1)
        if match
        else "Main"
    )

    java_file = os.path.join(
        temp_dir,
        f"{class_name}.java"
    )

    with open(
        java_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(code)

    try:

        compile_result = subprocess.run(
            ["javac", java_file],
            capture_output=True,
            text=True
        )

        if compile_result.returncode != 0:
            return compile_result.stderr

        run_result = subprocess.run(
            [
                "java",
                "-cp",
                temp_dir,
                class_name
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if run_result.stdout:
            return run_result.stdout

        if run_result.stderr:
            return run_result.stderr

        return "Program executed successfully."

    except subprocess.TimeoutExpired:
        return "Execution timed out."

    finally:

        for file in os.listdir(temp_dir):
            os.remove(
                os.path.join(temp_dir, file)
            )

        os.rmdir(temp_dir)


# ---------------- ROUTER ---------------- #

def run_code(code, language):

    language = language.lower()

    if language == "python":
        return run_python(code)

    elif language in ["javascript", "js"]:
        return run_javascript(code)

    elif language == "java":
        return run_java(code)

    return (
        f"{language.upper()} execution "
        "is not installed yet."
    )