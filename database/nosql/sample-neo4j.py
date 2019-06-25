from neo4j import GraphDatabase, basic_auth
from py2neo import Node, Relationship, Graph


class SampleNeo(object):

    def __init__(self):
        self.graph = Graph("localhost", username="neo4j", password="chen19910531")
        pass

    def __del__(self):
        pass

    def insert_data(self):
        u1 = Node(label="Person", name="Mengfei")
        u2 = Node(label="Person", name="Xidong")
        self.graph.create(u1)
        self.graph.create(u2)

        b1 = Node(label="Beer", name="IPA")
        b2 = Node(label="Beer", name="Rosee")
        self.graph.create(b1)
        self.graph.create(b2)

        r1 = Relationship(u1, "likes", b1)
        r1['count'] = 1
        r2 = Relationship(u2, "likes", b2)
        r2['count'] = 1
        r3 = Relationship(u1, "friends", u2)
        r3['count'] = 1
        self.graph.create(r1)
        self.graph.create(r2)
        self.graph.create(r3)


    def search_data(self):
        nodes = self.graph.nodes.match(label="Person")
        node = nodes.first()
        # rel = self.graph.run("MATCH p=()-->() RETURN p LIMIT 25")
        rel = self.graph.match([node], ["likes"])
        print(rel.first())
        for i in rel:
            print(i)

s = SampleNeo()
s.insert_data()
s.search_data()