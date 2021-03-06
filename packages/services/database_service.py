
from packages import db


class DatabaseService:
    session = db.session

    # attribute_of_object - e.g. User.username (NOTE: object here means type and must be written capitalized)
    def already_exists(self, model, attribute_of_object, unique_value):
        result = self.session.query(model).filter(attribute_of_object == unique_value).all()
        return False if len(result) == 0 else True

    def add_to_db(self, *objects):
        self.session.add_all(*objects)
        self.session.commit()

    def get_object(self, model, attribute_of_object, unique_value):
        result = self.session.query(model).filter(attribute_of_object == unique_value).first()
        return result
