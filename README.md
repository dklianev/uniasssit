# Student Assistant Application

A comprehensive desktop application built with Python and wxPython to help students manage their academic life efficiently.

## Features

### 📚 **Six Main Modules**

1. **Home Dashboard** - Quick overview and navigation
2. **AI Chat** - Integrated AI assistant (supports Ollama local and OpenAI cloud)
3. **Notes Management** - Create, edit, and organize study notes by subject
4. **Pomodoro Timer** - 25-minute focused study sessions with breaks
5. **Calendar & Events** - Track assignments, exams, and important dates
6. **Grade Tracker** - Monitor academic performance with statistics

### 🎯 **Key Capabilities**

- **Note-Taking**: Organize notes by subject with rich text editing
- **Grade Management**: Track grades on Bulgarian 2-6 scale with automatic statistics
- **Event Planning**: Calendar integration for academic scheduling
- **Study Timer**: Built-in Pomodoro technique implementation
- **AI Integration**: Chat with AI for study assistance and questions
- **Data Persistence**: SQLite database for reliable data storage

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Required Dependencies

```bash
pip install wxpython requests sqlite3
```

### Optional Dependencies

For AI functionality:
- **Ollama** (local AI): Install from [ollama.ai](https://ollama.ai)
- **OpenAI API** (cloud AI): API key required

## Usage

### Starting the Application

```bash
python main.py
```

### First Run Setup

1. The application will automatically create a SQLite database (`student_assistant.db`)
2. Navigate through the tabs to explore different features
3. For AI chat, configure either Ollama (local) or OpenAI (API key required)

### Main Interface

- **Tab Navigation**: Click between Home, AI Chat, Notes, Pomodoro, Calendar, and Grades
- **Context Menus**: Right-click on lists for additional options
- **Keyboard Shortcuts**: Standard shortcuts for copy/paste in text areas

## Project Structure

```
uniassistant/
├── main.py          # Main GUI application
├── database.py      # SQLite database management
├── events.py        # Calendar and event handling
├── grades.py        # Grade tracking and statistics
├── ollama.py        # AI integration (Ollama/OpenAI)
├── pomodoro.py      # Pomodoro timer functionality
├── README.md        # This file
├── LICENSE          # MIT License
└── student_assistant.db  # SQLite database (created on first run)
```

## Technical Details

### Architecture

- **3-Tier Architecture**: Presentation (GUI) → Business Logic → Data Access
- **Database**: SQLite with 4 tables (notes, subjects, grades, events)
- **GUI Framework**: wxPython for cross-platform desktop interface
- **Threading**: Background operations for timers and AI requests

### Design Patterns

- **Facade Pattern**: Simplified interfaces for complex operations
- **Repository Pattern**: Data access abstraction
- **Strategy Pattern**: Multiple AI providers (Ollama/OpenAI)

### Database Schema

- **notes**: id, subject_id, title, content, created_at, updated_at
- **subjects**: id, name, color
- **grades**: id, subject_id, grade, description, date
- **events**: id, title, description, date, time

## Configuration

### AI Settings

Edit the `ollama.py` file to configure AI providers:

```python
# For Ollama (local)
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"

# For OpenAI (cloud)
OPENAI_API_KEY = "your-api-key-here"
```

### Database Location

By default, the database is created in the same directory as `main.py`. To change this, modify the `DATABASE_PATH` in `database.py`.


## Future Enhancements

- [ ] Cloud synchronization
- [ ] Export/import functionality
- [ ] More AI model options
- [ ] Mobile companion app
- [ ] Advanced statistics and reporting
