import subprocess
import sys
import os


def set_pythonpath_to_root():

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    os.environ["PYTHONPATH"] = project_root


def run_streamlit_app():
    set_pythonpath_to_root()
    subprocess.run(["streamlit", "run", "./src/ui/app.py"])


if __name__ == "__main__":
    run_streamlit_app()
