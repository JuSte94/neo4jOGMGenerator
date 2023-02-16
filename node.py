import os
import relationship as OGMRelationship

class node:
    OGMNode = '''<<PACKAGE>>
    <<IMPORTS>>
    <<ACCESS>> <<ABSTRACT>> class <<CLASSNAME>> <<EXTENDS>> {
        <<PROPERTIES>>

        <<RELATIONSHIPS>>
    }
    '''

    def __init__(self, nodeName, EXPORT) -> None:
        self.nodeName = nodeName
        self.abstract = False
        self.imports = []
        self.lables = []
        self.properties = {}
        self.relationships = []
        self.extends = None
        self.export = EXPORT

        self.OGMNode = node.OGMNode
        
    def save(self, location, packagename):
        self.OGMNode = self.OGMNode.replace('<<PACKAGE>>', 'package ' + packagename + ';\n')
        self.OGMNode = self.OGMNode.replace('<<IMPORTS>>', str('\n'.join(self.imports.get('node'))))
        self.OGMNode = self.OGMNode.replace('<<ACCESS>>', 'public')
        if(self.abstract == True):
            self.OGMNode = self.OGMNode.replace('<<ABSTRACT>>','abstract')
        else:
            self.OGMNode = self.OGMNode.replace('<<ABSTRACT>>','')
        self.OGMNode = self.OGMNode.replace('<<CLASSNAME>>', self.nodeName)
        if(self.extends is None):
            self.OGMNode = self.OGMNode.replace('<<EXTENDS>>','')
        else:
            self.OGMNode = self.OGMNode.replace('<<EXTENDS>>', 'extends ' + self.extends)
        
        properties = ''''''
        hasId = False
        for property in self.properties:
            if(len(property.split(':')) > 1 and property.split(':')[1].lower() == 'id'):
                properties += '@Id\nprivate ' + self.properties[property] + ' ' + property.split(':')[0] + ';\n'
                hasId = True
            else:
                properties += 'private ' + self.properties[property] + ' ' + property + ';\n'
        
        if(hasId == False and self.extends is None):
            properties += '\n@Id\n\@GeneratedValue\nprivate Long Id;'

        self.OGMNode = self.OGMNode.replace('<<PROPERTIES>>', properties)

        relationships = ''''''
        for relationship in self.relationships:
            if('startNode' in relationship and 'endNode' in relationship):
                ogmRelationship = OGMRelationship.relationship(relationship.get('startNode'), relationship.get('endNode'), relationship.get('type').split(':')[0], relationship.get('properties'), self.imports.get('relationship'))
                ogmRelationship.save(self.export + 'relationships/' + self.nodeName + '/')
            else:
                if(relationship.get('list') == True):
                    relationships += '@Relationship(type="' + relationship.get('type').split(':')[0] + '", direction="OUTGOING")\n\t\tprivate List<' + relationship.get('endNode') + '> ' + relationship.get('endNode')
                else:
                    relationships += '@Relationship(type="' + relationship.get('type').split(':')[0] + '", direction="OUTGOING")\n\t\tprivate ' + relationship.get('endNode') + ' ' + relationship.get('endNode')

        self.OGMNode = self.OGMNode.replace('<<RELATIONSHIPS>>', relationships)

        path = ''
        for _location in location.split('/'):
            path += _location + '/'
            if(os.path.exists(path) == False):
                os.mkdir(path)

        with open(path + self.nodeName + '.java', "w") as file:
            file.write(self.OGMNode)
