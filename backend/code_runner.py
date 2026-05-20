import subprocess
import os

def run_code(language, filename):

    try:

        if language == "python":
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True
            )

        elif language == "javascript":
            result = subprocess.run(
                ["node", filename],
                capture_output=True,
                text=True
            )

        elif language == "c":
            subprocess.run(["gcc", filename, "-o", "temp"])
            result = subprocess.run(
                ["./temp"],
                capture_output=True,
                text=True
            )

        elif language == "cpp":
            subprocess.run(["g++", filename, "-o", "temp"])
            result = subprocess.run(
                ["./temp"],
                capture_output=True,
                text=True
            )

        elif language == "java":
            subprocess.run(["javac", filename])
            classname = os.path.splitext(filename)[0]
            result = subprocess.run(
                ["java", classname],
                capture_output=True,
                text=True
            )

        else:
            return "Language not supported"

        return result.stdout + result.stderr

    except Exception as e:
        return str(e)