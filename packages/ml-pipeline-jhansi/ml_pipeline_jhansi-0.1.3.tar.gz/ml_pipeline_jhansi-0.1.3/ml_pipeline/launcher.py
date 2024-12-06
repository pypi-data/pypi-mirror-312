import os
import subprocess
import sys

def main():
    # Determine the path to the app.py file
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    print(f"Launching Streamlit app from: {app_path}")

    # Use subprocess to call the Streamlit CLI
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except FileNotFoundError:
        sys.stderr.write("Error: Streamlit is not installed or not found in PATH.\n")
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error running Streamlit app: {e}\n")

if __name__ == "__main__":
    main()