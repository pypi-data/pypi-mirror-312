import os
import sys

from AnyQt.QtWidgets import QApplication, QLabel
from Orange.widgets import widget
from Orange.widgets.utils.signals import Output
import spacy


if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from orangecontrib.AAIT.utils import SimpleDialogQt, thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import GetFromRemote, get_local_store_path
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.utils import SimpleDialogQt, thread_management
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.MetManagement import GetFromRemote, get_local_store_path
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file


class OWModelSpacyMDFR(widget.OWWidget):
    name = "Model - SpacyMD-FR"
    description = "Load the model SpacyMD-FR from the AAIT Store"
    icon = "icons/owmodel_spacymd_fr.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/owmodel_spacymd_fr.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owmodel_spacymd_fr.ui")
    priority=1072
    want_control_area = False

    class Outputs:
        model_path = Output("Model", str)

    def __init__(self):
        super().__init__()
        # Path management
        self.current_ows = ""
        local_store_path = get_local_store_path()
        model_name = os.path.join("fr_core_news_md", "fr_core_news_md-3.7.0")
        self.model_path = os.path.join(local_store_path, "Models", "NLP", model_name)

        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)

        if not os.path.exists(self.model_path):
            self.error(f"{model_name} could not be found in your AI store")
        else:
            self.Outputs.model_path.send(self.model_path)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWModelMPNET()
    my_widget.show()
    app.exec_()
