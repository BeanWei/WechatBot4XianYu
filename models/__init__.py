from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, DateTime


class BaseModel(Model):
    create_at = Column(DateTime, default=datetime.utcnow())

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}


db = SQLAlchemy(model_class=BaseModel)