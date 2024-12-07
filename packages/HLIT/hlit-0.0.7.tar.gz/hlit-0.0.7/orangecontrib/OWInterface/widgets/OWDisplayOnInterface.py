import os
from pathlib import Path
from AnyQt.QtWidgets import QLineEdit, QMessageBox, QCheckBox
from Orange.data.table import Table
from Orange.widgets import widget, gui
from Orange.widgets.widget import Input
from Orange.widgets.settings import Setting
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.data.io import CSVReader
import tempfile
from typing import Union
# import the orange-spectroscopy module
import json

class OWDisplayOnInterface(widget.OWWidget):
    name = "Display on local interface"
    description = "Push data to a local interface"
    icon = "icons/local_interf_push.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_push.svg"

    priority = 1220
    category = "Advanced Artificial Intelligence Tools"
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        data = Input("Data", Table)

    # Persistent setting for fileId
    output_fileId: str = Setting('untitled.csv')  # type: ignore

    # Persistent setting for the Workflow id:
    workflow_id: str = Setting('test.ows') # type: ignore


    
    def __init__(self):
        super().__init__()
        self.data = None
        self.base_folder = Path(__file__).parent.parent / "webserver" / "received_files"
        self.in_process_queue = self.base_folder / "in_process_queue.json"

        if not self.in_process_queue.exists():
            self.in_process_queue.touch(exist_ok=True)
        self.setup_ui()


    def get_output_folder(self) -> Union[str, None]:
        """Returns the output folder."""
        try:
            with open(self.in_process_queue, 'r') as f:
                in_process_queue = json.load(f)

            
            for item in in_process_queue:
                if item['workflow_id'] == self.workflow_id:
                    return item['output_folder']
                
            raise ValueError("Workflow ID provided does not exist in the queue.")
        
        except json.decoder.JSONDecodeError:
            print("No items in the queue.")

        except ValueError:
            QMessageBox.critical(self, "UploadWidget Error", "Workflow ID provided does not match the workflow id of inputs.")
            


    def setup_ui(self):
        # Create a horizontal box layout for the text input
        hbox = gui.hBox(self.controlArea, "name")
        hbox2 = gui.hBox(self.controlArea, "Workflow ID")
        
        # Text input for fileId
        self.le_fileId = QLineEdit(self)
        self.le_fileId.setText(self.output_fileId)
        self.le_fileId.editingFinished.connect(self.update_fileId)
        hbox.layout().addWidget(self.le_fileId)

        # Text input for Workflow ID
        self.le_workflow_id = QLineEdit(self)
        self.le_workflow_id.setText(self.workflow_id)
        self.le_workflow_id.editingFinished.connect(self.update_workflow_id)
        hbox2.layout().addWidget(self.le_workflow_id)
        
        self.adjustSize()

    @Inputs.data
    def dataset(self, data):
        self.data = data
        if self.data is not None:
            self.save_to_file()

    def update_fileId(self):
        self.output_fileId = self.ensure_csv_extension(self.le_fileId.text())
    
    def update_workflow_id(self):   
        self.workflow_id = self.le_workflow_id.text()


    def save_to_file(self):
        if self.data is None:
            QMessageBox.warning(self, "No Data", "No data available to save.")
            return
        # Compute full output path
        output_folder = self.get_output_folder()

        if output_folder is None:
            QMessageBox.warning(self, "No file to upload.", "The queue doesn't contains any item with the provided Workflow ID.")
            return
        file_path = Path(output_folder) / self.output_fileId
        
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                CSVReader.write(temp.name, self.data)
            os.replace(temp.name, file_path)
            print("Data successfully saved to: ", file_path)
        except IOError as err:
            QMessageBox.critical(self, "Error", f"Failed to save file: {err}")

    @staticmethod
    def ensure_csv_extension(fileId):
        return fileId if fileId.endswith('.csv') else fileId + '.csv'

if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWDisplayOnInterface).run(Table("iris"))
