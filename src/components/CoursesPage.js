import React, { useState, useEffect } from 'react';
import Header from './Header';
import Footer from './Footer';
import CourseItem from './CourseItem';
import EnrollmentList from './EnrollmentList';
import courses from '../backend/courses';
import { useAuth } from '../context/AuthContext'; 

const CoursesPage = () => {
  const { isLoggedIn, user } = useAuth();
  const studentId = user?.id;

  const [enrolledCourses, setEnrolledCourses] = useState(() => {
    const saved = localStorage.getItem('enrollments');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('enrollments', JSON.stringify(enrolledCourses));
  }, [enrolledCourses]);

  const handleEnroll = async (course) => {
    if (!isLoggedIn) {
      alert('You must log in before enrolling in a course.');
      return;
    }
    try {
      const response = await fetch(`http://127.0.0.1:5000/enroll/${studentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ course_id: course.id })
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Enrollment failed.');
      }

      setEnrolledCourses((prev) => [
        ...prev,
        { 
          ...course,
          enrollmentId: Date.now() 
        }
      ]);

      console.log(data.message);
    } catch (error) {
      console.error('Error enrolling:', error);
      alert(`Error enrolling: ${error.message}`);
    }
  };

  const handleRemove = async (enrollmentId, courseId) => {
    if (!isLoggedIn) {
      alert('You must log in before dropping a course.');
      return;
    }
  
    try {
      const response = await fetch(`http://127.0.0.1:5000/drop/${studentId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ course: courseId })
      });
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.message || 'Drop failed.');
      }
  
      setEnrolledCourses((prev) =>
        prev.filter((course) => course.enrollmentId !== enrollmentId)
      );
  
      console.log(data.message);
    } catch (error) {
      console.error('Error dropping course:', error);
      alert(`Error dropping course: ${error.message}`);
    }
  };
  
  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column' 
    }}>
      <Header />
      
      <div style={{ 
        flex: 1,
        display: 'flex',
        padding: '20px',
        gap: '30px'
      }}>
        <div style={{ flex: 3 }}>
          <h2 style={{ color: '#004080' }}>Available Courses</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '20px'
          }}>
            {courses.map(course => (
              <CourseItem 
                key={course.id} 
                course={course} 
                onEnroll={handleEnroll}
              />
            ))}
          </div>
        </div>
        
        <EnrollmentList 
          enrolledCourses={enrolledCourses}
          onRemove={handleRemove}
        />
      </div>

      <Footer />
    </div>
  );
};

export default CoursesPage;
