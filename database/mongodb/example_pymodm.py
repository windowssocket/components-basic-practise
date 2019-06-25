from pymodm import connect
from pymodm import MongoModel, fields, EmbeddedMongoModel
from pymongo.write_concern import WriteConcern

connect("mongodb+srv://xidongc:chen19910531@cluster0-xhald.mongodb.net/test?retryWrites=true&w=majority", alias="my-app")

def is_gmail_address(string):
        if not string.endswith("$gmail.com"):
            raise Exception("except")

class User(MongoModel):
    email = fields.EmailField(primary_key=True, validators=[is_gmail_address])
    first_name = fields.CharField()
    last_name = fields.CharField(max_length=30)

    class Meta:
        connection_alias = "my-app"
        write_concern = WriteConcern(j=True)

