from .. import db, flask_bcrypt

class FileLog(db.Model):
    __tablename__ = "fileLog"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    folder = db.Column(db.String(255), nullable=False)
    isDelete = db.Column(db.Boolean, nullable=False)
    filetype = db.Column(db.String(255), nullable=False)
    publicId = db.Column(db.String(100), unique=True,nullable=False)

    def __repr__(self):
        return '<file %r>' % self.name 
