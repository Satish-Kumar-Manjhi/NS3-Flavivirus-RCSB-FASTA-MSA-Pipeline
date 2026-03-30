# NS3-Flavivirus-RCSB-FASTA-MSA-Pipeline

## 🧬 Overview
This repository provides an automated structural bioinformatics pipeline for:
- Extracting protein sequences (FASTA) from RCSB PDB entries
- Organizing flavivirus NS3 protein datasets
- Performing Multiple Sequence Alignment (MSA) using Clustal Omega (EMBL-EBI API)

The workflow bridges structural data with sequence-based evolutionary analysis.

---

## 🎯 Objectives
- Automate FASTA retrieval from PDB IDs
- Enable comparative sequence analysis across flaviviruses
- Identify conserved residues in NS3 protease and helicase domains
- Support antiviral drug discovery research

---

## 🧠 Scientific Relevance
This pipeline supports:
- Catalytic triad analysis (His, Asp, Ser)
- Binding site conservation studies
- Structure–sequence relationship analysis
- Preprocessing for MD simulation interpretation

---

## ⚙️ Features
- Automated directory traversal
- FASTA extraction from RCSB Protein Data Bank
- Batch processing of multiple PDB structures
- Combined FASTA dataset generation
- Clustal Omega REST API integration
- Alignment retrieval and saving

---

## 📂 Project Structure
scripts/        → Python pipeline  
data/           → Input PDB structure directories  
results/        → Generated FASTA and alignment files  

---

## 🔧 Requirements
- Python 3.x
- requests

Install dependencies:
pip install -r requirements.txt

---

## ▶️ Usage
Run the pipeline:
python scripts/fetch_fasta_msa.py

---

## 📥 Input Format
Directory structure should follow:

Proteases/DENV/2FOM_chainA/

Where:
- Folder name starts with PDB ID

---

## 📤 Output
- Individual FASTA files per PDB
- Combined FASTA file:
results/combined.fasta
- Alignment file:
results/alignment.aln

---

## 🔬 Methodology

### Step 1: Extract PDB IDs
Folder names are parsed to identify PDB IDs

### Step 2: Fetch FASTA
Sequences retrieved from:
https://www.rcsb.org/fasta/entry/<PDB_ID>

### Step 3: Combine Sequences
All sequences merged into a single FASTA file

### Step 4: Perform MSA
Alignment via EMBL-EBI Clustal Omega API

---

## 🔐 API Usage Note
This pipeline uses EMBL-EBI Clustal Omega API.

⚠️ IMPORTANT:
Update email inside script:
"email": "your_email@example.com"

---

## 🚀 Future Improvements
- Sequence conservation scoring (Shannon entropy)
- Structure mapping (PyMOL)
- Integration with MD simulations
- Parallel processing

---

## 👨‍🔬 Author
Satish Kumar Manjhi  
PhD Computational Biology  
Email: satish.manjhi21@gmail.com  

---

## 📄 License
MIT License
