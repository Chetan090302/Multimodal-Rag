# Resume Builder

This repository contains a small resume-building / multimodal script.

## Prerequisites

- Python 3.10+ (or your preferred 3.x)
- Git (optional)

## Setup

1. Create and activate a virtual environment (Windows):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1  # or use venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## How to run

- Run the main script:

```powershell
python multimodel.py
```

- If the project expects input files, place them in the `resumes/`, `images/`, or `bytes/` folders as appropriate.

## Project layout

- `multimodel.py` — main entrypoint
- `requirements.txt` — Python dependencies
- `resumes/` — input or output resumes
- `images/` — helper images used by the project
- `bytes/` — binary data / cached pages

## Notes

- If `multimodel.py` accepts flags or arguments, run `python multimodel.py -h` to see available options.
- For any platform-specific issues on Windows, ensure your virtual environment is activated before installing or running.

