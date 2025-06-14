#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система за оценки
Използва централната база данни
"""

from datetime import datetime
from database import Database

class GradeTracker:
    def __init__(self):
        self.db = Database()
        print("📊 Система за оценки инициализирана")
    
    # Директно използваме database методите
    def add_subject(self, name, credits=3, professor="", semester=""):
        return self.db.add_subject(name, credits, professor, semester)
    
    def add_grade(self, subject_id, grade, exam_type="test", description="", exam_date=""):
        """Добавя нова оценка (винаги в скала до 6.0)"""
        return self.db.add_grade(subject_id, grade, exam_type, description, exam_date)
    
    def get_all_subjects(self):
        return self.db.get_all_subjects()
    
    def get_subject_grades(self, subject_id):
        return self.db.get_subject_grades(subject_id)
    
    def delete_subject(self, subject_id):
        return self.db.delete_subject(subject_id)
    
    def delete_grade(self, grade_id):
        """Изтрива оценка по ID"""
        return self.db.delete_grade(grade_id)
    
    def calculate_subject_average(self, subject_id):
        """Изчислява средната оценка за предмет"""
        grades = self.get_subject_grades(subject_id)
        
        if not grades:
            return 0.0
        
        # Просто средно аритметично - всички оценки са в скала 2-6
        total_grades = sum(grade[2] for grade in grades)
        return round(total_grades / len(grades), 2)
    
    def calculate_average_grade(self):
        """Изчислява общата средна оценка (аритметично средно)"""
        subjects = self.get_all_subjects()
        
        if not subjects:
            return 0.0
        
        subject_averages = [self.calculate_subject_average(subject[0]) for subject in subjects]
        valid_averages = [avg for avg in subject_averages if avg > 0]
        
        return round(sum(valid_averages) / len(valid_averages), 2) if valid_averages else 0.0
    

    
    def get_exam_types(self):
        """Връща всички типове изпити"""
        return ["test", "exam", "quiz", "homework", "project", "presentation", "lab", "seminar", "coursework"]
    
    def get_statistics(self):
        """Връща статистики за оценките"""
        subjects = self.get_all_subjects()
        total_grades = sum(len(self.get_subject_grades(s[0])) for s in subjects)
        
        return {
            'total_subjects': len(subjects),
            'total_grades': total_grades,
            'average_grade': self.calculate_average_grade(),
            'subjects_with_grades': len([s for s in subjects if len(self.get_subject_grades(s[0])) > 0])
        }
    
    def format_grade_text(self, grade, subject_name=None):
        """Форматира оценката за показване"""
        grade_id, subject_id, grade_value, max_grade, exam_type, description, exam_date, created_date = grade
        
        # Форматираме датата
        try:
            date_obj = datetime.strptime(exam_date, "%d-%m-%Y")
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except:
            formatted_date = exam_date
        
        # Просто показваме оценката - без излишно нормализиране
        grade_text = f"{grade_value:.1f}"
        
        if description:
            return f"{grade_text} - {description} ({formatted_date})"
        else:
            return f"{grade_text} ({formatted_date})" 