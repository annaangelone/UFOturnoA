import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):

        for i in range(1910, 2015):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))

        self._view.update_page()

    def handle_graph(self, e):
        year = int(self._view.ddyear.value)

        if year is None:
            self._view.create_alert("No year selected, please select an year")
            return

        shape = self._view.ddshape.value

        if shape is None:
            self._view.create_alert("No shape selected, please select a shape")
            return

        self._model.buildGraph(year, shape)

        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getNumNodes()} nodi e "
                                                      f"{self._model.getNumEdges()} archi"))

        vicini = self._model.stampaPesiAdiacenti()

        for (stato, peso) in vicini.items():
            self._view.txt_result.controls.append(ft.Text(f"Stato={stato}; peso archi adiacenti={peso}"))

        self._view.update_page()


    def handle_anno(self, e):
        year = int(self._view.ddyear.value)

        if year is None:
            self._view.create_alert("No year selected, please select an year")
            return

        forme = self._model.getShapes(year)

        self._view.ddshape.options.clear()
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))

        self._view.update_page()


    def handle_path(self, e):
        path, lunghezza = self._model.getPercorso()

        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {lunghezza}"))

        for i in range(len(path) - 1):
            peso = self._model.getPeso(path[i], path[i+1])
            distanza = self._model.getDistanza(path[i], path[i + 1])
            self._view.txtOut2.controls.append(ft.Text(f"{path[i]} --> {path[i+1]}; peso={peso}; distanza={distanza}"))

        self._view.update_page()
