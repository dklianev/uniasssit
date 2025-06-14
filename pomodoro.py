#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomodoro таймер
Базова функционалност за продуктивност
"""

import time
import threading
from datetime import datetime

class PomodoroTimer:
    def __init__(self):
        self.work_minutes = 25
        self.break_minutes = 5
        
        self.is_running = False
        self.is_paused = False
        self.current_session = None  # 'work' или 'break'
        self.remaining_seconds = 0
        self.sessions_completed = 0
        
        print("🍅 Pomodoro таймер готов!")
    
    def start_session(self, session_type):
        """Общ метод за стартиране на сесия"""
        if self.is_running:
            print("⚠️ Таймерът вече работи!")
            return False
        
        self.current_session = session_type
        self.is_paused = False
        minutes = self.work_minutes if session_type == 'work' else self.break_minutes
        self.remaining_seconds = minutes * 60
        self.is_running = True
        
        session_name = "работна сесия" if session_type == 'work' else "почивка"
        print(f"{'🎯' if session_type == 'work' else '☕'} Започвам {session_name}: {minutes} минути")
        self._start_timer()
        return True
    
    def start_work_session(self):
        """Започва работна сесия от 25 минути"""
        return self.start_session('work')
    
    def start_break_session(self):
        """Започва почивка от 5 минути"""
        return self.start_session('break')
    
    def pause_timer(self):
        """Превключва пауза/продължи"""
        self.is_paused = not self.is_paused
        print("⏸️ Пауза" if self.is_paused else "▶️ Продължавам")
    
    def stop_timer(self):
        """Спира таймера"""
        if self.is_running:
            self.is_running = False
            self.is_paused = False
            print("⏹️ Таймерът е спрян")
            return True
        else:
            print("⚠️ Таймерът не работи")
            return False
    
    def _start_timer(self):
        """Вътрешен метод за стартиране на таймера"""
        def timer_thread():
            while self.is_running and self.remaining_seconds > 0:
                if not self.is_paused:
                    time.sleep(1)
                    self.remaining_seconds -= 1
                    
                    # Показваме прогреса на всеки 5 минути
                    if self.remaining_seconds % 300 == 0 and self.remaining_seconds > 0:
                        minutes_left = self.remaining_seconds // 60
                        print(f"⏰ Остават {minutes_left} минути...")
                else:
                    time.sleep(0.1)  # Проверяваме за unpause по-често
            
            # Таймерът приключи
            if self.is_running:
                self._session_completed()
        
        # Стартираме в отделен thread
        thread = threading.Thread(target=timer_thread, daemon=True)
        thread.start()
    
    def _session_completed(self):
        """Обработва завършването на сесия"""
        self.is_running = False
        self.is_paused = False
        
        if self.current_session == 'work':
            self.sessions_completed += 1
            print(f"🎉 Работната сесия приключи! Общо сесии: {self.sessions_completed}")
            print("💡 Препоръка: Започнете почивка от 5 минути")
        else:
            print("✅ Почивката приключи!")
            print("💡 Препоръка: Започнете нова работна сесия")
        
        print("\a")  # Звуков сигнал
        self.current_session = None
    
    def get_status(self):
        """Връща текущия статус на таймера"""
        if not self.is_running:
            return {
                'status': 'stopped',
                'message': 'Таймерът не работи',
                'sessions_completed': self.sessions_completed
            }
        
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_left = f"{minutes:02d}:{seconds:02d}"
        
        session_type = "Работа" if self.current_session == 'work' else "Почивка"
        
        if self.is_paused:
            message = f"{session_type}: ПАУЗА - {time_left}"
        else:
            message = f"{session_type}: {time_left}"
        
        return {
            'status': 'running',
            'session_type': session_type,
            'time_left': time_left,
            'remaining_seconds': self.remaining_seconds,
            'sessions_completed': self.sessions_completed,
            'message': message,
            'is_paused': self.is_paused
        }
    
    def get_statistics(self):
        """Връща статистики"""
        return {
            'sessions_completed': self.sessions_completed,
            'total_work_minutes': self.sessions_completed * self.work_minutes,
            'work_session_length': self.work_minutes,
            'break_length': self.break_minutes
        } 