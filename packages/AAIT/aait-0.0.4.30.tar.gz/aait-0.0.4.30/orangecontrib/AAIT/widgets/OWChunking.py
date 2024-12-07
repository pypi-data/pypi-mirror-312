import os
import sys

import Orange.data
from AnyQt.QtWidgets import QApplication
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
import numpy as np
from Orange.data import Table
from chonkie import SemanticChunker

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import  get_local_store_path
else:
    from orangecontrib.AAIT.utils import thread_management
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.MetManagement import GetFromRemote, get_local_store_path



    # """
    # Splits a given text into segments of a specified maximum length.
    #
    # This function takes a text and divides it into segments, where each segment
    # does not exceed the specified maximum number of words (`chunk_size`).
    # Sentences are split by periods and are not fragmented across segments.
    #
    # :param text:
    #      The text to be segmented.
    # :param chunk_size:
    #      The maximum number of words allowed per segment. Default is 400.
    #
    # :return:
    #     List[str]: A list of text segments.
    # """
    #
    # chunks = []
    # current_chunk = []
    # current_length = 0
    # sentences = text.split('.')
    #
    # for sentence in sentences:
    #     sentence = sentence.strip()
    #     if not sentence:
    #         continue
    #     sentence_length = len(sentence.split())
    #
    #     if current_length + sentence_length <= chunk_size:
    #         current_chunk.append(sentence)
    #         current_length += sentence_length
    #     else:
    #         chunks.append('. '.join(current_chunk) + '.')
    #         current_chunk = [sentence]
    #         current_length = sentence_length
    #
    # if current_chunk:
    #     chunks.append('. '.join(current_chunk) + '.')
    #
    # return chunks


class OWChunker(widget.OWWidget):
    name = "Text Chunker"
    description = "Chunk text into segments of approximately 400 words, stopping at sentence boundaries."
    icon = "icons/owchunking.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/owchunking.png"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owchunking.ui")
    want_control_area = False
    priority = 1050

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        data = Output("Chunked Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        if self.autorun:
            self.run()

    def __init__(self):
        super().__init__()
        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)

        # Data Management
        self.data = None
        self.thread = None
        self.autorun = True
        self.post_initialized()

    def chunk_text(text, chunk_size=400):

        # Basic initialization with default parameters
        local_store_path = get_local_store_path()
        model_name = "all-mpnet-base-v2"
        model = os.path.join(local_store_path, "Models", "NLP", model_name)
        model = "C:/Users/timot/aait_store/Models/NLP/all-mpnet-base-v2"
        chunker = SemanticChunker(
            #embedding_model=model,  # Default model
            similarity_threshold=0.4,  # Similarity threshold (0-1)
            chunk_size=512,  # Maximum tokens per chunk
            initial_sentences=2  # Initial sentences per chunk
        )

        # text = r"L'importance de l'alimentation équilibrée Une alimentation équilibrée est essentielle pour maintenir une bonne santé. Elle fournit les nutriments nécessaires au bon fonctionnement de l'organisme et aide à prévenir diverses maladies. Les fruits et légumes, riches en vitamines et minéraux, devraient constituer une part importante de notre régime alimentaire. De plus, il est recommandé de consommer des protéines maigres, des glucides complexes et des graisses saines pour assurer un apport nutritionnel complet. Les bienfaits de l'exercice physique régulier Pratiquer une activité physique régulière présente de nombreux avantages pour la santé physique et mentale. L'exercice aide à contrôler le poids, renforce le système cardiovasculaire et améliore la flexibilité et la force musculaire. De plus, il contribue à réduire le stress, l'anxiété et les symptômes de la dépression, tout en améliorant la qualité du sommeil. Il est recommandé de pratiquer au moins 150 minutes d'activité modérée par semaine. L'impact de la technologie sur la communication Avec l'avènement des smartphones et des réseaux sociaux, la manière dont nous communiquons a radicalement changé. Les messages instantanés et les appels vidéo permettent de rester en contact avec des personnes à travers le monde en temps réel. Cependant, cette hyperconnectivité peut également entraîner une diminution des interactions en face à face et affecter la qualité des relations humaines. Il est donc important de trouver un équilibre entre l'utilisation de la technologie et les interactions personnelles. La préservation de l'environnement La protection de l'environnement est devenue une priorité mondiale. Les activités humaines, telles que la déforestation, la pollution et la surconsommation des ressources naturelles, ont conduit à des changements climatiques significatifs. Pour préserver notre planète, il est essentiel d'adopter des pratiques durables, comme le recyclage, la réduction de l'utilisation des plastiques et la promotion des énergies renouvelables. Chacun peut contribuer à la protection de l'environnement par des actions quotidiennes simples. L'importance de l'éducation financière Comprendre les principes de base de la gestion financière est crucial pour assurer une stabilité économique personnelle. L'éducation financière permet aux individus de prendre des décisions éclairées concernant l'épargne, l'investissement et la gestion des dettes. Elle aide également à planifier l'avenir, en préparant des budgets et en fixant des objectifs financiers à long terme. Une bonne éducation financière peut prévenir les difficultés économiques et améliorer la qualité de vie."
        chunks = chunker.chunk(text)
        chunks1 = []
        for chunk in chunks:
            chunks1.append(chunk.text)
            print("Chunks produits ---->", chunk.text, "\n\n\n")
        return chunks1
    def run(self):
        # if thread is running quit
        """
        Main function of the widget. It segments the text into chunks of approximately
        400 words, stopping at sentence boundaries.

        If a thread is already running, it will be terminated.

        The function will also check if the input data contains a column named "content"
        and if it is a text variable. If not, an error message will be displayed.

        The function will then start a progress bar and a new thread with the
        chunk_data function. The thread will be connected to the progress bar,
        as well as to the result and finish signals.

        :return: None
        """

        if self.thread is not None:
            self.thread.safe_quit()

        if self.data is None:
            return

        # Verification of in_data
        self.error("")
        if not "content" in self.data.domain:
            self.error('You need a "content" column in input data')
            return

        if type(self.data.domain["content"]).__name__ != 'StringVariable':
            self.error('"content" column needs to be a Text')
            return

        # Start progress bar
        self.progressBarInit()

        # Connect and start thread
        self.thread = thread_management.Thread(self.chunk_data, self.data)
        self.thread.progress.connect(self.handle_progress)
        self.thread.result.connect(self.handle_result)
        self.thread.finish.connect(self.handle_finish)
        self.thread.start()

    def chunk_data(self, data):
        """
        Takes a Table, segments the content of each instance into chunks of approximately
        400 words, stopping at sentence boundaries, and returns a new Table with the new instances.

        :param data: The input Table.
        :return: A new Table with the segmented instances.
        """

        new_instances = []
        domain = data.domain

        # Créer un nouveau domaine avec une colonne "Chunks"
        new_metas = list(domain.metas) + [Orange.data.StringVariable("Chunks")]
        new_domain = Orange.data.Domain(domain.attributes, domain.class_vars, new_metas)

        for instance in data:
            content = instance["content"].value  # Vérifie que "content" existe bien
            chunks = self.chunk_text(content)  # Découpe le texte en segments

            for chunk in chunks:
                # Construire une nouvelle instance avec le segment
                new_metas_values = list(instance.metas) + [chunk]
                new_instance = Orange.data.Instance(new_domain, [instance[x] for x in domain.attributes] + [instance[y] for y in domain.class_vars] + new_metas_values)
                new_instances.append(new_instance)

        # Retourner une nouvelle table avec toutes les instances générées
        return Orange.data.Table.from_list(new_domain, new_instances)

    def handle_progress(self, value: float) -> None:
        """
        Handles the progress signal from the main function.

        Updates the progress bar with the given value.

        :param value: (float): The value to set for the progress bar.

        :return: None
        """

        self.progressBarSet(value)

    def handle_result(self, result):
        """
        Handles the result signal from the main function.

        Attempts to send the result to the data output port. In case of an error,
        sends None to the data output port and displays the error message.

        :param result:
             Any: The result from the main function.

        :return:
            None
        """

        try:
            self.Outputs.data.send(result)
        except Exception as e:
            print("An error occurred when sending out_data:", e)
            self.Outputs.data.send(None)
            return
    def handle_finish(self):
        """
        Handles the end signal from the main function.

        Displays a message indicating that the segmentation is complete and updates
        the progress bar to reflect the completion.

        :return:
            None
        """
        print("Chunking finished")
        self.progressBarFinished()

    def post_initialized(self):
        """
        This method is intended for post-initialization tasks after the widget has
        been fully initialized.

        Override this method in subclasses to perform additional configurations
        or settings that require the widget to be fully constructed. This can
        include tasks such as connecting signals, initializing data, or setting
        properties of the widget dependent on its final state.

        :return:
            None
        """
        pass

if __name__ == "__main__":

    #print(chunks1)

    # Advanced initialization with custom parameters
    from orangewidget.utils.widgetpreview import WidgetPreview
    from orangecontrib.text.corpus import Corpus
    from orangecontrib.text.preprocess import BASE_TOKENIZER

    #corpus_ = Corpus.from_file(r"C:\Users\timot\Downloads\contes_de_Perrault\Documents.tab")
    corpus_ = Corpus.from_file("book-excerpts")
    #corpus_ = corpus_[:3]
    #corpus_ = BASE_TOKENIZER(corpus_)
    WidgetPreview(OWChunker).run(corpus_)