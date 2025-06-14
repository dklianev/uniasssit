#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Централна база данни за студентски асистент
Управлява всички данни: бележки, оценки, събития
"""

import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="assistant.db"):
        self.db_name = db_name
        self.init_database()
    
    def _execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Помощен метод за изпълнение на заявки"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
            
            conn.commit()
            return result
        finally:
            conn.close()
    
    def init_database(self):
        """Създава всички необходими таблици"""
        queries = [
            '''CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_date TEXT NOT NULL
            )''',
            
            '''CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                credits INTEGER DEFAULT 3,
                professor TEXT,
                semester TEXT,
                created_date TEXT NOT NULL
            )''',
            
            '''CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                grade REAL NOT NULL,
                max_grade REAL DEFAULT 6.0,
                exam_type TEXT DEFAULT 'test',
                description TEXT,
                exam_date TEXT,
                created_date TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                event_date TEXT NOT NULL,
                event_time TEXT,
                event_type TEXT DEFAULT 'general',
                created_date TEXT NOT NULL
            )'''
        ]
        
        for query in queries:
            self._execute_query(query)
        
        print("✅ Централна база данни инициализирана")
    
    # ===================
    # МЕТОДИ ЗА БЕЛЕЖКИ
    # ===================
    
    def add_note(self, title, content):
        """Добавя нова бележка"""
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        query = 'INSERT INTO notes (title, content, created_date) VALUES (?, ?, ?)'
        note_id = self._execute_query(query, (title, content, current_time))
        print(f"✅ Бележка '{title}' добавена с ID: {note_id}")
        return note_id
    
    def get_all_notes(self):
        """Връща всички бележки"""
        return self._execute_query('SELECT * FROM notes ORDER BY created_date DESC', fetch_all=True)
    
    def get_note_by_id(self, note_id):
        """Връща бележка по ID"""
        return self._execute_query('SELECT * FROM notes WHERE id = ?', (note_id,), fetch_one=True)
    
    def delete_note(self, note_id):
        """Изтрива бележка"""
        query = 'DELETE FROM notes WHERE id = ?'
        self._execute_query(query, (note_id,))
        print(f"✅ Бележка с ID {note_id} изтрита")
        return True
    
    def get_notes_count(self):
        """Връща броя на бележките"""
        return self._execute_query('SELECT COUNT(*) FROM notes', fetch_one=True)[0]
    
    # ===================
    # МЕТОДИ ЗА ОЦЕНКИ И ПРЕДМЕТИ
    # ===================
    
    def add_subject(self, name, credits=3, professor="", semester=""):
        """Добавя нов предмет"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        query = 'INSERT INTO subjects (name, credits, professor, semester, created_date) VALUES (?, ?, ?, ?, ?)'
        
        try:
            subject_id = self._execute_query(query, (name, credits, professor, semester, current_time))
            print(f"✅ Предмет '{name}' добавен")
            return subject_id
        except sqlite3.IntegrityError:
            print(f"❌ Предмет '{name}' вече съществува")
            return None
    
    def add_grade(self, subject_id, grade, exam_type="test", description="", exam_date=""):
        """Добавя нова оценка"""
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        if not exam_date:
            exam_date = datetime.now().strftime("%d-%m-%Y")
        
        max_grade = 6.0
        query = '''INSERT INTO grades (subject_id, grade, max_grade, exam_type, description, exam_date, created_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        
        grade_id = self._execute_query(query, (subject_id, grade, max_grade, exam_type, description, exam_date, current_time))
        print(f"✅ Оценка {grade}/6.0 добавена")
        return grade_id
    
    def get_all_subjects(self):
        """Връща всички предмети"""
        return self._execute_query('SELECT * FROM subjects ORDER BY name', fetch_all=True)
    
    def get_subject_grades(self, subject_id):
        """Връща всички оценки за предмет"""
        query = 'SELECT * FROM grades WHERE subject_id = ? ORDER BY exam_date DESC'
        return self._execute_query(query, (subject_id,), fetch_all=True)
    
    def delete_subject(self, subject_id):
        """Изтрива предмет и всичките му оценки"""
        # Първо изтриваме оценките
        self._execute_query('DELETE FROM grades WHERE subject_id = ?', (subject_id,))
        # После изтриваме предмета
        self._execute_query('DELETE FROM subjects WHERE id = ?', (subject_id,))
        print(f"✅ Предмет и оценки изтрити")
        return True
    
    def delete_grade(self, grade_id):
        """Изтрива отделна оценка по ID"""
        self._execute_query('DELETE FROM grades WHERE id = ?', (grade_id,))
        print(f"✅ Оценка с ID {grade_id} изтрита")
        return True
    
    # ===================
    # МЕТОДИ ЗА СЪБИТИЯ
    # ===================
    
    def add_event(self, title, description, event_date, event_time=None, event_type="general"):
        """Добавя ново събитие"""
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        query = '''INSERT INTO events (title, description, event_date, event_time, event_type, created_date)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        
        event_id = self._execute_query(query, (title, description, event_date, event_time, event_type, current_time))
        print(f"✅ Събитие '{title}' добавено")
        return event_id
    
    def get_all_events(self):
        """Връща всички събития, сортирани по дата"""
        query = '''SELECT * FROM events 
                   ORDER BY 
                   CASE 
                       WHEN substr(event_date,7,4) || '-' || substr(event_date,4,2) || '-' || substr(event_date,1,2) >= date('now') 
                       THEN substr(event_date,7,4) || '-' || substr(event_date,4,2) || '-' || substr(event_date,1,2)
                       ELSE '9999-12-31'
                   END,
                   event_time'''
        
        return self._execute_query(query, fetch_all=True)
    
    def delete_event(self, event_id):
        """Изтрива събитие"""
        self._execute_query('DELETE FROM events WHERE id = ?', (event_id,))
        print(f"✅ Събитие изтрито")
        return True
    
    def get_events_count(self):
        """Връща броя на събитията"""
        return self._execute_query('SELECT COUNT(*) FROM events', fetch_one=True)[0]
    
    # ===================
    # ОБЩИ СТАТИСТИКИ
    # ===================
    
    def get_all_statistics(self):
        """Връща общи статистики"""
        return {
            'notes_count': self.get_notes_count(),
            'events_count': self.get_events_count(),
            'subjects_count': len(self.get_all_subjects()),
            'grades_count': self._get_grades_count()
        }
    
    def _get_grades_count(self):
        """Връща общия брой оценки"""
        return self._execute_query('SELECT COUNT(*) FROM grades', fetch_one=True)[0] 