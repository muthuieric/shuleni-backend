from app import app
from faker import Faker
import random
from datetime import datetime

from models import db, User, Assessment, Assessment_Response, Attendance, Chat, Class,Resource, Role, School, Student_Class

with app.app_context():
    #deleting previous records
        
    User.query.delete()
    Assessment.query.delete()
    Assessment_Response.query.delete()
    Attendance.query.delete()
    Chat.query.delete()
    Class.query.delete()
    Resource.query.delete()
    Role.query.delete()
    School.query.delete()
    Student_Class.query.delete()

    db.session.commit()

    fake = Faker()
    
    print('🦸‍♀️ seeding roles...')
    
    roles_data = [
        {"id": 1, "role": "Owner"},
        {"id": 2, "role": "Instructor"},
        {"id": 3, "role": "Student"}
    ]

    roles = [Role(**role_info) for role_info in roles_data]
    
    db.session.add_all(roles)
    db.session.commit()
    
    print('🦸‍♀️ Seeding users...')
    
    users =[]
    existing_emails = set()  # Keep track of used email addresses

    for _ in range(600):
        role_random = random.choice(roles)
        fake_email = fake.email()

        # email address is unique
        while fake_email in existing_emails:
            fake_email = fake.email()

        existing_emails.add(fake_email)  # Mark the email as used

        user = User(
            name=fake.name(),
            phone_number = fake.phone_number(),
            photo = f'https://dummyimage.com/200x200/{random.randint(10, 100000)}',
            email_address=fake_email,
            password=fake.password(),
            role_id=role_random.id
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()  
    
    print('🦸‍♀️ Seeding schools...')
    
    owners = User.query.filter(User.role_id == 1).all()
    used_posters = set()  # Keep track of used poster URLs
    
    schools =[]
    for _ in range(800):
        random_owner = random.choice(owners)
        unique_poster = f'https://dummyimage.com/200x200/{random.randint(10, 100000)}'
        
        #  poster is unique
        while unique_poster in used_posters:
            unique_poster = f'https://dummyimage.com/200x200/{random.randint(10, 100000)}'

        used_posters.add(unique_poster)  # Mark the poster as used

        school = School(
            school_name=fake.company(),
            poster=unique_poster,
            location=fake.address(),
            owner_id=random_owner.id,
        )
        schools.append(school)

    db.session.add_all(schools)
    db.session.commit()

    
    print('🦸‍♀️ Seeding classes...')
    
    classes = []
    educator = User.query.filter_by(role_id = 2).all()
    for _ in range(400):
        school_random = random.choice(schools)
        class_bd = Class(
            class_name = fake.color_name(),
            educator_id = random.choice(educator).id,
            school_id = school_random.id,
        )
        classes.append(class_bd)
        
    db.session.add_all(classes)
    db.session.commit()
    
    print('🦸‍♀️ Seeding student_class...')

    
    students = User.query.filter_by(role_id = 3).all()
    student_classes =[]
    for _ in range(500):
        classes_random = random.choice(classes)
        student_class = Student_Class(
            class_id = classes_random.id,
            student_id = random.choice(students).id
        )
        student_classes.append(student_class)
        
    db.session.add_all(student_classes)
    db.session.commit()
    
    print('🦸‍♀️ Seeding attendance...')
    
    attendances= []
    for _ in range(500):
        classes_random = random.choice(classes)
        attendance = Attendance(
            class_id = classes_random.id,
            student_id = random.choice(students).id,
            date = "11-11-2023",
            is_present = fake.boolean(chance_of_getting_true=75)
        )
        attendances.append(attendance)
    
    db.session.add_all(attendances)
    db.session.commit()
    
    print('🦸‍♀️ Seeding resources...')
    
    resources =[]
    for _ in range(250):
        resource = Resource(
            title = fake.sentence(),
            type = fake.job(),
            url = fake.url(),
            content = fake.text(),
            educator_id = random.choice(educator).id
        )
        resources.append(resource)
        
    db.session.add_all(resources)
    db.session.commit()
        
    print('🦸‍♀️ Seeding assessments...')
    
    assessments =[]
    for _ in range(250):
        classes_random = random.choice(classes)
        assesment = Assessment(
            class_id = classes_random.id,
            title = fake.sentence(),
            body = fake.text(),
            start_time = '10:00',
            end_time = '12:00',
            duration = 120
        )
        assessments.append(assesment)
        
    db.session.add_all(assessments)
    db.session.commit()
    
    print('🦸‍♀️ Seeding assessments_choice...')
    
    responses = []
    for _ in range(650):
        assessment_random = random.choice(assessments)
        response = Assessment_Response(
            assessment_id = assessment_random.id,
            student_id = random.choice(students).id,
            work = fake.text()
        )        
        responses.append(response)
        
    db.session.add_all(responses)
    db.session.commit()
    
    print('🦸‍♀️ Seeding chats...')
    
    chats = []
    for _ in range(2000):
        user_random = random.choice(users)
        classes_random = random.choice(classes)
        chat = Chat(
            class_id = classes_random.id,
            sender = user_random.id,
            message = fake.text()
        )
        chats.append(chat)
        
    db.session.add_all(chats)
    db.session.commit()