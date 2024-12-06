import os
from pathlib import Path
from appdirs import user_cache_dir, user_config_dir
from dotenv import load_dotenv
from PIL import Image

from qtpy.QtWidgets import (
    QPushButton,
    QWidget,
    QCheckBox,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
    QMessageBox,
)
from atproto import Client

# Load credentials from environment variables
load_dotenv(Path(user_config_dir("napari-bluesky", "kephale")) / ".env")


class BlueskyWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.client = None

        # Textbox for entering prompt
        self.post_textbox = QPlainTextEdit(self)
        self.post_textbox.appendPlainText(
            "Posted from #napari with #napariBluesky."
        )

        self.screenshot_checkbox = QCheckBox(self)

        btn = QPushButton("Post to Bluesky")
        btn.clicked.connect(self._on_click)

        help_btn = QPushButton("How to Set Up Credentials")
        help_btn.clicked.connect(self._show_help)

        # Layout and labels
        self.setLayout(QVBoxLayout())

        label = QLabel(self)
        label.setText("Message")
        self.layout().addWidget(label)
        self.layout().addWidget(self.post_textbox)

        label = QLabel(self)
        label.setText("Screenshot with UI")
        self.layout().addWidget(label)
        self.layout().addWidget(self.screenshot_checkbox)

        self.layout().addWidget(btn)
        self.layout().addWidget(help_btn)

        self.login_bluesky()

    def login_bluesky(self):
        if self.client:
            return self.client
        handle = os.getenv("BLUESKY_HANDLE")
        password = os.getenv("BLUESKY_PASSWORD")

        if not handle or not password:
            QMessageBox.critical(
                self,
                "Missing Credentials",
                "Bluesky credentials are not set up. Please configure them first.",
            )
            return None

        self.client = Client()
        self.client.login(handle, password)
        return self.client

    def _on_click(self):
        self.post_to_bluesky()

    def post_to_bluesky(self):
        if not self.login_bluesky():
            print("Cannot login to Bluesky")
            return

        os.makedirs(user_cache_dir("napari-bluesky", "kephale"), exist_ok=True)

        screenshot_path = (
            Path(user_cache_dir("napari-bluesky", "kephale"))
            / "napari_bluesky_screenshot.png"
        )

        canvas_only = (not self.get_screenshot_with_ui())

        self.viewer.screenshot(
            screenshot_path, canvas_only=canvas_only
        )

        text = self.post_textbox.document().toPlainText()

        # Resize the image to be under the max size limit
        max_file_size = 976 * 1024  # 976.56 KB in bytes
        resized_path = screenshot_path.with_name("resized_screenshot.png")

        with Image.open(screenshot_path) as img:
            while True:
                # Calculate the current file size
                img.save(resized_path, format="PNG", optimize=True)
                if resized_path.stat().st_size < max_file_size:
                    break  # Stop resizing if the file size is under the limit
                
                # Resize by reducing dimensions
                new_width = int(img.width * 0.9)  # Reduce dimensions by 10%
                new_height = int(img.height * 0.9)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Load the resized image
        with open(resized_path, "rb") as f:
            image_data = f.read()

        alt_text = f"A screenshot automatically generated with napari-bluesky. Is the napari UI showing? {not canvas_only}. The corresponding post is: {text}."

        # Post to Bluesky
        self.client.send_image(text=text, image=image_data, image_alt=alt_text)

    def get_screenshot_with_ui(self):
        return self.screenshot_checkbox.checkState()

    def _show_help(self):
        # Display instructions for setting up credentials
        help_message = (
            "To configure your Bluesky credentials:\n\n"
            "1. Open the configuration directory:\n"
            f"   {Path(user_config_dir('napari-bluesky', 'kephale'))}\n\n"
            "2. Create a file named `.env` in that directory.\n"
            "3. Add the following lines to the file:\n\n"
            "   BLUESKY_HANDLE=your-handle\n"
            "   BLUESKY_PASSWORD=your-password\n\n"
            "4. Restart Napari and try again."
        )
        QMessageBox.information(self, "How to Set Up Credentials", help_message)


if __name__ == "__main__":
    import napari

    viewer = napari.Viewer()
    viewer.window.resize(800, 600)

    widget = BlueskyWidget(viewer)

    viewer.window.add_dock_widget(widget, name="napari-bluesky")

    print(Path(user_config_dir('napari-bluesky', 'kephale')) / ".env")

    napari.run()