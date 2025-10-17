# Rachel Mercado 30206376
# Hania Aamir 30204312

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

students = [
  {
    "id": 1, "username": "alice", "password": "P@ssword123", "email": "alice@gmail.com", "enrolled_courses": []
  },
  {
    "id": 2, "username": "bob", "password": "S@cure456", "email": "bob@gmail.com", "enrolled_courses": []
  },
  {
    "id": 3, "username": "charlie", "password": "Q@erty789", "email": "charlie@gmail.com", "enrolled_courses": []
  },
  {
    "id": 4, "username": "diana", "password": "H@nter2", "email": "diana@gmail.com", "enrolled_courses": []
  },
  {
    "id": 5, "username": "eve", "password": "P@sspass123", "email": "eve@gmail.com", "enrolled_courses": []
  },
  {
    "id": 6, "username": "frank", "password": "L@tmein123", "email": "frank@gmail.com", "enrolled_courses": []
  },
  {
    "id": 7, "username": "grace", "password": "T@rustno1", "email": "grace@gmail.com", "enrolled_courses": []
  },
  {
    "id": 8, "username": "heidi", "password": "A@dmin123", "email": "heidi@gmail.com", "enrolled_courses": []
  },
  {
    "id": 9, "username": "ivan", "password": "W@elcome1", "email": "ivan@gmail.com", "enrolled_courses": []
  },
  {
    "id": 10, "username": "judy","password": "p@SSWORD123","email": "judy@gmail.com","enrolled_courses": []
  }
]


@app.route('/register',methods=['POST'])
def register():
  data = request.get_json()
  entered_user = data.get('username').lower()
  entered_pass = data.get('password')
  entered_email = data.get('email')
  for user in students:
    if user['username'].lower() == entered_user:
      return jsonify({"success": False, "message": "The username is already taken."})
  last_student_id = students[-1]['id']
  added_student = {"id": last_student_id+1, "username": entered_user, "password": entered_pass, "email": entered_email, "enrolled_courses": []}
  students.append(added_student)
  return jsonify({"success": True, "message": "Signup successful! Redirecting to login..."}) 

@app.route('/login',methods=['POST'])
def login():
  data = request.get_json()
  entered_user = data.get('username').lower()
  entered_pass = data.get('password')
  for user in students:
    if user['username'].lower() == entered_user and user['password'] == entered_pass:
      return jsonify({
        "success": True,
        "message": "Login successful! Redirecting...",
        "user": {
          "id": user['id'],
          "username": user['username'],
          "email": user['email'],
          "enrolled_courses": user['enrolled_courses']
        }
      })
  return jsonify({"success": False, "message": "Invalid username or password!"})


@app.route('/random3courses')
def random3courses():
  try:
        with open('courses.json', 'r') as f:
            data = json.load(f)  
        randomOnes = random.sample(data, k=3)
        return jsonify(randomOnes)   
  except FileNotFoundError:
        return jsonify({"error": "Courses file not found"}), 404
  

@app.route('/testimonials',methods=['GET'])
def testimonials():
  try:
        with open('testimonials.json', 'r') as f:
            data = json.load(f)  
        randomOnes = random.sample(data, k=2)
        return jsonify(randomOnes)   
  except FileNotFoundError:
        return jsonify({"error": "Testimonials file not found"}), 404
  

@app.route('/enroll/<int:student_id>',methods=['POST'])
def enroll(student_id):
    data = request.get_json()
    course_id = data.get('course_id')
    if not course_id:
      return jsonify({"success": False, "message": "Course ID is missing in the request body."}), 400
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
      return jsonify({"success": False, "message": "Student not found."}), 404
    if course_id in student['enrolled_courses']:
      return jsonify({"success": False, "message": "Already enrolled in this course."}), 400
    
    student['enrolled_courses'].append(course_id)
    return jsonify({
      "success": True,
      "message": "Enrollment successful!",
      "student_id": student_id,
      "enrolled_courses": student['enrolled_courses']
  }), 200


@app.route('/drop/<int:student_id>',methods=['DELETE'])
def drop(student_id):
  try:
        data = request.get_json()
        course = data.get('course')
        for student in students:
            if student['id'] == student_id:
                if course in student['enrolled_courses']:
                    student['enrolled_courses'].remove(course)
                    return jsonify({"success": True, "message": f"Successfully dropped {course}."}), 200
                return jsonify({"success": False, "message": "Course not found in enrolled courses."}), 404
        return jsonify({"success": False, "message": "Student not found."}), 404
  except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/courses',methods=['GET'])
def courses():
  try:
        with open('courses.json', 'r') as file:
            courses = json.load(file)
        return jsonify({"success": True, "courses": courses}), 200
  except FileNotFoundError:
        return jsonify({"error": "Courses file not found."}), 404
  except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/student_courses/<int:student_id>', methods=['GET'])
def get_student_courses(student_id):
    try:
        for student in students:
            if student['id'] == student_id:
                return jsonify({"success": True, "courses": student['enrolled_courses']}), 200
        return jsonify({"success": False, "message": "Student not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)