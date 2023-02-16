import os

class relationship:

    OGMRelationship = '''<<PACKAGE>>
    <<IMPORTS>>
    
    <<PROPERTIES>>

    @StartNode
    <<STARTNODE>>

    @EndNode
    <<ENDNODE>>
    '''

    def __init__(self, startNode:str, endNode:str, type:str, properties:dict, imports:list) -> None:
        self.startNode = startNode
        self.endNode = endNode
        self.type = type
        self.properties = properties
        self.imports = imports

        self.OGMRelationship = relationship.OGMRelationship

    def save(self, location:str) -> None:

        self.OGMRelationship = self.OGMRelationship.replace('<<IMPORTS>>', str('\n'.join(self.imports)))
        self.OGMRelationship = self.OGMRelationship.replace('<<STARTNODE>>', 'private ' + self.startNode + ' ' + self.startNode + ';')
        self.OGMRelationship = self.OGMRelationship.replace('<<ENDNODE>>', 'private ' + self.endNode + ' ' + self.endNode + ';')

        properties = ''''''
        hasId = False
        for property in self.properties:
            if(len(property.split(':')) > 1 and property.split(':')[1].lower() == 'id'):
                properties += '@Id\nprivate ' + self.properties[property] + ' ' + property.split(':')[0] + ';\n'
                hasId = True
            else:
                properties += 'private ' + self.properties[property] + ' ' + property + ';\n'

        if(hasId == False):
            properties += '\n@Id\n\@GeneratedValue\nprivate Long Id;'

        # save to the path
        path = ''
        for _location in location.split('/'):
            path += _location + '/'
            if(os.path.exists(path) == False):
                os.mkdir(path)

        with open(path + self.startNode + '_' + self.endNode + '.java', "w") as file:
            file.write(self.OGMRelationship)