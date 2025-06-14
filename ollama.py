#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI чат клиент за Ollama и OpenAI
Базова функционалност за университетски проект
"""

import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.current_model = None
        self.openai_api_key = None
        self.use_openai = False
        print("🤖 AI клиент инициализиран")
    
    def set_openai_key_and_mode(self, api_key):
        """Задава OpenAI API ключ и превключва в OpenAI режим"""
        self.openai_api_key = api_key
        self.use_openai = True
        print("🔑 OpenAI режим активиран")
    
    def set_mode(self, mode="ollama"):
        """Превключва между 'ollama' и 'openai'"""
        self.use_openai = (mode == "openai")
        return True
    
    def check_connection(self):
        """Проверява дали AI услугата работи"""
        if self.use_openai:
            return self._check_openai_connection()
        else:
            return self._check_ollama_connection()
    
    def _check_ollama_connection(self):
        """Проверява дали Ollama работи"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def _check_openai_connection(self):
        """Проверява дали OpenAI API работи"""
        if not self.openai_api_key:
            return False
        try:
            headers = {"Authorization": f"Bearer {self.openai_api_key}"}
            response = requests.get("https://api.openai.com/v1/models", 
                                  headers=headers, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self):
        """Връща списък с налични модели"""
        if self.use_openai:
            return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
        else:
            return self._get_ollama_models()
    
    def _get_ollama_models(self):
        """Връща Ollama модели"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def set_model(self, model_name):
        """Задава модела за използване"""
        self.current_model = model_name
    
    def chat(self, message):
        """Изпраща съобщение към AI модела"""
        if not self.current_model:
            return "❌ Няма избран модел. Моля изберете модел."
        
        if self.use_openai:
            return self._chat_openai(message)
        else:
            return self._chat_ollama(message)
    
    def _chat_ollama(self, message):
        """Ollama чат функционалност"""
        if not self._check_ollama_connection():
            return "❌ Ollama не е достъпен. Моля стартирайте оllama"
        
        try:
            request_data = {
                "model": self.current_model,
                "prompt": message,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "Няма отговор")
            else:
                return f"❌ Ollama грешка {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ Времето за отговор изтече (30 сек)"
        except requests.exceptions.RequestException as e:
            return f"❌ Ollama мрежова грешка: {str(e)}"
        except Exception as e:
            return f"❌ Ollama неочаквана грешка: {str(e)}"
    
    def _chat_openai(self, message):
        """OpenAI чат функционалност"""
        if not self.openai_api_key:
            return "❌ Няма зададен OpenAI API ключ"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            request_data = {
                "model": self.current_model,
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"❌ OpenAI грешка {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ OpenAI: Времето за отговор изтече (30 сек)"
        except requests.exceptions.RequestException as e:
            return f"❌ OpenAI мрежова грешка: {str(e)}"
        except Exception as e:
            return f"❌ OpenAI неочаквана грешка: {str(e)}"
    
    def get_status(self):
        """Връща статуса на връзката"""
        if not self.check_connection():
            provider = "OpenAI" if self.use_openai else "Ollama"
            return f"❌ {provider} не е достъпен"
        
        if not self.current_model:
            return "⚠️ Няма избран модел"
        
        provider = "OpenAI" if self.use_openai else "Ollama"
        return f"✅ Готов с модел: {self.current_model} ({provider})" 