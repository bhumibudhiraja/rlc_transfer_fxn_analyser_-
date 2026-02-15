class NetLabel(QGraphicsTextItem):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.attached_net = None
