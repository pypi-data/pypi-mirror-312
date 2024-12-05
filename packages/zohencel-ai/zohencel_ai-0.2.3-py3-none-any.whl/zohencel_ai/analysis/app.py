import subprocess
import os


class Analysischartbot:
    """
    A class to launch a specific Streamlit app programmatically.
    """

    APP_FILENAME = "chart_bot.py"  # Hardcoded Streamlit app filename

    def __init__(self):
        """
        Initializes the launcher with the Streamlit app path.
        """
        self.app_path = os.path.join(os.path.dirname(__file__), self.APP_FILENAME)

    def _validate_app_file(self):
        """
        Validates if the Streamlit app file exists.

        Raises:
            FileNotFoundError: If the specified app file does not exist.
        """
        if not os.path.isfile(self.app_path):
            raise FileNotFoundError(f"Streamlit app file not found at: {self.app_path}")

    def run(self):
        """
        Launches the Streamlit app using `streamlit run` command.
        """
        self._validate_app_file()
        try:
            print(f"Launching Streamlit app: {self.app_path}")
            subprocess.run(["streamlit", "run", self.app_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to launch Streamlit app: {e}")

