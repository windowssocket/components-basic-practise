from cassandra.cluster import Cluster, BatchStatement
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel


class SampleCassandra(object):

    def __init__(self):
        self.cluster = None
        self.session = None
        self.keyspace = None
        self.log = None

    def __del__(self):
        self.cluster.shutdown()

    def createsession(self):
        self.cluster = Cluster(['localhost'])
        self.session = self.cluster.connect(self.keyspace)

    def getsession(self):
        return self.session

    # create keyspace
    def createkeyspace(self, keyspace):
        rows = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        print([row[0] for row in rows])
        if keyspace in [row[0] for row in rows]:
            print("found keyspace")
            self.session.execute("DROP KEYSPACE " + keyspace)
        self.session.execute("""
                            CREATE KEYSPACE %s 
                            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' } 
                            """ % keyspace)
        self.session.set_keyspace(keyspace)

    def create_table(self):
        c_sql = """
        CREATE TABLE IF NOT EXISTS employee (emp_id int PRIMARY KEY, 
        ename varchar, sal double, city varchar);
        """
        self.session.execute(c_sql)
        print("employee table created")

    def insert_data(self):
        insert_sql = self.session.prepare("INSERT INTO employee (emp_id, ename, sal, city) VALUES (?, ?, ?, ?)")
        batch = BatchStatement()
        batch.add(insert_sql, (1, 'xidong', 28000, 'Shanghai'))
        batch.add(insert_sql, (2, 'mengfei', 20000, 'Shanghai'))
        batch.add(insert_sql, (3, None, 200, "Shanghai"))
        self.session.execute(batch)
        print("insert finished")

    def select_data(self):
        rows = self.session.execute('select * from employee limit 5;')
        for row in rows:
            print(row.ename, row.sal)

    def update_data(self):
        pass

    def delete_data(self):
        pass


s = SampleCassandra()
s.createsession()
s.createkeyspace("helloworld")
s.create_table()
s.insert_data()
s.select_data()
