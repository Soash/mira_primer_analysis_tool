# 🧬 MIRA Primer Analyzer

MIRA (Multienzyme Isothermal Rapid Amplification) Primer Analyzer is a specialized, interactive Django web application designed for the thermodynamic analysis and visual alignment of primer pairs. It is particularly optimized for isothermal amplification assays, where the formation of primer-dimers and active 3' terminal extensions can severely impact amplification efficiency and cause false-positive results.

Live deployment: [mira.soash.dev](https://mira.soash.dev)

---

## 📋 Table of Contents
1. [Key Features](#-key-features)
2. [How It Works (Under the Hood)](#-how-it-works-under-the-hood)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [Running the Application](#-running-the-application)
7. [Production Deployment](#-production-deployment)
8. [License](#-license)

---

## ✨ Key Features

* **Interactive Sliding Alignment Grid**: Real-time visualization of the Forward Primer (5' &rarr; 3') and Reverse Primer (3' &rarr; 5' visual presentation) alignments.
* **Dynamic Shift Slider**: Easily shift alignments relative to one another (using the UI slider or **Prev / Next** buttons) to explore overlapping configurations.
* **Watson-Crick Pair Mapping**: Highlights hydrogen bonds (`|`) in yellow between matching nucleotides (A-T, G-C).
* **3' Terminal Extension Detection**:
  * Automatically detects and flags Watson-Crick base-pairing at the active 3' end of either primer.
  * Displays warning alerts if a single primer is prone to 3' extension.
  * Displays a critical red alert (**Mutual 3' Extension**) if both primers can simultaneously extend each other—a fatal design flaw in isothermal amplification.
* **Thermodynamic Analysis (Primer3 & Biopython)**:
  * **Length**: Number of base pairs.
  * **GC Content %**: Calculated dynamically via Biopython.
  * **Melting Temperature ($T_m$)**: Accurate $T_m$ calculation using Primer3.
  * **Self-Annealing Hairpin Free Energy ($\Delta G$)**: Minimum free energy ($\text{kcal/mol}$) for hairpin structure formation.
  * **Cross-Annealing Heterodimer Free Energy ($\Delta G$)**: Minimum free energy ($\text{kcal/mol}$) for forward/reverse primer dimer structures.

---

## 🔬 How It Works (Under the Hood)

### Isothermal Amplification Constraints
Unlike conventional PCR, which relies on high-temperature thermal cycling (e.g., $95^\circ\text{C}$) to melt non-specific primer structures, isothermal amplification systems like MIRA operate at a constant temperature (usually between $37^\circ\text{C}$ and $42^\circ\text{C}$). 

If the 3' terminal end of a primer is annealed to any sequence (including the other primer) and has a Watson-Crick base pair at its extreme 3' nucleotide, the isothermal DNA polymerase will initiate synthesis. This results in **primer-dimer elongation**, which rapidly depletes reaction components (dNTPs, primers, polymerase) and generates false-positive fluorescent signals.

### 3' Terminal Match Logic
The tool evaluates the alignment at every shift coordinate. If:
1. The **Forward Primer**'s last nucleotide (index `length - 1` on its 3' end) matches the aligned character on the Reverse Primer.
2. The **Reverse Primer**'s last nucleotide (index `0` on its 3' end when split/reversed) matches the aligned character on the Forward Primer.

If both conditions are met at any alignment configuration, it triggers the **Mutual 3' Extension** alert.

---

## 🛠️ Tech Stack

* **Backend**: Django 6.0.5, Python 3.10+
* **Bioinformatics**: `primer3-py` (wrapper for the C-based Primer3 library), `biopython`
* **Frontend**: HTML5, Vanilla JavaScript, CSS3
* **CSS Framework**: Tailwind CSS (integrated via `django-tailwind`)
* **Utilities**: `django-environ` (configuration management), `django-browser-reload` (development hot-reload)

---

## 📂 Project Structure

```text
mira_primer_analysis_tool/
│
├── manage.py                  # Django administrative script
├── db.sqlite3                 # SQLite database file (development)
│
├── project/                   # Project-level configuration directory
│   ├── .env                   # Environment secrets and settings
│   ├── settings.py            # Main Django configuration file
│   ├── urls.py                # Main routing table
│   └── wsgi.py / asgi.py      # WSGI/ASGI application endpoints
│
├── primer_analyzer/           # Core application files
│   ├── views.py               # API and page controllers
│   ├── utils.py               # Thermodynamic analysis wrapper functions (Primer3/BioPython)
│   └── templates/
│       └── primer_analyzer/
│           └── index.html     # Interactive interface with alignment logic & JS script
│
├── theme/                     # Tailwind theme app
│   ├── templates/
│   │   └── base.html          # Base layout template
│   └── static_src/            # Node/npm files for Tailwind compiler (package.json, src/, etc.)
│
└── dump/                      # Documentation and utility dumps
```

---

## ⚙️ Prerequisites & Installation

### 1. Prerequisites
Ensure you have the following installed on your machine:
* Python 3.10 or higher
* Node.js (version 16+) and `npm` (required to compile Tailwind CSS)
* Git

### 2. Clone the Repository
```bash
git clone https://github.com/Soash/mira_primer_analysis_tool.git
cd mira_primer_analysis_tool
```

### 3. Create and Activate Virtual Environment
On Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python Dependencies
```bash
pip install django django-environ django-tailwind django-browser-reload primer3-py biopython
```

### 5. Initialize Tailwind CSS Dependencies
Install NPM packages inside the Tailwind theme app:
```bash
python manage.py tailwind install
```

### 6. Set Up Environment Variables
Create a file named `.env` in the `project/` directory (adjacent to `settings.py`) with the following fields:
```ini
ENVIRONMENT=development
SECRET_KEY=your-secure-random-secret-key-here
```

---

## 🚀 Running the Application

To run the application locally, you need to run both the Tailwind compiler watcher and the Django development server in parallel.

### Step A: Compile Tailwind CSS (terminal 1)
Make sure your virtual environment is active, then run:
```bash
python manage.py tailwind start
```
This command starts the Tailwind CSS builder, watch mode, and compiles styles dynamically as templates change.

### Step B: Start Django Server (terminal 2)
In a separate terminal with the virtual environment active, run:
```bash
python manage.py runserver
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

---

## 🌐 Production Deployment

For deploying the application to production:

1. Update the `.env` file:
   ```ini
   ENVIRONMENT=production
   SECRET_KEY=a-very-strong-production-only-secret-key
   ```
2. Build Tailwind CSS for production (minified):
   ```bash
   python manage.py tailwind build
   ```
3. Run migrations and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --no-input
   ```
4. Set up a production WSGI server (e.g., Gunicorn or uWSGI) behind a reverse proxy like Nginx.

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details (if applicable).
