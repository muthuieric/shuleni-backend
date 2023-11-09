from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)

class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String)
    email_address = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    role = db.relationship('Role', backref='users')


class School(db.Model, SerializerMixin):

    __tablename__ = "schools"

    id = db.Column(db.Integer(), primary_key=True)
    school_name = db.Column(db.String, nullable=False)
    poster = db.Column(db.String(), nullable=False) 
    location = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    educators = db.relationship('User', backref= 'classes')

    
    
class Class(db.Model, SerializerMixin):

    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, nullable=False)
    educator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable= False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    educators = db.relationship('User', backref= 'class')
    schoools = db.relationship('School', backref = 'class')


class Student_Class(db.Model, SerializerMixin):
    
    __tablename__ = 'student_classes'

    id = db.Column(db.Integer(), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable= False)
    student_id = db.Column(db.String, db.ForeignKey('users.id'), nullable= False)

    classes = db.relationship('Class', backref='student_classes')
    senders = db.relationship('User', backref= 'student_classes')



class Attendance(db.Model, SerializerMixin):

    __tablename__ = 'attendances'

    id = db.Column(db.Integer(), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable= False)
    student_id = db.Column(db.String, db.ForeignKey('users.id'), nullable= False)
    date = db.Column(db.String)
    is_present = db.Column(db.Boolean)

    classes = db.relationship('Class', backref='attendances')
    senders = db.relationship('User', backref= 'attendances')

class Resource(db.Model, SerializerMixin):

    __tablename__ = 'resources'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    url = db.Column(db.String)
    content = db.Column(db.String)
    educator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)

    educators = db.relationship('User', backref= 'resources')

class Assessment(db.Model, SerializerMixin):

    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable= False)
    title = db.Column(db.String)
    body = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    duration = db.Column(db.Integer)

    classes = db.relationship('Class', backref='assessments')


class Assessment_Response(db.Model, SerializerMixin):

    __tablename__ = 'assessment_responses'

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    student_id = db.Column(db.String, db.ForeignKey('users.id'), nullable= False)
    submitted_time = db.Column(db.DateTime, server_default=db.func.now())
    work = db.Column(db.String)

    asssessments = db.relationship('Assessment', backref='assesment_responses')
    students = db.relationship('User', backref= 'assesment_responses')


class Chat(db.Model, SerializerMixin):

    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable= False)
    sender = db.Column(db.String, db.ForeignKey('users.id'), nullable= False)
    message = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    classes = db.relationship('Class', backref='chats')
    senders = db.relationship('User', backref= 'chats')

    