# RoboMed – AI for Safer Patient Monitoring

RoboMed is a robotics and AI system designed to support hospital staff through intelligent monitoring, automated inspection workflows, and simulation-driven decision support.

The system combines robotic perception, AI-based analysis, and real-time visualization to assist with patient observation and reduce monitoring workload.

---

## Overview

Hospitals face increasing monitoring demands, where medical staff must track multiple patients simultaneously. RoboMed explores how intelligent robotic assistants can improve situational awareness and support early intervention.

The project integrates:

- robotic data acquisition (simulation-based)
- AI-driven interpretation
- automated inspection workflows
- dashboard-based visualization

---

## Key Features

- AI-assisted monitoring logic  
- Integration with robot-generated data  
- Automated inspection pipeline (LLM-based)  
- Real-time dashboard (Streamlit)  
- Modular and extensible system design  

---

## System Architecture

RoboMed consists of multiple layers:

- **Simulation Layer** → robot behavior and data capture  
- **Data Layer** → logs, snapshots, structured outputs  
- **AI Layer** → interpretation and decision support  
- **Interface Layer** → dashboard and visualization  

---

## Repository Structure

```text
robomed-ai/
├── dashboard/        # Streamlit interface
├── ai_pipeline/      # AI / LLM processing logic

## Simulation

Simulation environment:
https://github.com/hkhodamoradi/robomed-simulation

## Demo

Full system demo:
[Add full demo link here]

Robot perspective:
https://youtu.be/BnZjWKFgz0M

Top view:
https://youtu.be/SilspwN7Z0g
