class relationship:

    OGMRelationship = '''<<PACKAGE>>
    

    '''

    def __init__(self, startNode, endNode, type) -> None:
        self.startNode = startNode
        self.endNode = endNode
        self.type = type