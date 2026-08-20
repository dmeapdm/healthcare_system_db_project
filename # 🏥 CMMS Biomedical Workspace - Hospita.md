# 🏥 CMMS Biomedical Workspace - Hospital Heller
### *Sistema Modular de Gestión Patrimonial e Ingeniería Clínica Basado en Estándares de la OMS*

Este proyecto es un desarrollo de **Investigación y Desarrollo (I+D+i)** diseñado de forma nativa en entornos Linux (Ubuntu) para resolver la trazabilidad, el cálculo de ciclo de vida (antigüedad) y la gestión de órdenes de trabajo en talleres de electromedicina hospitalaria.

---

## 📈 Evolución y Maduración del Pensamiento Arquitectónico (R&D Log)

La característica principal de este repositorio es su **trazabilidad cronológica**. Mediante el uso de Git Branches, se puede auditar cómo el sistema maduró desde un borrador relacional inicial hasta cumplir con normativas internacionales de auditoría:

*   **`main` (Punto Cero):** Estructura inicial con limitaciones de palabras reservadas e identificadores planos.
*   **`feature/01-schema-refactor`:** Rediseño maestro de base de datos relacional eliminando colisiones de sintaxis e implementando candados `CHECK` y restricciones `RESTRICT`.
*   **`feature/02-data-testing`:** Scripts de inyección masiva en taller y configuración de privilegios para un puente de red seguro.
*   **`feature/03-python-console`:** Desarrollo de canalizaciones nativas en Python y consultas de metadatos por terminal local.
*   **`feature/04-streamlit-interface`:** Migración a interfaz gráfica interactiva (GUI) web utilizando entornos virtuales aislados (`env`).
*   **`feature/05-oms-supplier-upgrade`:** *[Estado Actual]* Re-ingeniería de base de datos e interfaz para asimilar la **Tabla 1 de Datos de Inventario Mínimos de la OMS**, desenganchando proveedores rígidos (`NULL-Safe`) e inyectando auditorías automáticas de energía.

---

## 🛠️ Stack Tecnológico Utilizado
*   **Engine:** MySQL Server / Workbench.
*   **Core Backend:** Python 3.12 (Virtual Environments `venv`).
*   **Interface Layer:** Streamlit Ecosystem (UI/UX Responsivo).
*   **Version Control:** Git Graph & GitHub Cloud Pipeline.
*   **Operating System:** Ubuntu Linux Architecture (ThinkPad Dev-Station).

---

## 🚀 Cómo Ejecutar el Entorno Local
1. Clonar el repositorio.
2. Inicializar y activar el entorno virtual local: `source env/bin/activate`
3. Instalar dependencias esenciales.
4. Lanzar la aplicación CMMS: `streamlit run 14_app_visual.py`
