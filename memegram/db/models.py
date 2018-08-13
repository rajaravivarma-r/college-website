from peewee import Model, SqliteDatabase, CharField

from memegram.db import DB_FILE_PATH

db = SqliteDatabase(DB_FILE_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Image(BaseModel):
    filename = CharField()
    filepath = CharField()
    digest = CharField(unique=True)

    def __repr__(self):
        return (
            f"<Image(id: {self.id}, filename: {self.filename}, "
            f"filepath: {self.filepath}, digest: {self.digest}>"
        )


Image.create_table()
