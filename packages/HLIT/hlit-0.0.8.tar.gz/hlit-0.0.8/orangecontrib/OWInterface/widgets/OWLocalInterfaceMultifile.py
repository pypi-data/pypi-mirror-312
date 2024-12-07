import os
from itertools import chain, repeat
from pathlib import Path
from typing import Union

import numpy as np
from Orange.data import Domain, StringVariable, Table
from Orange.widgets import widget

from ..download.BaseLocalInterfaceWidget import BaseLocalInterfaceWidget


class OWLocalInterfaceMultifile(BaseLocalInterfaceWidget):
    name = "Local Interface - Multifile"
    description = "Get multiple data file (csv, xlsx, pkl...) from a local interface"
    icon = "icons/local_interf_multi_pull.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_multi_pull.svg"
    priority = 1213
    category = "Advanced Artificial Intelligence Tools"
    class Outputs:
        data = widget.Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.opening_method = "multiple_file"

    def process_files(self, files_to_process: list[Path]):
        data = self.concatenate_data_with_origin(files_to_process)
        self.Outputs.data.send(data)

    def concatenate_data_with_origin(self, filepaths: list[Path])->Union[Table,None]:
        if not filepaths:
            return None
        
        filenames = [filepath.name for filepath in filepaths]
        tables = [Table.from_file(str(x)) for x in filepaths]

        # Determine the merged domain, accounting for all attributes and metas in all tables
        domain = self._merge_domains([table.domain for table in tables])
        source_var = StringVariable("File Source")
        domain = Domain(domain.attributes, domain.class_vars, domain.metas + (source_var,))

        # Transform tables to the new domain so they can be concatenated
        tables = [table.transform(domain) for table in tables]
        data = Table.concatenate(tables)

        with data.unlocked():
            # Flatten the array to the correct shape
            data.metas[:, -1] = np.array(list(
                chain(*(repeat(fn, len(table))
                        for fn, table in zip(filenames, tables)))
            ))

        return data

    def _merge_domains(self, domains):
        # This assumes all tables have compatible domains; more complex logic can be implemented if needed
        return domains[0] if domains else Domain([])

if __name__ == "__main__":
    # This would normally start the GUI application
    pass
