#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Календар за студентски асистент
Използва централната база данни
"""

from datetime import datetime, timedelta
from database import Database

class Calendar:
    def __init__(self):
        self.db = Database()
        print("📅 Календар инициализиран")
    
    # Директно използваме database методите
    def add_event(self, title, description, event_date, event_time=None, event_type="general"):
        return self.db.add_event(title, description, event_date, event_time, event_type)
    
    def get_all_events(self):
        return self.db.get_all_events()
    
    def delete_event(self, event_id):
        return self.db.delete_event(event_id)
    
    def get_events_count(self):
        return self.db.get_events_count()
    
    def get_upcoming_events(self, days=7):
        """Връща предстоящи събития за следващите X дни"""
        today = datetime.now().date()
        future_date = today + timedelta(days=days)
        
        all_events = self.get_all_events()
        upcoming_events = []
        
        for event in all_events:
            try:
                event_date = datetime.strptime(event[3], "%d-%m-%Y").date()
                if today <= event_date <= future_date:
                    upcoming_events.append(event)
            except ValueError:
                continue
        
        return upcoming_events
    
    def get_today_events(self):
        """Връща днешните събития"""
        today = datetime.now().strftime("%d-%m-%Y")
        return self.get_events_for_date(today)
    
    def get_events_for_date(self, date_str):
        """Връща всички събития за определена дата"""
        all_events = self.get_all_events()
        events_for_date = [event for event in all_events if event[3] == date_str]
        # Сортираме по време
        events_for_date.sort(key=lambda x: x[4] if x[4] else "")
        return events_for_date
    
    def get_events_by_type(self, event_type):
        """Връща събития по тип"""
        all_events = self.get_all_events()
        return [event for event in all_events if event[5] == event_type]
    
    def get_event_types(self):
        """Връща всички типове събития"""
        return ["general", "exam", "assignment", "lecture", "meeting", "deadline", "birthday", "reminder"]
    
    def format_event_text(self, event):
        """Форматира събитието за показване"""
        event_id, title, description, event_date, event_time, event_type, created_date = event
        
        # Форматираме датата
        try:
            date_obj = datetime.strptime(event_date, "%d-%m-%Y")
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except:
            formatted_date = event_date
        
        # Добавяме време ако има
        time_info = f" в {event_time}" if event_time else ""
        
        # Емоджи според типа
        type_emoji = {
            "exam": "📝", "assignment": "📋", "lecture": "🎓", "meeting": "👥",
            "deadline": "⏰", "birthday": "🎂", "reminder": "🔔", "general": "📅"
        }
        
        emoji = type_emoji.get(event_type, "📅")
        text = f"{emoji} {title} - {formatted_date}{time_info}"
        
        if description:
            text += f" ({description})"
        
        return text 