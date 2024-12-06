import os
import sys

import Orange.data
from AnyQt.QtWidgets import QApplication
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
import numpy as np
from Orange.data import Table

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
else:
    from orangecontrib.AAIT.utils import thread_management
    from orangecontrib.AAIT.utils.import_uic import uic


def chunk_text(text, chunk_size=400):
    """
    Divise un texte donné en segments d’une longueur maximale spécifiée.

    Cette fonction prend un texte et le divise en segments, où chaque segment
    ne dépasse pas le nombre maximal de mots spécifié (`chunk_size`).
    Les phrases sont découpées par des points et ne sont pas fragmentées entre
    les segments.

    :param text:
         Le texte à segmenter.
    :param chunk_size:
         Le nombre maximal de mots autorisé par segment. Par défaut, 400.

    :return:
        List[str] : Une liste de segments de texte.
    """

    chunks = []
    current_chunk = []
    current_length = 0
    sentences = text.split('.')

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        sentence_length = len(sentence.split())

        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks


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

    def run(self):
        # if thread is running quit
        """
        Fonction principale du widget. Elle segmentera le texte en morceaux d’environ
        400 mots, en s’arrêtant aux limites des phrases.

        Si un thread est déjà en cours d’exécution, il sera interrompu.

        Elle vérifiera également si les données d’entrée contiennent une colonne
        nommée "content" et si celle-ci est une variable texte. Si ce n’est pas le cas,
        un message d’erreur sera affiché.

        La fonction lancera ensuite une barre de progression et un nouveau thread avec
        la fonction chunk_data. Le thread sera connecté à la barre de progression,
        ainsi qu’aux signaux de résultat et de fin.

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
        Prend une Table, segmente le contenu de chaque instance en morceaux d’environ
        400 mots en s’arrêtant aux limites des phrases, et retourne une nouvelle Table
        avec les nouvelles instances.

        :param data: La Table d’entrée.
        :return: Une nouvelle Table avec les nouvelles instances.
        """
        new_instances = []
        domain = data.domain

        # Créer un nouveau domaine avec une colonne "Chunks"
        new_metas = list(domain.metas) + [Orange.data.StringVariable("Chunks")]
        new_domain = Orange.data.Domain(domain.attributes, domain.class_vars, new_metas)

        for instance in data:
            content = instance["content"].value  # Vérifie que "content" existe bien
            chunks = chunk_text(content)  # Découpe le texte en segments

            for chunk in chunks:
                # Construire une nouvelle instance avec le segment
                new_metas_values = list(instance.metas) + [chunk]
                new_instance = Orange.data.Instance(new_domain, [instance[x] for x in domain.attributes] + [instance[y] for y in domain.class_vars] + new_metas_values)
                new_instances.append(new_instance)

        # Retourner une nouvelle table avec toutes les instances générées
        return Orange.data.Table(new_domain, new_instances)

    def handle_progress(self, value: float) -> None:
        """
        Gère le signal de progression provenant de la fonction principale.

        Met à jour la barre de progression avec la valeur donnée.

        :param value: (float) : La valeur à attribuer à la barre de progression.

        :return: None

        """
        self.progressBarSet(value)

    def handle_result(self, result):
        """
        Gère le signal de résultat provenant de la fonction principale.

        Tente d’envoyer le résultat au port de sortie des données. En cas d’erreur,
        envoie None au port de sortie des données et affiche le message d’erreur.

        :param result:
             Any : Le résultat de la fonction principale.

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
        Gère le signal de fin provenant de la fonction principale.

        Affiche un message indiquant que le découpage est terminé et met à jour
        la barre de progression pour indiquer la fin.

        :return:
            None
        """
        print("Chunking finished")
        self.progressBarFinished()

    def post_initialized(self):
        """
        Cette méthode est destinée aux tâches d’initialisation après que le widget
        a été entièrement initialisé.

        Surcharger cette méthode dans les sous-classes pour effectuer des configurations
        ou des paramétrages supplémentaires nécessitant que le widget soit complètement
        construit. Cela peut inclure des tâches telles que la connexion de signaux,
        l’initialisation de données ou la définition de propriétés du widget dépendant
        de son état final.

        :return:
            None
        """
        pass

if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    from orangecontrib.text.corpus import Corpus

    from orangecontrib.text.preprocess import BASE_TOKENIZER

    #corpus_ = Corpus.from_file(r"C:\Users\timot\Downloads\contes_de_Perrault\Documents.tab")
    corpus_ = Corpus.from_file("book-excerpts")
    #corpus_ = corpus_[:3]
    #corpus_ = BASE_TOKENIZER(corpus_)
    WidgetPreview(OWChunker).run(corpus_)