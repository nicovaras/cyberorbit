# cyberorbit/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func # For default timestamps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Import UserMixin for Flask-Login integration

# Initialize SQLAlchemy instance - this will be properly configured in app.py
# For now, create a placeholder instance
db = SQLAlchemy()

# --- Model Definitions ---

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Relationships (loads related data automatically or via queries)
    exercise_completions = db.relationship('UserExerciseCompletion', backref='user', lazy=True, cascade="all, delete-orphan")
    ctf_completions = db.relationship('UserCtfCompletion', backref='user', lazy=True, cascade="all, delete-orphan")
    badges = db.relationship('UserBadge', backref='user', lazy=True, cascade="all, delete-orphan")
    streak = db.relationship('UserStreak', uselist=False, backref='user', lazy=True, cascade="all, delete-orphan") # One-to-one
    node_statuses = db.relationship('UserNodeStatus', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Graph(db.Model):
    __tablename__ = 'graphs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    nodes = db.relationship('Node', backref='graph', lazy=True)

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Text, primary_key=True)
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    popup_text = db.Column(db.Text)
    pdf_link = db.Column(db.Text)
    exercises = db.relationship('Exercise', backref='node', cascade="all, delete-orphan")
    # Relationships defined in NodeRelationship model
    # user_statuses = db.relationship('UserNodeStatus', backref='node', lazy=True) # Relationship to user status

# Junction table for node relationships
class NodeRelationship(db.Model):
    __tablename__ = 'node_relationships'
    relationship_id = db.Column(db.Integer, primary_key=True)
    parent_node_id = db.Column(db.Text, db.ForeignKey('nodes.id'), nullable=False)
    child_node_id = db.Column(db.Text, db.ForeignKey('nodes.id'), nullable=False)
    relationship_type = db.Column(db.String(15), nullable=False) # 'CHILD' or 'PREREQUISITE'

    # Define relationships to allow querying like parent_node.children or child_node.parents
    parent_node = db.relationship('Node', foreign_keys=[parent_node_id], backref=db.backref('child_links', lazy='dynamic', cascade="all, delete-orphan"))
    child_node = db.relationship('Node', foreign_keys=[child_node_id], backref=db.backref('parent_links', lazy='dynamic', cascade="all, delete-orphan"))


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Text, primary_key=True)
    node_id = db.Column(db.Text, db.ForeignKey('nodes.id'), nullable=False)
    label = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=10)
    optional = db.Column(db.Boolean, default=False)
    categories = db.relationship('ExerciseCategory', secondary='exercise_category_map', backref=db.backref('exercises', lazy='dynamic'))
    # user_completions = db.relationship('UserExerciseCompletion', backref='exercise', lazy=True) # Relationship to user completion

class ExerciseCategory(db.Model):
    __tablename__ = 'exercise_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# Many-to-many mapping table for exercises and categories
exercise_category_map = db.Table('exercise_category_map', db.metadata,
    db.Column('map_id', db.Integer, primary_key=True),
    db.Column('exercise_id', db.Text, db.ForeignKey('exercises.id'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('exercise_categories.category_id'), nullable=False),
    db.UniqueConstraint('exercise_id', 'category_id', name='uq_exercise_category')
)

class Ctf(db.Model):
    __tablename__ = 'ctfs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    link = db.Column(db.Text)
    # user_completions = db.relationship('UserCtfCompletion', backref='ctf', lazy=True) # Relationship to user completion

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.Text)
    # users = db.relationship('UserBadge', backref='badge', lazy=True) # Relationship to user badges

# --- User Progress Tables ---

class UserExerciseCompletion(db.Model):
    __tablename__ = 'user_exercise_completion'
    completion_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Text, db.ForeignKey('exercises.id'), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    __table_args__ = (db.UniqueConstraint('user_id', 'exercise_id', name='uq_user_exercise'),)
    # Relationships defined via backref in User and Exercise

class UserCtfCompletion(db.Model):
    __tablename__ = 'user_ctf_completion'
    completion_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ctf_id = db.Column(db.Integer, db.ForeignKey('ctfs.id'), nullable=False)
    completed_count = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('user_id', 'ctf_id', name='uq_user_ctf'),)
    # Relationships defined via backref in User and Ctf
    ctf = db.relationship('Ctf', backref=db.backref('user_completions', lazy=True)) # Add relationship here if needed


class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    user_badge_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Text, db.ForeignKey('badges.id'), nullable=False)
    earned_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    shown = db.Column(db.Boolean, default=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='uq_user_badge'),)
    # Relationships defined via backref in User and Badge
    badge = db.relationship('Badge', backref=db.backref('user_badges', lazy=True)) # Add relationship here if needed


class UserStreak(db.Model):
    __tablename__ = 'user_streaks'
    user_streak_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    current_streak = db.Column(db.Integer, default=0)
    last_used_date = db.Column(db.Date)
    # Relationship defined via backref in User

class UserNodeStatus(db.Model):
    __tablename__ = 'user_node_status'
    status_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    node_id = db.Column(db.Text, db.ForeignKey('nodes.id'), nullable=False)
    unlocked = db.Column(db.Boolean, default=False)
    discovered = db.Column(db.Boolean, default=False)
    percent_complete = db.Column(db.Integer, default=0)
    user_notes = db.Column(db.Text)
    __table_args__ = (db.UniqueConstraint('user_id', 'node_id', name='uq_user_node'),)
    # Relationships defined via backref in User and Node
    node = db.relationship('Node', backref=db.backref('user_statuses', lazy=True)) # Add relationship here if needed