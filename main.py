#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 Студентски Асистент
Университетски проект 

Функционалности:
- Поздрав според часа от деня
- AI чат с локален LLM модел (Ollama)
- Бележки (добавяне, преглед, изтриване)
- Pomodoro таймер
- SQLite база данни

📋 СТРУКТУРА НА ФАЙЛА:
1. Импорти
2. Основен клас StudentAssistant
3. __init__ и базови методи
4. HOME TAB + методи
5. AI CHAT TAB + методи  
6. NOTES TAB + методи
7. POMODORO TAB + методи
8. CALENDAR TAB + методи
9. GRADES TAB + методи
10. Dialog класове
11. Главно приложение
"""

import wx
import wx.adv
import threading
from datetime import datetime
import random
import time

# Импортираме нашите модули
from database import Database
from ollama import OllamaClient
from pomodoro import PomodoroTimer
from events import Calendar
from grades import GradeTracker

class StudentAssistant(wx.Frame):
    # ============================================================================
    # 🏗️ ИНИЦИАЛИЗАЦИЯ И БАЗОВИ МЕТОДИ
    # ============================================================================
    
    def __init__(self):
        super().__init__(None, title="🎓 Студентски Асистент", size=(800, 600))
        
        # Инициализираме компонентите
        self.db = Database()
        self.ai = OllamaClient()
        self.pomodoro = PomodoroTimer()
        self.calendar = Calendar()
        self.grades = GradeTracker()
        
        # Създаваме интерфейса
        self.create_ui()
        self.Center()
        
        # Показваме поздрав
        self.show_greeting()
        
        print("🎓 Студентски асистент стартиран успешно!")
    
    def create_ui(self):
        """Създава потребителския интерфейс"""
        # Главен панел
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Заглавие
        title = wx.StaticText(panel, label="🎓 Студентски Асистент")
        title_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(50, 100, 200))
        
        # Поздрав и време
        self.greeting_label = wx.StaticText(panel, label=self.get_greeting())
        greeting_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.greeting_label.SetFont(greeting_font)
        
        # Notebook за таб страници
        self.notebook = wx.Notebook(panel)
        
        # Създаваме табовете
        self.create_home_tab()
        self.create_chat_tab()
        self.create_notes_tab()
        self.create_pomodoro_tab()
        self.create_calendar_tab()
        self.create_grades_tab()
        
        # Layout
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        main_sizer.Add(self.greeting_label, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)
        
        panel.SetSizer(main_sizer)
    
    def get_greeting(self):
        """Връща поздрав според часа от деня"""
        hour = datetime.now().hour
        current_time = datetime.now().strftime("%H:%M - %d.%m.%Y")
        
        if hour < 12:
            greeting = "☀️ Добро утро!"
        elif hour < 18:
            greeting = "🌤️ Добър ден!"
        else:
            greeting = "🌙 Добър вечер!"
        
        return f"{greeting} | {current_time}"
    
    def show_greeting(self):
        """Показва поздрав в конзолата"""
        hour = datetime.now().hour
        if hour < 12:
            print("☀️ Добро утро! Готов съм да ти помогна днес!")
        elif hour < 18:
            print("🌤️ Добър ден! Как минава денят ти?")
        else:
            print("🌙 Добър вечер! Време е за учене!")

    # ============================================================================
    # 🏠 HOME TAB - Начална страница
    # ============================================================================
    
    def create_home_tab(self):
        """Създава началната страница"""
        home_panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Дневен цитат
        quotes = [
            "💪 Успехът е сбор от малки усилия, повтаряни ден след ден.",
            "🎯 Единственият начин да свършиш работа е да започнеш.",
            "📚 Знанието е сила, но прилагането му е мъдрост.",
            "🌟 Бъди промяната, която искаш да видиш в света.",
            "🚀 Не чакай възможността - създай я!"
        ]
        
        daily_quote = random.choice(quotes)
        quote_label = wx.StaticText(home_panel, label=f"Цитат на деня:\n{daily_quote}")
        quote_label.SetForegroundColour(wx.Colour(100, 100, 200))
        
        # Статистики
        notes_count = self.db.get_notes_count()
        pomodoro_stats = self.pomodoro.get_statistics()
        events_count = self.calendar.get_events_count()
        grade_stats = self.grades.get_statistics()
        
        stats_text = f"""
📊 Твоите статистики:
• 📝 Бележки: {notes_count}
• 🍅 Pomodoro сесии: {pomodoro_stats['sessions_completed']} 
• ⏰ Работно време: {pomodoro_stats['total_work_minutes']} мин
• 📅 Събития: {events_count}
• 📚 Предмети: {grade_stats['total_subjects']}
• 🎯 Средна оценка: {grade_stats['average_grade']:.2f}
        """
        
        stats_label = wx.StaticText(home_panel, label=stats_text)
        
        # Бързи действия
        actions_box = wx.StaticBox(home_panel, label="Бързи действия")
        actions_sizer = wx.StaticBoxSizer(actions_box, wx.HORIZONTAL)
        
        new_note_btn = wx.Button(home_panel, label="📝 Нова бележка")
        start_work_btn = wx.Button(home_panel, label="🍅 Помодоро")
        
        new_note_btn.Bind(wx.EVT_BUTTON, lambda e: self.notebook.SetSelection(2))
        start_work_btn.Bind(wx.EVT_BUTTON, lambda e: self.notebook.SetSelection(3))
        
        actions_sizer.Add(new_note_btn, 0, wx.ALL, 5)
        actions_sizer.Add(start_work_btn, 0, wx.ALL, 5)
        
        # Layout
        sizer.Add(quote_label, 0, wx.ALL | wx.CENTER, 20)
        sizer.Add(wx.StaticLine(home_panel), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(stats_label, 0, wx.ALL, 20)
        sizer.Add(actions_sizer, 0, wx.ALL | wx.CENTER, 20)
        
        home_panel.SetSizer(sizer)
        self.notebook.AddPage(home_panel, "🏠 Начало")
    
    # ============================================================================
    # 💬 AI CHAT TAB - Чат с изкуствен интелект  
    # ============================================================================
    
    def create_chat_tab(self):
        """Създава чат страницата"""
        chat_panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # AI Доставчик
        provider_sizer = wx.BoxSizer(wx.HORIZONTAL)
        provider_label = wx.StaticText(chat_panel, label="AI Модел:")
        self.provider_choice = wx.Choice(chat_panel, choices=["Ollama", "OpenAI"])
        self.provider_choice.SetSelection(0)  # По подразбиране Ollama
        self.provider_choice.Bind(wx.EVT_CHOICE, self.on_provider_change)
        
        provider_sizer.Add(provider_label, 0, wx.ALL | wx.CENTER, 5)
        provider_sizer.Add(self.provider_choice, 0, wx.ALL, 5)
        
        # OpenAI API Key контроли
        self.api_key_label = wx.StaticText(chat_panel, label="OpenAI API ключ:")
        self.api_key_text = wx.TextCtrl(chat_panel, style=wx.TE_PASSWORD)
        self.set_key_btn = wx.Button(chat_panel, label="🔑 Задай")
        self.set_key_btn.Bind(wx.EVT_BUTTON, self.set_openai_key)
        
        # Групираме в sizer
        self.api_key_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.api_key_sizer.Add(self.api_key_label, 0, wx.ALL | wx.CENTER, 5)
        self.api_key_sizer.Add(self.api_key_text, 1, wx.ALL | wx.EXPAND, 5)
        self.api_key_sizer.Add(self.set_key_btn, 0, wx.ALL, 5)
        
        # Скриваме OpenAI контролите първоначално
        self.api_key_label.Hide()
        self.api_key_text.Hide()
        self.set_key_btn.Hide()
        
        # Модели
        model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        model_label = wx.StaticText(chat_panel, label="AI Модел:")
        self.model_choice = wx.Choice(chat_panel)
        refresh_btn = wx.Button(chat_panel, label="🔄 Обнови")
        refresh_btn.Bind(wx.EVT_BUTTON, self.refresh_models)
        
        model_sizer.Add(model_label, 0, wx.ALL | wx.CENTER, 5)
        model_sizer.Add(self.model_choice, 1, wx.ALL | wx.EXPAND, 5)
        model_sizer.Add(refresh_btn, 0, wx.ALL, 5)
        
        # Чат
        self.chat_display = wx.TextCtrl(chat_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        chat_font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.chat_display.SetFont(chat_font)
        
        # Вход за съобщения
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.chat_input = wx.TextCtrl(chat_panel, style=wx.TE_PROCESS_ENTER)
        self.chat_input.Bind(wx.EVT_TEXT_ENTER, self.send_message)
        send_btn = wx.Button(chat_panel, label="📤 Изпрати")
        send_btn.Bind(wx.EVT_BUTTON, self.send_message)
        
        input_sizer.Add(self.chat_input, 1, wx.ALL | wx.EXPAND, 5)
        input_sizer.Add(send_btn, 0, wx.ALL, 5)
        
        # Статус
        self.chat_status = wx.StaticText(chat_panel, label="Готов за чат")
        
        # Layout
        sizer.Add(provider_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.api_key_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(model_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.chat_display, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.chat_status, 0, wx.ALL, 5)
        
        chat_panel.SetSizer(sizer)
        self.notebook.AddPage(chat_panel, "💬 AI Чат")
        
        # Зареждаме моделите
        self.refresh_models()

    # AI CHAT МЕТОДИ
    # --------------------------------------------------------------------------------

    def refresh_models(self, event=None):
        """Обновява списъка с AI модели"""
        models = self.ai.get_available_models()
        
        self.model_choice.Clear()
        if models:
            for model in models:
                self.model_choice.Append(model)
            self.model_choice.SetSelection(0)
            self.ai.set_model(models[0])
            provider = self.provider_choice.GetStringSelection()
            self.chat_status.SetLabel(f"✅ Намерени {len(models)} {provider} модела")
        else:
            self.model_choice.Append("Няма модели")
            self.chat_status.SetLabel("❌ Няма достъпни модели")

    def send_message(self, event):
        """Изпраща съобщение към AI"""
        message = self.chat_input.GetValue().strip()
        if not message:
            return
        
        # Задаваме модела
        if self.model_choice.GetSelection() >= 0:
            model_name = self.model_choice.GetStringSelection()
            if model_name != "Няма модели":
                self.ai.set_model(model_name)
        
        # Показваме съобщението
        self.chat_display.AppendText(f"🧑 Ти: {message}\n\n")
        self.chat_input.SetValue("")
        self.chat_status.SetLabel("🤖 AI мисли...")
        
        # Изпращаме в отделен thread
        def send_thread():
            response = self.ai.chat(message)
            wx.CallAfter(self.on_ai_response, response)
        
        thread = threading.Thread(target=send_thread)
        thread.daemon = True
        thread.start()

    def on_ai_response(self, response):
        """Обработва отговора от AI"""
        self.chat_display.AppendText(f"🤖 AI: {response}\n\n")
        self.chat_status.SetLabel("✅ Готов за нови въпроси")

    def on_provider_change(self, event):
        """Променя AI доставчика"""
        provider = self.provider_choice.GetStringSelection()
        
        if provider == "OpenAI":
            self.ai.set_mode("openai")
            self._show_openai_controls(True)
            if self.api_key_text.GetValue().strip():
                self.ai.set_openai_key_and_mode(self.api_key_text.GetValue().strip())
        else:
            self.ai.set_mode("ollama")
            self._show_openai_controls(False)
        
        self.refresh_models()

    def _show_openai_controls(self, show):
        """Показва/скрива OpenAI контролите"""
        self.api_key_label.Show(show)
        self.api_key_text.Show(show)
        self.set_key_btn.Show(show)
        self.api_key_label.GetParent().Layout()

    def set_openai_key(self, event):
        """Задава OpenAI API ключа"""
        api_key = self.api_key_text.GetValue().strip()
        if not api_key:
            wx.MessageBox("Моля въведете API ключ", "Грешка")
            return
        
        self.ai.set_openai_key_and_mode(api_key)
        self.chat_status.SetLabel("🔑 OpenAI API ключ зададен")
        self.refresh_models()

    # ============================================================================
    # 📝 NOTES TAB - Бележки
    # ============================================================================

    def create_notes_tab(self):
        """Създава страницата с бележки"""
        notes_panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(notes_panel, label="➕ Добави бележка")
        refresh_btn = wx.Button(notes_panel, label="🔄 Обнови")
        delete_btn = wx.Button(notes_panel, label="🗑️ Изтрий")
        
        add_btn.Bind(wx.EVT_BUTTON, self.add_note)
        refresh_btn.Bind(wx.EVT_BUTTON, self.refresh_notes)
        delete_btn.Bind(wx.EVT_BUTTON, self.delete_note)
        
        btn_sizer.Add(add_btn, 0, wx.ALL, 5)
        btn_sizer.Add(refresh_btn, 0, wx.ALL, 5)
        btn_sizer.Add(delete_btn, 0, wx.ALL, 5)
        
        # Списък с бележки
        self.notes_list = wx.ListCtrl(notes_panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.notes_list.AppendColumn("ID", width=50)
        self.notes_list.AppendColumn("Заглавие", width=200)
        self.notes_list.AppendColumn("Създадена", width=150)
        
        # Преглед на бележка
        self.note_view = wx.TextCtrl(notes_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        self.notes_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_note_selected)
        
        # Layout
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        sizer.Add(self.notes_list, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(wx.StaticText(notes_panel, label="Съдържание:"), 0, wx.ALL, 5)
        sizer.Add(self.note_view, 1, wx.EXPAND | wx.ALL, 5)
        
        notes_panel.SetSizer(sizer)
        self.notebook.AddPage(notes_panel, "📝 Бележки")
        
        # Зареждаме бележките
        self.refresh_notes()

    # NOTES МЕТОДИ
    # --------------------------------------------------------------------------------

    def refresh_notes(self, event=None):
        """Обновява списъка с бележки"""
        self.notes_list.DeleteAllItems()
        notes = self.db.get_all_notes()
        
        for note in notes:
            index = self.notes_list.InsertItem(self.notes_list.GetItemCount(), str(note[0]))
            self.notes_list.SetItem(index, 1, note[1])
            self.notes_list.SetItem(index, 2, note[3])

    def add_note(self, event):
        """Добавя нова бележка"""
        dialog = NoteDialog(self, "Нова бележка")
        if dialog.ShowModal() == wx.ID_OK:
            title, content = dialog.get_data()
            if title and content:
                self.db.add_note(title, content)
                self.refresh_notes()
        dialog.Destroy()

    def delete_note(self, event):
        """Изтрива избраната бележка"""
        selected = self.notes_list.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Моля изберете бележка за изтриване", "Информация")
            return
        
        note_id = int(self.notes_list.GetItemText(selected, 0))
        
        if wx.MessageBox("Сигурни ли сте?", "Потвърждение", wx.YES_NO) == wx.YES:
            self.db.delete_note(note_id)
            self.refresh_notes()
            self.note_view.SetValue("")

    def on_note_selected(self, event):
        """Показва съдържанието на избраната бележка"""
        selected = event.GetIndex()
        note_id = int(self.notes_list.GetItemText(selected, 0))
        
        note = self.db.get_note_by_id(note_id)
        if note:
            content = f"Заглавие: {note[1]}\nСъздадена: {note[3]}\n\n{note[2]}"
            self.note_view.SetValue(content)

    # ============================================================================
    # 🍅 POMODORO TAB - Pomodoro техника
    # ============================================================================

    def create_pomodoro_tab(self):
        """Създава Pomodoro страницата"""
        pomodoro_panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Статус
        self.pomodoro_status = wx.StaticText(pomodoro_panel, label="Готов за започване")
        status_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.pomodoro_status.SetFont(status_font)
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.work_btn = wx.Button(pomodoro_panel, label="🎯 Работа (25 мин)")
        self.break_btn = wx.Button(pomodoro_panel, label="☕ Почивка (5 мин)")
        self.pause_btn = wx.Button(pomodoro_panel, label="⏸️ Пауза")
        self.stop_btn = wx.Button(pomodoro_panel, label="⏹️ Стоп")
        
        self.work_btn.Bind(wx.EVT_BUTTON, self.start_work)
        self.break_btn.Bind(wx.EVT_BUTTON, self.start_break)
        self.pause_btn.Bind(wx.EVT_BUTTON, self.pause_pomodoro)
        self.stop_btn.Bind(wx.EVT_BUTTON, self.stop_pomodoro)
        
        btn_sizer.Add(self.work_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.break_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.pause_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.stop_btn, 0, wx.ALL, 5)
        
        # Статистики
        stats = self.pomodoro.get_statistics()
        stats_text = f"""
🍅 Pomodoro статистики:
• Завършени сесии: {stats['sessions_completed']}
• Общо работно време: {stats['total_work_minutes']} минути
• Работна сесия: {stats['work_session_length']} минути
• Почивка: {stats['break_length']} минути
        """
        
        self.pomodoro_stats = wx.StaticText(pomodoro_panel, label=stats_text)
        
        # Layout
        sizer.Add(self.pomodoro_status, 0, wx.ALL | wx.CENTER, 20)
        sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(wx.StaticLine(pomodoro_panel), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.pomodoro_stats, 0, wx.ALL, 20)
        
        pomodoro_panel.SetSizer(sizer)
        self.notebook.AddPage(pomodoro_panel, "🍅 Pomodoro")
        
        # Стартираме обновяването на статуса
        self.start_pomodoro_updates()

    # POMODORO МЕТОДИ
    # --------------------------------------------------------------------------------

    def start_work(self, event):
        """Започва работна сесия"""
        if self.pomodoro.start_work_session():
            self.work_btn.Enable(False)
            self.break_btn.Enable(False)
            self.pause_btn.Enable(True)
            self.stop_btn.Enable(True)

    def start_break(self, event):
        """Започва почивка"""
        if self.pomodoro.start_break_session():
            self.work_btn.Enable(False)
            self.break_btn.Enable(False)
            self.pause_btn.Enable(True)
            self.stop_btn.Enable(True)

    def pause_pomodoro(self, event):
        """Превключва пауза/продължи"""
        self.pomodoro.pause_timer()
        # Текстът на бутона се обновява автоматично от update_pomodoro_display

    def stop_pomodoro(self, event):
        """Спира таймера"""
        self.pomodoro.stop_timer()
        self.work_btn.Enable(True)
        self.break_btn.Enable(True)
        self.pause_btn.Enable(False)
        self.stop_btn.Enable(False)
        self.pomodoro_status.SetLabel("Спрян")
        print("\a")  # Звуков сигнал при спиране

    def start_pomodoro_updates(self):
        """Стартира обновяването на Pomodoro статуса"""
        def update_status():
            while True:
                status = self.pomodoro.get_status()
                wx.CallAfter(self.update_pomodoro_display, status)
                time.sleep(1)
        
        thread = threading.Thread(target=update_status)
        thread.daemon = True
        thread.start()

    def update_pomodoro_display(self, status):
        """Обновява дисплея на Pomodoro"""
        if hasattr(self, 'pomodoro_status'):
            self.pomodoro_status.SetLabel(status['message'])
            
            # Обновяваме текста на pause бутона
            if hasattr(self, 'pause_btn') and status['status'] == 'running':
                if status.get('is_paused', False):
                    self.pause_btn.SetLabel("▶️ Продължи")
                else:
                    self.pause_btn.SetLabel("⏸️ Пауза")
            
            # Обновяваме статистиките
            if status['status'] == 'stopped':
                stats = self.pomodoro.get_statistics()
                stats_text = f"""
🍅 Pomodoro статистики:
• Завършени сесии: {stats['sessions_completed']}
• Общо работно време: {stats['total_work_minutes']} минути
• Работна сесия: {stats['work_session_length']} минути
• Почивка: {stats['break_length']} минути
                """
                self.pomodoro_stats.SetLabel(stats_text)
                
                # Възстановяваме бутоните
                self.work_btn.Enable(True)
                self.break_btn.Enable(True)
                self.pause_btn.Enable(False)
                self.stop_btn.Enable(False)

    # ============================================================================
    # 📅 CALENDAR TAB - Календар със събития
    # ============================================================================

    def create_calendar_tab(self):
        """Създава календарната страница с реален календар"""
        calendar_panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_event_btn = wx.Button(calendar_panel, label="➕ Ново събитие")
        delete_btn = wx.Button(calendar_panel, label="🗑️ Изтрий събитие")
        today_btn = wx.Button(calendar_panel, label="🏠 Днес")
        
        add_event_btn.Bind(wx.EVT_BUTTON, self.add_event)
        delete_btn.Bind(wx.EVT_BUTTON, self.delete_event)
        today_btn.Bind(wx.EVT_BUTTON, self.go_to_today)
        
        btn_sizer.Add(add_event_btn, 0, wx.ALL, 5)
        btn_sizer.Add(delete_btn, 0, wx.ALL, 5)
        btn_sizer.Add(today_btn, 0, wx.ALL, 5)
        
        # Реален календарен контрол
        self.calendar_ctrl = wx.adv.CalendarCtrl(calendar_panel, 
                                                style=wx.adv.CAL_SHOW_HOLIDAYS | 
                                                      wx.adv.CAL_MONDAY_FIRST)
        self.calendar_ctrl.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.on_date_selected)
        
        # Събития за избраната дата
        events_box = wx.StaticBox(calendar_panel, label="Събития за избраната дата")
        events_sizer = wx.StaticBoxSizer(events_box, wx.VERTICAL)
        
        self.selected_date_events = wx.ListCtrl(calendar_panel, 
                                              style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
                                              size=(-1, 150))
        self.selected_date_events.AppendColumn("ID", width=50)
        self.selected_date_events.AppendColumn("Събитие", width=200)
        self.selected_date_events.AppendColumn("Час", width=80)
        self.selected_date_events.AppendColumn("Тип", width=100)
        
        events_sizer.Add(self.selected_date_events, 1, wx.EXPAND | wx.ALL, 5)
        
        # Информация за избраната дата
        self.date_info = wx.StaticText(calendar_panel, label="Изберете дата от календара")
        date_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.date_info.SetFont(date_font)
        self.date_info.SetForegroundColour(wx.Colour(50, 100, 200))
        
        # Layout
        sizer.Add(btn_sizer, 0, wx.ALL, 5)
        sizer.Add(self.date_info, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self.calendar_ctrl, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(events_sizer, 1, wx.EXPAND | wx.ALL, 5)
        
        calendar_panel.SetSizer(sizer)
        self.notebook.AddPage(calendar_panel, "📅 Календар")
        
        # Инициализираме с днешната дата
        self.refresh_calendar_display()

    # CALENDAR МЕТОДИ
    # --------------------------------------------------------------------------------

    def refresh_calendar_display(self):
        """Обновява календарния дисплей"""
        # Обновяваме событията за текущо избраната дата
        selected_date = self.calendar_ctrl.GetDate()
        date_str = selected_date.Format("%d-%m-%Y")
        self.update_date_events(date_str)

    def on_date_selected(self, event):
        """Обработва избиране на дата в календара"""
        selected_date = self.calendar_ctrl.GetDate()
        date_str = selected_date.Format("%d-%m-%Y")
        
        # Обновяваме информацията за датата
        formatted_date = selected_date.Format("%d.%m.%Y")
        weekday = selected_date.GetWeekDayName(selected_date.GetWeekDay())
        self.date_info.SetLabel(f"📅 {weekday}, {formatted_date}")
        
        # Показваме събитията за тази дата
        self.update_date_events(date_str)

    def update_date_events(self, date_str):
        """Обновява списъка със събития за дадена дата"""
        self.selected_date_events.DeleteAllItems()
        
        # Вземаме всички събития и филтрираме по дата
        all_events = self.calendar.get_all_events()
        date_events = [event for event in all_events if event[3] == date_str]
        
        for event_data in date_events:
            index = self.selected_date_events.InsertItem(self.selected_date_events.GetItemCount(), str(event_data[0]))
            self.selected_date_events.SetItem(index, 1, event_data[1])  # title
            self.selected_date_events.SetItem(index, 2, event_data[4] or "")  # time
            self.selected_date_events.SetItem(index, 3, event_data[5])  # type


    def go_to_today(self, event):
        """Отива на днешната дата в календара"""
        today = wx.DateTime.Today()
        self.calendar_ctrl.SetDate(today)
        self.on_date_selected(None)  # Обновяваме дисплея

    def add_event(self, event):
        """Добавя ново събитие"""
        # Попълваме подразбиращата се дата с избраната от календара
        selected_date = self.calendar_ctrl.GetDate()
        default_date = selected_date.Format("%d-%m-%Y")
        
        dialog = EventDialog(self, "Ново събитие", default_date)
        if dialog.ShowModal() == wx.ID_OK:
            title, description, date, time, event_type = dialog.get_data()
            self.calendar.add_event(title, description, date, time, event_type)
            self.refresh_calendar_display()
        dialog.Destroy()

    def delete_event(self, event):
        """Изтрива избраното събитие"""
        selected = self.selected_date_events.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Моля изберете събитие за изтриване от списъка", "Информация")
            return
        
        event_id = int(self.selected_date_events.GetItemText(selected, 0))
        event_title = self.selected_date_events.GetItemText(selected, 1)
        
        if wx.MessageBox(f"Сигурни ли сте, че искате да изтриете '{event_title}'?", 
                        "Потвърждение", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.calendar.delete_event(event_id)
            self.refresh_calendar_display()

    # ============================================================================
    # 📚 GRADES TAB - Система за оценки
    # ============================================================================

    def create_grades_tab(self):
        """Създава страницата за оценки"""
        grades_panel = wx.Panel(self.notebook)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Разделяме на горна и долна част
        splitter = wx.SplitterWindow(grades_panel, style=wx.SP_3D)
        
        # Горна част - Предмети
        subjects_panel = wx.Panel(splitter)
        subjects_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Бутони за предмети
        subjects_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_subject_btn = wx.Button(subjects_panel, label="➕ Предмет")
        delete_subject_btn = wx.Button(subjects_panel, label="🗑️ Изтрий предмет")
        
        add_subject_btn.Bind(wx.EVT_BUTTON, self.add_subject)
        delete_subject_btn.Bind(wx.EVT_BUTTON, self.delete_subject)
        
        subjects_btn_sizer.Add(add_subject_btn, 0, wx.ALL, 5)
        subjects_btn_sizer.Add(delete_subject_btn, 0, wx.ALL, 5)
        
        # Списък с предмети
        self.subjects_list = wx.ListCtrl(subjects_panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.subjects_list.AppendColumn("ID", width=50)
        self.subjects_list.AppendColumn("Предмет", width=200)
        self.subjects_list.AppendColumn("Кредити", width=80)
        self.subjects_list.AppendColumn("Преподавател", width=150)
        self.subjects_list.AppendColumn("Средна оценка", width=100)
        
        self.subjects_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_subject_selected)
        
        subjects_sizer.Add(subjects_btn_sizer, 0, wx.ALL, 5)
        subjects_sizer.Add(self.subjects_list, 1, wx.EXPAND | wx.ALL, 5)
        subjects_panel.SetSizer(subjects_sizer)
        
        # Долна част - Оценки
        grades_panel_lower = wx.Panel(splitter)
        grades_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Бутони за оценки
        grades_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_grade_btn = wx.Button(grades_panel_lower, label="➕ Оценка")
        delete_grade_btn = wx.Button(grades_panel_lower, label="🗑️ Изтрий оценка")
        
        add_grade_btn.Bind(wx.EVT_BUTTON, self.add_grade)
        delete_grade_btn.Bind(wx.EVT_BUTTON, self.delete_grade)
        
        grades_btn_sizer.Add(add_grade_btn, 0, wx.ALL, 5)
        grades_btn_sizer.Add(delete_grade_btn, 0, wx.ALL, 5)
        
        # Списък с оценки
        self.grades_list = wx.ListCtrl(grades_panel_lower, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.grades_list.AppendColumn("ID", width=50)
        self.grades_list.AppendColumn("Оценка", width=80)
        self.grades_list.AppendColumn("Макс", width=60)
        self.grades_list.AppendColumn("Тип", width=100)
        self.grades_list.AppendColumn("Описание", width=150)
        self.grades_list.AppendColumn("Дата", width=100)
        
        # Средна оценка статистика
        self.gpa_label = wx.StaticText(grades_panel_lower, label="Средна оценка: 0.00")
        gpa_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.gpa_label.SetFont(gpa_font)
        self.gpa_label.SetForegroundColour(wx.Colour(50, 150, 50))
        
        grades_sizer.Add(grades_btn_sizer, 0, wx.ALL, 5)
        grades_sizer.Add(self.grades_list, 1, wx.EXPAND | wx.ALL, 5)
        grades_sizer.Add(self.gpa_label, 0, wx.ALL | wx.CENTER, 10)
        grades_panel_lower.SetSizer(grades_sizer)
        
        # Splitter setup
        splitter.SplitHorizontally(subjects_panel, grades_panel_lower)
        splitter.SetSashGravity(0.5)
        
        main_sizer.Add(splitter, 1, wx.EXPAND | wx.ALL, 5)
        grades_panel.SetSizer(main_sizer)
        self.notebook.AddPage(grades_panel, "📊 Оценки")
        
        # Зареждаме данните
        self.refresh_subjects()
        self.update_average_display()

    # GRADES МЕТОДИ
    # --------------------------------------------------------------------------------

    def refresh_subjects(self, event=None):
        """Обновява списъка с предмети"""
        self.subjects_list.DeleteAllItems()
        subjects = self.grades.get_all_subjects()
        
        for subject in subjects:
            index = self.subjects_list.InsertItem(self.subjects_list.GetItemCount(), str(subject[0]))
            self.subjects_list.SetItem(index, 1, subject[1])  # name
            self.subjects_list.SetItem(index, 2, str(subject[2]))  # credits
            self.subjects_list.SetItem(index, 3, subject[3] or "")  # professor
            
            # Изчисляваме средната оценка
            avg = self.grades.calculate_subject_average(subject[0])
            self.subjects_list.SetItem(index, 4, f"{avg:.2f}")

    def add_subject(self, event):
        """Добавя нов предмет"""
        dialog = SubjectDialog(self, "Нов предмет")
        if dialog.ShowModal() == wx.ID_OK:
            name, credits, professor, semester = dialog.get_data()
            if name:
                self.grades.add_subject(name, credits, professor, semester)
                self.refresh_subjects()
                self.update_average_display()
        dialog.Destroy()

    def delete_subject(self, event):
        """Изтрива избрания предмет"""
        selected = self.subjects_list.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Моля изберете предмет за изтриване", "Информация")
            return
        
        subject_id = int(self.subjects_list.GetItemText(selected, 0))
        
        if wx.MessageBox("Това ще изтрие и всички оценки за предмета!\nСигурни ли сте?", "Потвърждение", wx.YES_NO) == wx.YES:
            self.grades.delete_subject(subject_id)
            self.refresh_subjects()
            self.refresh_grades()
            self.update_average_display()

    def on_subject_selected(self, event):
        """Показва оценките за избрания предмет"""
        selected = event.GetIndex()
        subject_id = int(self.subjects_list.GetItemText(selected, 0))
        self.refresh_grades(subject_id)

    def refresh_grades(self, subject_id=None):
        """Обновява списъка с оценки"""
        self.grades_list.DeleteAllItems()
        
        if subject_id:
            grades = self.grades.get_subject_grades(subject_id)
        else:
            # Показваме всички оценки
            grades = []
            subjects = self.grades.get_all_subjects()
            for subject in subjects:
                grades.extend(self.grades.get_subject_grades(subject[0]))
        
        for grade in grades:
            index = self.grades_list.InsertItem(self.grades_list.GetItemCount(), str(grade[0]))
            self.grades_list.SetItem(index, 1, f"{grade[2]:.1f}")  # grade
            self.grades_list.SetItem(index, 2, f"{grade[3]:.1f}")  # max_grade
            self.grades_list.SetItem(index, 3, grade[4])  # exam_type
            self.grades_list.SetItem(index, 4, grade[5] or "")  # description
            self.grades_list.SetItem(index, 5, grade[6])  # exam_date

    def add_grade(self, event):
        """Добавя нова оценка"""
        # Проверяваме дали има избран предмет
        selected = self.subjects_list.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Моля първо изберете предмет", "Информация")
            return
        
        subject_id = int(self.subjects_list.GetItemText(selected, 0))
        
        dialog = GradeDialog(self, "Нова оценка")
        if dialog.ShowModal() == wx.ID_OK:
            grade, exam_type, description, exam_date = dialog.get_data()
            if grade is not None:
                self.grades.add_grade(subject_id, grade, exam_type, description, exam_date)
                self.refresh_grades(subject_id)
                self.refresh_subjects()
                self.update_average_display()
        dialog.Destroy()

    def delete_grade(self, event):
        """Изтрива избраната оценка"""
        selected = self.grades_list.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Моля изберете оценка за изтриване", "Информация")
            return
        
        grade_id = int(self.grades_list.GetItemText(selected, 0))
        
        if wx.MessageBox("Сигурни ли сте?", "Потвърждение", wx.YES_NO) == wx.YES:
            self.grades.delete_grade(grade_id)
            # Обновяваме текущите оценки
            subject_selected = self.subjects_list.GetFirstSelected()
            if subject_selected != -1:
                subject_id = int(self.subjects_list.GetItemText(subject_selected, 0))
                self.refresh_grades(subject_id)
            self.refresh_subjects()
            self.update_average_display()

    def update_average_display(self):
        """Обновява показаната средна оценка"""
        average = self.grades.calculate_average_grade()
        self.gpa_label.SetLabel(f"Средна оценка: {average:.2f}")


# ============================================================================
# 🪟 DIALOG КЛАСОВЕ - Диалогови прозорци
# ============================================================================

class EventDialog(wx.Dialog):
    """Диалог за добавяне на събитие"""
    def __init__(self, parent, title, default_date=None):
        super().__init__(parent, title=title, size=(550, 450))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Заглавие
        title_label = wx.StaticText(panel, label="Заглавие:")
        self.title_ctrl = wx.TextCtrl(panel)
        
        # Описание
        desc_label = wx.StaticText(panel, label="Описание:")
        self.desc_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 60))
        
        # Дата
        date_label = wx.StaticText(panel, label="Дата (DD-MM-YYYY):")
        date_value = default_date if default_date else datetime.now().strftime("%d-%m-%Y")
        self.date_ctrl = wx.TextCtrl(panel, value=date_value)
        
        # Час
        time_label = wx.StaticText(panel, label="Час (HH:MM) - незадължително:")
        self.time_ctrl = wx.TextCtrl(panel)
        
        # Тип
        type_label = wx.StaticText(panel, label="Тип:")
        self.type_choice = wx.Choice(panel)
        types = ["general", "exam", "assignment", "lecture", "meeting", "deadline", "birthday", "reminder"]
        for t in types:
            self.type_choice.Append(t)
        self.type_choice.SetSelection(0)
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, wx.ID_OK, "Запиши")
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "Отказ")
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        
        # Layout
        sizer.Add(title_label, 0, wx.ALL, 5)
        sizer.Add(self.title_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(desc_label, 0, wx.ALL, 5)
        sizer.Add(self.desc_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(date_label, 0, wx.ALL, 5)
        sizer.Add(self.date_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(time_label, 0, wx.ALL, 5)
        sizer.Add(self.time_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(type_label, 0, wx.ALL, 5)
        sizer.Add(self.type_choice, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        panel.SetSizer(sizer)
        self.Center()
    
    def get_data(self):
        return (
            self.title_ctrl.GetValue(),
            self.desc_ctrl.GetValue(),
            self.date_ctrl.GetValue(),
            self.time_ctrl.GetValue() if self.time_ctrl.GetValue() else None,
            self.type_choice.GetStringSelection()
        )


class SubjectDialog(wx.Dialog):
    """Диалог за добавяне на предмет"""
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(500, 350))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Име
        name_label = wx.StaticText(panel, label="Име на предмет:")
        self.name_ctrl = wx.TextCtrl(panel)
        
        # Кредити
        credits_label = wx.StaticText(panel, label="Кредити:")
        self.credits_ctrl = wx.SpinCtrl(panel, value="3", min=1, max=10)
        
        # Преподавател
        prof_label = wx.StaticText(panel, label="Преподавател:")
        self.prof_ctrl = wx.TextCtrl(panel)
        
        # Семестър
        sem_label = wx.StaticText(panel, label="Семестър:")
        self.sem_ctrl = wx.TextCtrl(panel)
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, wx.ID_OK, "Запиши")
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "Отказ")
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        
        # Layout
        sizer.Add(name_label, 0, wx.ALL, 5)
        sizer.Add(self.name_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(credits_label, 0, wx.ALL, 5)
        sizer.Add(self.credits_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(prof_label, 0, wx.ALL, 5)
        sizer.Add(self.prof_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sem_label, 0, wx.ALL, 5)
        sizer.Add(self.sem_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        self.Center()
    
    def get_data(self):
        return (
            self.name_ctrl.GetValue(),
            self.credits_ctrl.GetValue(),
            self.prof_ctrl.GetValue(),
            self.sem_ctrl.GetValue()
        )


class GradeDialog(wx.Dialog):
    """Диалог за добавяне на оценка"""
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(500, 450))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Оценка
        grade_label = wx.StaticText(panel, label="Оценка:")
        self.grade_ctrl = wx.SpinCtrlDouble(panel, value="5.0", min=2.0, max=6.0, inc=0.1)
        
        # Максимална оценка винаги е 6.0
        max_info = wx.StaticText(panel, label="Максимална оценка: 6.0")
        
        # Тип изпит
        type_label = wx.StaticText(panel, label="Тип изпит:")
        self.type_choice = wx.Choice(panel)
        types = ["test", "exam", "homework", "project", "quiz", "presentation", "lab", "final"]
        for t in types:
            self.type_choice.Append(t)
        self.type_choice.SetSelection(0)
        
        # Описание
        desc_label = wx.StaticText(panel, label="Описание:")
        self.desc_ctrl = wx.TextCtrl(panel)
        
        # Дата
        date_label = wx.StaticText(panel, label="Дата (DD-MM-YYYY):")
        self.date_ctrl = wx.TextCtrl(panel, value=datetime.now().strftime("%d-%m-%Y"))
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, wx.ID_OK, "Запиши")
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "Отказ")
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        
        # Layout
        sizer.Add(grade_label, 0, wx.ALL, 5)
        sizer.Add(self.grade_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(max_info, 0, wx.ALL, 5)
        sizer.Add(type_label, 0, wx.ALL, 5)
        sizer.Add(self.type_choice, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(desc_label, 0, wx.ALL, 5)
        sizer.Add(self.desc_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(date_label, 0, wx.ALL, 5)
        sizer.Add(self.date_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        self.Center()
    
    def get_data(self):
        return (
            self.grade_ctrl.GetValue(),
            self.type_choice.GetStringSelection(),
            self.desc_ctrl.GetValue(),
            self.date_ctrl.GetValue()
        )


class NoteDialog(wx.Dialog):
    """Диалог за добавяне на бележка"""
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 300))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Заглавие
        title_label = wx.StaticText(panel, label="Заглавие:")
        self.title_ctrl = wx.TextCtrl(panel)
        
        # Съдържание
        content_label = wx.StaticText(panel, label="Съдържание:")
        self.content_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        
        # Бутони
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, wx.ID_OK, "Запиши")
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "Отказ")
        
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        
        # Layout
        sizer.Add(title_label, 0, wx.ALL, 5)
        sizer.Add(self.title_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(content_label, 0, wx.ALL, 5)
        sizer.Add(self.content_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        panel.SetSizer(sizer)
        self.Center()
    
    def get_data(self):
        return self.title_ctrl.GetValue(), self.content_ctrl.GetValue()


# ============================================================================
# 🚀 ГЛАВНО ПРИЛОЖЕНИЕ
# ============================================================================

class StudentApp(wx.App):
    def OnInit(self):
        frame = StudentAssistant()
        frame.Show()
        return True


if __name__ == "__main__":
    app = StudentApp()
    app.MainLoop() 