**🛡️ VigilMJ — Digital Wellbeing & Productivity Suite**

VigilMJ is not just another task manager; it is an all-in-one Digital Wellbeing & Productivity Suite designed to streamline daily workflows, prevent burnout, and foster focus. Built with a modern dark-glassmorphism UI, VigilMJ helps users balance intense task execution with mindful breaks.

**✨ Features Highlight**

🚀 Live Features

📋 Smart Task Management: Create, edit, and organize daily tasks with live progress tracking and automatic deadline validation.

📝 Dynamic Notepad: Quick note-taking system to capture ideas, code snippets, and daily thoughts seamlessly.

📊 Visual Progress Bar: Real-time analytics on completed vs. pending tasks.

🔒 Secure User Authentication: Individual user accounts with isolated task and note storage.

🎨 Glassmorphism Metallic UI: Responsive, sleek, and animated dark-mode design powered by Tailwind CSS.


**🔮 Upcoming Features (Roadmap)**

⏱️ Pomodoro Timer & Focus Mode: Distraction-free workspace with structured deep-work intervals.

🧘 5-Minute Reset & Mindful Breaks: Built-in wellness prompts to avoid cognitive fatigue.

🔔 Break Reminders: Gentle screen notifications encouraging regular posture checks and hydration.

🚨 Forced Shutdown Alarm: (Desktop Helper Script) Intelligent screen-time limiter for healthy work-life balance.


**🛠️ Tech Stack**

Backend: Python, Django Web Framework

Frontend: HTML5, Tailwind CSS, JavaScript (ES6)

Icons & Fonts: FontAwesome 6, Google Fonts (Inter)

Database: SQLite (Development) / PostgreSQL (Production ready)


**📦 Installation & Setup Guide**

1. Clone the Repository
_Bash_
git clone https://github.com/your-username/VigilMJ-Task-Manager.git
cd VigilMJ-Task-Manager
3. Create & Activate Virtual Environment
_Bash_
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
_Bash_
pip install -r requirements.txt
4. Database Migrations
_Bash_
python manage.py makemigrations
python manage.py migrate
5. Run the Server
_Bash_
python manage.py runserver
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to explore VigilMJ.


**📂 Project Structure**

VigilMJ_Project/
│
├── my_site/              # Main Django Configuration

├── todo_app/             # Core Productivity App (Views, Models, Forms)

├── static/               # CSS, JavaScript & Static Images

├── templates/            # UI Templates (base.html, index.html, notes.html, etc.)

├── db.sqlite3            # Database File

├── manage.py             # Django CLI Tool

└── README.md             # Project Documentation


**📜 License & Copyright**

© 2026 VigilMJ — Created with ❤️ for high-performance productivity and digital wellbeing. All Rights Reserved.
