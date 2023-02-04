import os, json
import node as OGMNode

IMPOER_DIR = 'import/'
EXPORT_DIR = 'export/'
ARROWGRAPH = 'arrowGraph.json'

PROJECT = 'Maven'
LANGUAGE = 'Java'

GROUP = 'com.example'
ARTIFACT = 'demo'
NAME = 'demo'
PACKAGENAME = GROUP + '.' + NAME

PACKAGING = 'War'


IMPORTS = {
    'node' : [
        'import org.neo4j.ogm.annotation.NodeEntity;',
        'import org.neo4j.ogm.annotation.Id;',
        'import org.neo4j.ogm.annotation.Labels;',
        'import lombok.Getter;',
        'import lombok.Setter;',
    ],
    'relationships' : [
        'import org.neo4j.ogm.annotation.RelationshipEntity;',
        'import org.neo4j.ogm.annotation.StartNode;',
        'import org.neo4j.ogm.annotation.EndNode;',
    ]
}

def getArrowGraph() -> dict:
    arrowGraph = {
        'nodes' : {},
        'relationships' : {}
    }
    with open(IMPOER_DIR + ARROWGRAPH, 'r') as file:
        _arrowGraph = json.load(file)
        for node in _arrowGraph['nodes']:
            arrowGraph['nodes'].update({
                node.get('id') : node
            })

        for relationship in _arrowGraph['relationships']:
            if(relationship.get('fromId') not in arrowGraph['relationships']):
                arrowGraph['relationships'].update({
                    relationship.get('fromId') : []
                })
            
            arrowGraph['relationships'][relationship.get('fromId')].append(relationship)

    return arrowGraph

def main() -> None:
    nodes = getArrowGraph().get('nodes')
    relationships = getArrowGraph().get('relationships')
    for node in nodes:
        if(len(nodes[node].get('labels')) > 0):
            # node has at least one label (classname)
            for index, label in enumerate(nodes[node].get('labels')):
                if(index == 0):
                    # first label is the class name
                    if(len(label.split(':')) > 1):
                        OGMnode = OGMNode.node(label.split(':')[0])
                        if(label.split(':')[1].lower() == 'abstract'):
                            OGMnode.abstract = True
                        else:
                            OGMnode.extends = label.split(':')[1].capitalize()
                    else:
                        OGMnode = OGMNode.node(label)
                else:
                    # additional labels for the node
                    OGMnode.lables.append(label)

            if(node in relationships):
                for relationship in relationships[node]:
                    relationship.update({
                        'endNode' : nodes[relationship.get('toId')].get('labels')[0].split(':')[0]
                    })

                    if(relationship.get('properties')):
                        # relationship has additional properties => RelationshipClass needed
                        relationship.update({
                            'startNode' : nodes[node].get('labels')[0].split(':')[0],
                        })
                    
                    if(relationship.get('type') is not None and len(relationship.get('type').split(':')) > 0):
                        relationshipType = relationship.get('type').split(':')[1]

                        if(relationshipType == '[0..1]'):
                            relationship.update({
                                'list' : False,
                                'constructor' : False
                            })
                        elif(relationshipType == '[1..1]'):
                            relationship.update({
                                'list' : False,
                                'constructor' : True
                            })
                        elif(relationshipType == '[0..*]'):
                            relationship.update({
                                'list' : True,
                                'constructor' : False
                            })
                        elif(relationshipType == '[1..*]'):
                            relationship.update({
                                'list' : True,
                                'constructor' : True
                            })
                        else:
                            print(f"Relationship {relationship.get('type')} has no known relationship pattern: [0..1],[1..1],[0..*],[1..*]")
                    else:
                        # Default relationship: 0..1
                        relationship.update({
                            'list' : False,
                            'constructor' : False
                        })
                    OGMnode.relationships.append(relationship)

            OGMnode.properties.update(nodes[node].get('properties'))
            OGMnode.imports = IMPORTS['node'].copy()

            OGMnode.save(EXPORT_DIR + 'Models/', PACKAGENAME)
        else:
            print(f'Warnning: {node} is without Labels')

if __name__ == '__main__':
    #GROUP = input('Insert your Project Metadata for the Group: ')
    #ARTIFACT = input('Insert your Project Metadata for the Artifact: ')
    #NAME = input('Insert your Project Metadata for the Name: ')
    main()
