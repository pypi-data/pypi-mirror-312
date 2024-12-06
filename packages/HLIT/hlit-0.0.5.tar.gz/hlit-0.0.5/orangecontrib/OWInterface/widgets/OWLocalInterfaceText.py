import json
import os

from Orange.widgets import widget

from ..download.BaseLocalInterfaceWidget import BaseLocalInterfaceWidget


class OWLocalInterfaceText(BaseLocalInterfaceWidget):
    name = "Local Interface - Text"
    description = "Get textual data from a local interface"
    icon = "icons/local_interf_text_pull.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_text_pull.svg"
    priority=1214
    category = "Advanced Artificial Intelligence Tools"
    class Outputs:
        data = widget.Output("data", str)

    def __init__(self):
        super().__init__()
        self.Outputs.data.send("")

    def process_queue(self) -> None:
        # Standard queue processing logic
        if not self.queue_file_path.exists():
            self.info_label.setText("Queue file not found.")
            return

        try:
            with open(self.queue_file_path, 'r') as queue_file:
                content = queue_file.read().strip()
                if not content:
                    self.info_label.setText("Queue file is empty.")
                    return
                files_to_process = json.loads(content)
        except Exception as e:
            self.info_label.setText(f"Error reading queue file: {e}")

        entries_to_process = [entry for entry in files_to_process if entry.get("workflow_id") == self.workflow_id]
        assert len(entries_to_process) <= 1, "Multiple entries found for a single workflow ID."
        if entries_to_process:
            entry = entries_to_process[0]
            text_input = entry.get("text_inputs")
            if len(text_input) % 2 != 0:
                self.info_label.setText("Text input not in pairs.")
                return

            for key, value in zip(text_input[::2], text_input[1::2]):
                if key == self.input_id:
                    self.info_label.setText(f"Text input found: {value}")
                    self.Outputs.data.send(value)
                    break
            

