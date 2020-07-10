from mongoengine import Document, StringField, EmailField,\
    BooleanField, DictField, ReferenceField, DateTimeField, IntField, signals
from datetime import datetime


class Client(Document):
    uid = IntField()
    name = StringField()
    hostname = StringField()
    email = EmailField()
    path = StringField()
    remote = BooleanField(default=False)
    status = BooleanField(default=False)


class Structure(Document):
    client = ReferenceField(Client)
    date = DateTimeField(default=datetime.now)
    structure = DictField()


class Log(Document):
    client = ReferenceField(Client)
    date = DateTimeField(default=datetime.now())
    type = IntField()
    item = StringField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.date = datetime.now()


signals.pre_save.connect(Log.pre_save, sender=Log)
