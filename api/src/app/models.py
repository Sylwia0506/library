from . import db


class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    trace = db.Column(db.Text, nullable=True)

    __tablename__ = "system_logs"

    def __repr__(self):
        return f"<SystemLog {self.level}: {self.message[:50]}...>"
