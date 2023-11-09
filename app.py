import os
from flask import Flask, jsonify, request,make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy import desc, asc
from flask_cors import CORS


from models import db, User, School, Role, Assessment, Assessment_Response, Attendance, Chat, Class, Student_Class, Resource as Resource_model

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)  
api = Api(app)
# CORS(app)


@app.route('/')
def hello_world():
    return make_response(jsonify({'message': 'welcome to shuleni API'}), 200)



#-------------------------------------------------USER ROUTES-----------------------------------------------------------------


class Users(Resource):
    
    def get(self):
        list = []
        for user in User.query.all():
            role_data = Role.query.filter(Role.id == user.role_id).first()
            role_name = role_data.role
            user_dict ={
                'id': user.id,
                'name': user.name,
                'phone_number': user.phone_number,
                'photo': user.photo,
                'email_adress': user.email_address,
                'password': user.password,
                'role_id': user.role_id,
                'role': role_name
            }
            list.append(user_dict)
            
        return make_response(jsonify(list), 200)
    
    def post(self):
        data = request.get_json()
        new_user = User(
            name = data.get('name'),
            phone_number = data.get('phone_number'),
            photo = data.get('photo'),
            email_address = data.get('email_address'),
            password = data.get('password'),
            role_id = data.get('role_id'),
        )
        db.session.add(new_user)
        db.session.commit()
        
        role = Role.query.filter_by(id = new_user.role_id).first()
        new_user_dict = {
            'id': new_user.id,
            'name': new_user.name,
            'phone_number': new_user.phone_number,
            'photo': new_user.photo,
            'email_adress': new_user.email_address,
            'password': new_user.password,
            'role_id': new_user.role_id,
            'role': role.role
        }
        
        return make_response(jsonify(new_user_dict), 200)
    
    
class UserById(Resource):
    
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        
        if user:
            role = Role.query.filter_by(id = user.role_id).first()
            user_dict ={
                'id': user.id,
                'name': user.name,
                'phone_number': user.phone_number,
                'photo': user.photo,
                'email_adress': user.email_address,
                'password': user.password,
                'role_id': user.role_id,
                'role': role.role
            }
            
            return make_response(jsonify(user_dict), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)
        
    
    def patch(self, id):
        user = User.query.filter(User.id == id).first()
        
        if user:
            data = request.get_json()
            
            for attr in data:
                setattr(user, attr, data.get(attr))
                
            db.session.commit()
            
            role = Role.query.filter_by(id = user.role_id).first()
            user_dict ={
                'id': user.id,
                'name': user.name,
                'phone_number': user.phone_number,
                'photo': user.photo,
                'email_adress': user.email_address,
                'password': user.password,
                'role_id': user.role_id,
                'role': role.role
            }
            return make_response(jsonify(user_dict), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        
        if user:
            db.session.delete(user)
            db.session.commit()
            
            return make_response(jsonify({"message": "User deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)
   
        
#-------------------------------------------------SCHOOL ROUTES-----------------------------------------------------------------
    
class Schools(Resource):
    
    def get(self):
        list = []
        for school in School.query.all():
            owner_data = User.query.filter(User.id == school.owner_id).first()
            owner_name = owner_data.name
            school_dict = {
                'id': school.id,
                'school_name': school.school_name,
                'poster': school.poster,
                'location': school.location,
                'owner_id': school.owner_id,
                'created_at': school.created_at,
                'owner_name': owner_name,
            }
            list.append(school_dict)
        
        return make_response(jsonify(list), 200)
    
    def post(self):
        data = request.get_json()
        new_school = School(
            school_name = data.get('school_name'),
            poster = data.get('poster'),
            location = data.get('location'),
            owner_id = data.get('owner_id'),
        )
        db.session.add(new_school)
        db.session.commit()
        
        owner = User.query.filter_by(id = new_school.owner_id).first()
        new_school_dict = {
            'id': new_school.id,
            'school_name': new_school.school_name,
            'poster': new_school.poster,
            'location': new_school.location,
            'owner_id': new_school.owner_id,
            'created_at': new_school.created_at,
            'owner_name': owner.name,
        }
        return make_response(jsonify(new_school_dict), 200)
    

class SchoolById(Resource):
    
    def get(self, id):
        school = School.query.filter_by(id = id).first()
        
        if school:
            owner = User.query.filter_by(id = school.owner_id).first()
            school_dict ={
            'id': school.id,
            'school_name': school.school_name,
            'poster': school.poster,
            'location': school.location,
            'owner_id': school.owner_id,
            'created_at': school.created_at,
            'owner_name': owner.name,
            }
            return make_response(jsonify(school_dict), 200)
        else:
            return make_response(jsonify({"error": "School not found"}), 404)
        
    def patch(self, id):
        school = School.query.filter_by(id = id).first()
        
        if school:
            data = request.get_json()
            
            for attr in data:
                setattr(school, attr, data.get(attr))
                
            db.session.commit()
            
            owner = User.query.filter_by(id = school.owner_id).first()
            school_dict ={
            'id': school.id,
            'school_name': school.school_name,
            'poster': school.poster,
            'location': school.location,
            'owner_id': school.owner_id,
            'created_at': school.created_at,
            'owner_name': owner.name,
            }
            return make_response(jsonify(school_dict), 200)
        else:
            return make_response(jsonify({"error": "School not found"}), 404)
          
        
    def delete(self, id):
        school = School.query.filter_by(id = id).first()
        
        if school:
            db.session.delete(school)
            db.session.commit()
            
            return make_response(jsonify({"message": "School deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "School not found"}), 404)
     
     
#-------------------------------------------------CLASS ROUTES-----------------------------------------------------------------

    
class Classes(Resource):
    
    def get(self):
        list=[]
        for class_rm in Class.query.all():
            educator_data = User.query.filter(User.id == class_rm.educator_id).first()
            school_data = School.query.filter(School.id == class_rm.school_id).first()
            educator = educator_data.name
            school = school_data.school_name
            class_dict ={
                'id': class_rm.id,
                'class_name': class_rm.class_name,
                'educator_id': class_rm.educator_id,
                'school_id': class_rm.school_id,
                'created_at': class_rm.created_at,
                'educator': educator,
                'school': school
            }
            list.append(class_dict)
            
        return make_response(jsonify(list), 200)
    
    def post(self):
        data = request.get_json()
        new_class = Class(
            class_name = data.get('class_name'),
            educator_id = data.get('educator_id'),
            school_id = data.get('school_id'),
        )
        db.session.add(new_class)
        db.session.commit()
        
        educator = User.query.filter_by(id = new_class.educator_id).first()
        school = School.query.filter_by( id = new_class.school_id).first()
        new_class_dict = {
            'id': new_class.id,
            'class_name': new_class.class_name,
            'educator_id': new_class.educator_id,
            'school_id': new_class.school_id,
            'created_at': new_class.created_at,
            'educator': educator.name,
            'school': school.school_name     
        }
        return make_response(jsonify(new_class_dict), 200)


class ClassById(Resource):
    
    def get(self, id):
        class_rm = Class.query.filter_by(id=id).first()
        
        if class_rm:
            educator = User.query.filter(User.id == class_rm.educator_id).first()
            school = School.query.filter(School.id == class_rm.school_id).first()
            class_rm_dict ={
                'id': class_rm.id,
                'class_name': class_rm.class_name,
                'educator_id': class_rm.educator_id,
                'school_id': class_rm.school_id,
                'created_at': class_rm.created_at,
                'educator': educator.name,
                'school': school.school_name
            }
            return make_response(jsonify(class_rm_dict))
        else:
            return make_response(jsonify({"error": "Class not found"}), 404)
        
        
    def patch(self, id):
        class_rm = Class.query.filter_by(id=id).first()
        
        if class_rm:
            data = request.get_json()
            
            for attr in data:
                setattr(class_rm, attr, data.get(attr))
                
            db.session.commit()
            
            educator = User.query.filter(User.id == class_rm.educator_id).first()
            school = School.query.filter(School.id == class_rm.school_id).first()
            class_rm_dict ={
                'id': class_rm.id,
                'class_name': class_rm.class_name,
                'educator_id': class_rm.educator_id,
                'school_id': class_rm.school_id,
                'created_at': class_rm.created_at,
                'educator': educator.name,
                'school': school.school_name
            }
            return make_response(jsonify(class_rm_dict))
        else:
            return make_response(jsonify({"error": "Class not found"}), 404)
        

        
    def delete(self, id):
        class_rm = Class.query.filter_by(id = id).first()
        
        if class_rm:
            db.session.delete(class_rm)
            db.session.commit()
            
            return make_response(jsonify({"message": "Class deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Class not found"}), 404)
    

class StudentClasses(Resource):
    
    def get(self):
        list =[]
        
        for x in Student_Class.query.all():
            class_data = Class.query.filter(Class.id == x.class_id).first()
            student_data = User.query.filter(User.id == x.student_id).first()
            student_nm = student_data.name
            class_nm = class_data.class_name
            x_dict ={
                'id': x.id,
                'class_id': x.class_id,
                'student_id': x.student_id,
                'student': student_nm,
                'class': class_nm,
            }
            list.append(x_dict)
            
        return make_response(jsonify(list), 200)
    
        
    def post(self):
        data = request.get_json()
        new_x = Student_Class(
            class_id = data.get('class_id'),
            student_id = data.get('student_id'),
        )
        db.session.add(new_x)
        db.session.commit()
        
        student = User.query.filter_by(id = new_x.student_id).first()
        class_rm = Class.query.filter_by( id = new_x.class_id).first()
        new_x_dict = {
            'id': new_x.id,
            'class_id': new_x.class_id,
            'student_id': new_x.student_id,
            'student': student.name,
            'class': class_rm.class_name    
        }
        return make_response(jsonify(new_x_dict), 200)



class StudentClassesId(Resource):
    
    def get(self, id):
        x = Student_Class.query.filter_by(id=id).first()
        
        if x:
            class_data = Class.query.filter(Class.id == x.class_id).first()
            student = User.query.filter(User.id == x.student_id).first()
            x_dict ={
                'id': x.id,
                'class_id': x.class_id,
                'student_id': x.student_id,
                'student': student.name,
                'class': class_data.class_name,
            }
            return make_response(jsonify(x_dict))
        else:
            return make_response(jsonify({"error": "Class not found"}), 404)
        
        
    def patch(self, id):
        x = Student_Class.query.filter_by(id=id).first()
        
        if x:
            data = request.get_json()
            
            for attr in data:
                setattr(x, attr, data.get(attr))
                
            db.session.commit()
            
            class_data = Class.query.filter(Class.id == x.class_id).first()
            student = User.query.filter(User.id == x.student_id).first()
            x_dict ={
                'id': x.id,
                'class_id': x.class_id,
                'student_id': x.student_id,
                'student': student.name,
                'class': class_data.class_name,
            }
            return make_response(jsonify(x_dict))
        else:
            return make_response(jsonify({"error": "Class not found"}), 404)
        

        
    def delete(self, id):
        x = Student_Class.query.filter_by(id=id).first()
        
        if x:
            db.session.delete(x)
            db.session.commit()
            
            return make_response(jsonify({"message": "Class and student removed successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Class not found"}), 404)
   
   
#-------------------------------------------------ATTENDANCE ROUTES-----------------------------------------------------------------


class Attendances(Resource):
    
    def get(self):
        list = []
        
        for attendance in Attendance.query.all():
            class_data = Class.query.filter(Class.id == attendance.class_id).first()
            student_data = User.query.filter(User.id == attendance.student_id).first()
            student_nm = student_data.name
            class_nm = class_data.class_name
            attendance_dict= {
                'id': attendance.id,
                'class_id': attendance.class_id,
                'student_id': attendance.student_id,
                'date': attendance.date,
                'is_present': attendance.is_present,
                'student': student_nm,
                'class': class_nm,
            }
            list.append(attendance_dict)
            
        return make_response(jsonify(list), 200)
    
        
    def post(self):
        data = request.get_json()
        new_attendance = Attendance(
            class_id = data.get('class_id'),
            student_id = data.get('student_id'),
            date = data.get('date'),
            is_present = data.get('is_present'),
        )
        db.session.add(new_attendance)
        db.session.commit()
        
        student = User.query.filter_by(id = new_attendance.student_id).first()
        class_rm = Class.query.filter_by( id = new_attendance.class_id).first()
        new_class_dict = {
            'id': new_attendance.id,
            'class_id': new_attendance.class_id,
            'student_id': new_attendance.student_id,
            'date': new_attendance.date,
            'is_present': new_attendance.is_present,
            'student': student.name,
            'class': class_rm.class_name   
        }
        return make_response(jsonify(new_class_dict), 200)


class AttendanceById(Resource):
    
    def get(self, id):
        attendance = Attendance.query.filter_by(id=id).first()
        
        if attendance:
            class_data = Class.query.filter(Class.id == attendance.class_id).first()
            student_data = User.query.filter(User.id == attendance.student_id).first()
            student_nm = student_data.name
            class_nm = class_data.class_name
            attendance_dict= {
                'id': attendance.id,
                'class_id': attendance.class_id,
                'student_id': attendance.student_id,
                'date': attendance.date,
                'is_present': attendance.is_present,
                'student': student_nm,
                'class': class_nm,
            }
            return make_response(jsonify(attendance_dict))
        else:
            return make_response(jsonify({"error": "Attendance not found"}), 404)
        
        
    def patch(self, id):
        attendance = Attendance.query.filter_by(id=id).first()
        
        if attendance:
            data = request.get_json()
            
            for attr in data:
                setattr(attendance, attr, data.get(attr))
                
            db.session.commit()
            
            class_data = Class.query.filter(Class.id == attendance.class_id).first()
            student_data = User.query.filter(User.id == attendance.student_id).first()
            student_nm = student_data.name
            class_nm = class_data.class_name
            attendance_dict= {
                'id': attendance.id,
                'class_id': attendance.class_id,
                'student_id': attendance.student_id,
                'date': attendance.date,
                'is_present': attendance.is_present,
                'student': student_nm,
                'class': class_nm,
            }
            return make_response(jsonify(attendance_dict))
        else:
            return make_response(jsonify({"error": "Attendance not found"}), 404)

        
    def delete(self, id):
        attendance = Attendance.query.filter_by(id=id).first()
        
        if attendance:
            db.session.delete(attendance)
            db.session.commit()
            
            return make_response(jsonify({"message": "Attendance deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Attendance not found"}), 404)
 
 
 #-------------------------------------------------RESOURCES ROUTES-----------------------------------------------------------------
 
    
class Resources(Resource):
    
    def get(self):
        list = []
        
        for resource in Resource_model.query.all():
            educator = User.query.filter_by( id = resource.educator_id ).first()
            resource_dict ={
                'id': resource.id,
                'title': resource.title,
                'type': resource.type,
                'url': resource.url,
                'content': resource.content,
                'educator_id': resource.educator_id,
                'educator': educator.name
            }
            list.append(resource_dict)
        
        return make_response(jsonify(list))
    
        
    def post(self):
        data = request.get_json()
        new_resource = Resource_model(
            title = data.get('title'),
            type = data.get('type'),
            url = data.get('url'),
            content = data.get('content'),
            educator_id = data.get('educator_id'),
        )
        db.session.add(new_resource)
        db.session.commit()
        
        educator = User.query.filter_by(id = new_resource.educator_id).first()
        new_resource_dict = {
            'id': new_resource.id,
            'title': new_resource.title,
            'type': new_resource.type,
            'url': new_resource.url,
            'content': new_resource.content,
            'educator_id': new_resource.educator_id,
            'educator': educator.name      
        }
        return make_response(jsonify(new_resource_dict), 200)


class ResourceById(Resource):
    
    def get(self, id):
        resource = Resource_model.query.filter_by(id=id).first()
        
        if resource:
            educator = User.query.filter_by( id = resource.educator_id ).first()
            resource_dict ={
                'id': resource.id,
                'title': resource.title,
                'type': resource.type,
                'url': resource.url,
                'content': resource.content,
                'educator_id': resource.educator_id,
                'educator': educator.name
            }
            return make_response(jsonify(resource_dict))
        else:
            return make_response(jsonify({"error": "Resource not found"}), 404)
        
        
    def patch(self, id):
        resource = Resource_model.query.filter_by(id=id).first()
        
        if resource:
            data = request.get_json()
            
            for attr in data:
                setattr(resource, attr, data.get(attr))
                
            db.session.commit()
            
            educator = User.query.filter_by( id = resource.educator_id ).first()
            resource_dict ={
                'id': resource.id,
                'title': resource.title,
                'type': resource.type,
                'url': resource.url,
                'content': resource.content,
                'educator_id': resource.educator_id,
                'educator': educator.name
            }
            return make_response(jsonify(resource_dict))
        else:
            return make_response(jsonify({"error": "Resource not found"}), 404)

        
    def delete(self, id):
        resource = Resource_model.query.filter_by(id=id).first()
        
        if resource:
            db.session.delete(resource)
            db.session.commit()
            
            return make_response(jsonify({"message": "Resource deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Resource not found"}), 404)


#-------------------------------------------------ASSESSMENTS ROUTES-----------------------------------------------------------------
 

class Assessments(Resource):
    
    def get(self):
        list =[]
        
        for assessment in Assessment.query.all():
            class_data = Class.query.filter(Class.id == assessment.class_id).first()
            class_nm = class_data.class_name
            assessment_dict ={
                'id': assessment.id,
                'class_id': assessment.class_id,
                'title': assessment.title,
                'body': assessment.body,
                'start_time': assessment.start_time,
                'end_time': assessment.end_time,
                'duration':assessment.duration,
                'class': class_nm
            }
            list.append(assessment_dict)
            
        return make_response(jsonify(list), 200)
        
    def post(self):
        data = request.get_json()
        new_assessment = Assessment(
            class_id = data.get('class_id'),
            title = data.get('title'),
            body = data.get('body'),
            start_time = data.get('start_time'),
            end_time = data.get('end_time'),
            duration = data.get('duration')
        )
        db.session.add(new_assessment)
        db.session.commit()
        
        class_rm = Class.query.filter_by( id = new_assessment.class_id).first()
        new_assessment_dict = {
            'id': new_assessment.id,
            'class_id': new_assessment.class_id,
            'title': new_assessment.title,
            'body': new_assessment.body,
            'start_time': new_assessment.start_time,
            'end_time': new_assessment.end_time,
            'duration':new_assessment.duration,
            'class': class_rm.name      
        }
        return make_response(jsonify(new_assessment_dict), 200)


class AssessmentsById(Resource):
    
    def get(self, id):
        assessment = Assessment.query.filter_by(id=id).first()
        
        if assessment:
            class_data = Class.query.filter(Class.id == assessment.class_id).first()
            class_nm = class_data.class_name
            assessment_dict ={
                'id': assessment.id,
                'class_id': assessment.class_id,
                'title': assessment.title,
                'body': assessment.body,
                'start_time': assessment.start_time,
                'end_time': assessment.end_time,
                'duration':assessment.duration,
                'class': class_nm
            }
            return make_response(jsonify(assessment_dict))
        else:
            return make_response(jsonify({"error": "Assessment not found"}), 404)
        
        
    def patch(self, id):
        assessment = Assessment.query.filter_by(id=id).first()
        
        if assessment:
            data = request.get_json()
            
            for attr in data:
                setattr(assessment, attr, data.get(attr))
                
            db.session.commit()
            
            class_data = Class.query.filter(Class.id == assessment.class_id).first()
            class_nm = class_data.class_name
            assessment_dict ={
                'id': assessment.id,
                'class_id': assessment.class_id,
                'title': assessment.title,
                'body': assessment.body,
                'start_time': assessment.start_time,
                'end_time': assessment.end_time,
                'duration':assessment.duration,
                'class': class_nm
            }
            return make_response(jsonify(assessment_dict))
        else:
            return make_response(jsonify({"error": "Assessment not found"}), 404)

    
    def delete(self, id):
        assessment = Assessment.query.filter_by(id=id).first()
        
        if assessment:
            db.session.delete(assessment)
            db.session.commit()
            
            return make_response(jsonify({"message": "Assessment deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Assessment not found"}), 404)
 

class AssessmentResponses(Resource):
    
    def get(self):
        list = []
        
        for response in Assessment_Response.query.all():
            student = User.query.filter_by(id = response.student_id).first()
            response_dict = {
                'id': response.id,
                'assessment_id': response.assessment_id,
                'student_id': response.student_id,
                'submitted_time': response.submitted_time,
                'work': response.work,
                'student': student.name
            }
            list.append(response_dict)
            
        return make_response(jsonify(list), 200)
    
    def post(self):
        data = request.get_json()
        new_response = Assessment_Response(
            assessment_id = data.get('id'),
            student_id = data.get('student_id'),
            submitted_time = data.get('submitted_time'),
            work = data.get('work')
        )
        db.session.add(new_response)
        db.session.commit()
        
        student = User.query.filter_by(id = new_response.student_id).first()
        new_response_dict = {
            'id': new_response.id,
            'assessment_id': new_response.assessment_id,
            'student_id': new_response.student_id,
            'submitted_time': new_response.submitted_time,
            'work': new_response.work,
            'student': student.name
        }
        
        return make_response(jsonify(new_response_dict), 200)


class AssessmentResponseById(Resource):
    
    def get(self, id):
        response = Assessment_Response.query.filter_by(id=id).first()
        
        if response:
            student = User.query.filter_by(id = response.student_id).first()
            response_dict = {
                'id': response.id,
                'assessment_id': response.assessment_id,
                'student_id': response.student_id,
                'submitted_time': response.submitted_time,
                'work': response.work,
                'student': student.name
            }
            return make_response(jsonify(response_dict))
        else:
            return make_response(jsonify({"error": "Assessment_Response not found"}), 404)
       
        
    def patch(self, id):
        response = Assessment_Response.query.filter_by(id=id).first()
        
        if response:
            data = request.get_json()
            
            for attr in data:
                setattr(response, attr, data.get(attr))
                
            db.session.commit()
            
            student = User.query.filter_by(id = response.student_id).first()
            response_dict = {
                'id': response.id,
                'assessment_id': response.assessment_id,
                'student_id': response.student_id,
                'submitted_time': response.submitted_time,
                'work': response.work,
                'student': student.name
            }
            return make_response(jsonify(response_dict))
        else:
            return make_response(jsonify({"error": "Assessment_Response not found"}), 404)

    
    def delete(self, id):
        response = Assessment_Response.query.filter_by(id=id).first()
        
        if response:
            db.session.delete(response)
            db.session.commit()
            
            return make_response(jsonify({"message": "Assessment_Response deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Assessment_Response not found"}), 404)
 
 
 #-------------------------------------------------CHATS ROUTES-----------------------------------------------------------------


class Chats(Resource):
    
    def get(self):
        list = []
        for chat in Chat.query.all():
            host = User.query.filter(User.id == chat.sender).first()
            class_room = Class.query.filter_by(id = chat.class_id).first()
            chat_dict ={
                'id': chat.id,
                'class_id': chat.class_id,
                'sender': chat.sender,
                'message': chat.message,
                'name': host.name,
                'class': class_room.class_name,
                'created_at': chat.created_at
            }
            list.append(chat_dict)
            
        return make_response(jsonify(list))
    
    def post(self):
        data = request.get_json()
        new_chat = Chat(
            class_id = data.get('class_id'),
            sender = data.get('sender'),
            message = data.get('message')
        )
        db.session.add(new_chat)
        db.session.commit()
        
        host = User.query.filter(User.id == new_chat.sender).first()
        class_room = Class.query.filter_by(id = new_chat.class_id).first()
        new_chat_dict = {
            'id': new_chat.id,
            'class_id': new_chat.class_id,
            'sender': new_chat.sender,
            'message': new_chat.message,
            'name': host.name,
            'class': class_room.class_name,
            'created_at': new_chat.created_at
        }
        
        return make_response(jsonify(new_chat_dict), 200)


class ChatsById(Resource):
    
    def get(self, id):
        chat = Chat.query.filter_by(id=id).first()
        
        if chat:
            host = User.query.filter(User.id == chat.sender).first()
            class_room = Class.query.filter_by(id = chat.class_id).first()
            chat_dict ={
                'id': chat.id,
                'class_id': chat.class_id,
                'sender': chat.sender,
                'message': chat.message,
                'name': host.name,
                'class': class_room.class_name,
                'created_at': chat.created_at
            }
            return make_response(jsonify(chat_dict))
        else:
            return make_response(jsonify({"error": "Chat not found"}), 404)
        
    def patch(self, id):
        chat = Chat.query.filter_by(id=id).first()
        
        if chat:
            data = request.get_json()
            
            for attr in data:
                setattr(chat, attr, data.get(attr))
                
            db.session.commit()
            
            host = User.query.filter(User.id == chat.sender).first()
            class_room = Class.query.filter_by(id = chat.class_id).first()
            chat_dict ={
                'id': chat.id,
                'class_id': chat.class_id,
                'sender': chat.sender,
                'message': chat.message,
                'name': host.name,
                'class': class_room.class_name,
                'created_at': chat.created_at
            }
            return make_response(jsonify(chat_dict))
        else:
            return make_response(jsonify({"error": "Chat not found"}), 404)

    def delete(self, id):
        chat = Chat.query.filter_by(id=id).first()
        
        if chat:
            db.session.delete(chat)
            db.session.commit()
            
            return make_response(jsonify({"message": "Chat deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Chat not found"}), 404)
 

api.add_resource(Users, '/users')
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(Schools, '/schools')
api.add_resource(SchoolById, '/school/<int:id>')
api.add_resource(Classes, '/classes')
api.add_resource(ClassById, '/class/<int:id>')
api.add_resource(StudentClasses, '/student_classes')
api.add_resource(StudentClassesId, '/student_class/<int:id>')
api.add_resource(Attendances, '/attendance')
api.add_resource(AttendanceById, '/attendance/<int:id>')
api.add_resource(Resources, '/resources')
api.add_resource(ResourceById, '/resource/<int:id>')
api.add_resource(Assessments, '/assessments')
api.add_resource(AssessmentsById, '/assessment/<int:id>')
api.add_resource(Chats, '/chats')
api.add_resource(ChatsById, '/chat/<int:id>')


if __name__ == '__main__':
    app.run(port = 5555)
    