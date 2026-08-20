# 🏥 CMMS Biomedical Workspace - Hospital Heller
### *Modular Asset Management & Clinical Engineering System Based on WHO Core Inventory Standards*

This project is a comprehensive **Research and Development (R&D+i)** environment designed natively on Linux (Ubuntu) architectures. It solves real-world hospital engineering challenges: lifecycle tracking (lifespan calculation), local database pipeline bypasses, inventory data entry, and secure work order tracking within a biomedical workshop.

---

## 📈 Evolution of Architectural Thinking (R&D Log / Roadmap)

The defining hallmark of this repository is its **strict chronological traceability**. Through precise Git branching, stakeholders can audit exactly how the software matured from a raw data draft into an international-standard compliance matrix:

*   **`main` (Root Commit):** Initial database blueprint. Contained standard relational schemas but exhibited structural keyword collisions (e.g., `name`, `code`) and rigid vendor constraints.
*   **`feature/01-schema-refactor`:** Major database refactoring. Cleaned up reserved keywords and injected strict data integrity constraints via uppercase/lowercase `CHECK` fields and `RESTRICT` deletion blocks.
*   **`feature/02-data-testing`:** Core workshop simulation scripts. Developed transaction payloads for hardware and vendors, and built secure permission matrices for local application layers.
*   **`feature/03-python-console`:** Built native Python database engines and metadata extraction tunnels, logging equipment lifespans directly through terminal pipelines.
*   **`feature/04-streamlit-interface`:** Migrated from backend scripts to an interactive Graphical User Interface (GUI) powered by Streamlit web instances running on isolated virtual environments (`env`).
*   **`feature/05-oms-supplier-upgrade`:** *[Current Production Branch]* Complete re-engineering of the database and UI layers to fully assimilate the **WHO Technical Series: Table 1 Minimum Inventory Requirements**. Decoupled rigid procurement links using `NULL-Safe` dynamic selectboxes and integrated automated electrical compliance auditing fields.

---

## 🛠️ Technological Stack
*   **Database Engine:** MySQL Server / Workbench Ecosystem.
*   **Core Backend:** Python 3.12 (Isolated Virtual Environments `venv`).
*   **Interface Layer:** Streamlit Architecture (Responsive UI/UX).
*   **Version Control:** Git Graph Engine & GitHub Cloud Pipeline.
*   **Operating System:** Ubuntu Linux OS (ThinkPad Dev-Station).

---

## 🚀 Local Environment Installation & Deployment
1. Clone the repository into your local workspace.
2. Initialize and activate the secure virtual sandbox environment:
   ```bash
   source env/bin/activate
   ```
3. Install required database and layout dependencies.
4. Fire up the live biomedical workspace dashboard:
   ```bash
   streamlit run 14_app_visual.py
   ```
