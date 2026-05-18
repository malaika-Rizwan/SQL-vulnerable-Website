from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    total_score = db.Column(db.Integer, default=0, nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    badges = db.Column(db.String(512), default="", nullable=False)
    last_activity = db.Column(db.DateTime, default=utcnow, nullable=False)

    submissions = db.relationship("Submission", back_populates="user", lazy="dynamic")
    progress = db.relationship("Progress", back_populates="user", lazy="dynamic")


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    sqli_type = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String(120), nullable=False)
    hints = db.Column(db.Text, default="[]", nullable=False)
    description = db.Column(db.Text, nullable=False)
    practice = db.Column(db.Boolean, default=True, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False, index=True
    )
    submitted_flag = db.Column(db.String(120), nullable=False)
    correct = db.Column(db.Boolean, default=False, nullable=False)
    points_awarded = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="submissions")
    challenge = db.relationship("Challenge")


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    completed_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="progress")

    __table_args__ = (db.UniqueConstraint("user_id", "challenge_id", name="uq_user_challenge"),)
