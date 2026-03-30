"""
Title: NS3 Flavivirus FASTA Extraction and MSA Pipeline
Author: Satish Kumar Manjhi
Designation: PhD Computational Biology
Email: satish.manjhi21@gmail.com

Description:
This script automates:
1. Extraction of FASTA sequences from RCSB PDB
2. Organization of sequences from flavivirus NS3 structures
3. Multiple Sequence Alignment (MSA) using EMBL-EBI Clustal Omega API

Requirements:
- Python 3.x
- requests library
"""

import os
import requests
import time

# ==============================
# USER CONFIGURATION
# ==============================

working_dir = r"D:\BITS_PhD_work\FLAVIVIRUS\RCSB_All_orthflavivirus_structure_database\NS3"
main_folders = ["Helicases", "Protease-helicases", "Proteases"]

# IMPORTANT: Provide valid email for EBI API
USER_EMAIL = "satish.manjhi21@gmail.com"

# ==============================
# FUNCTION: Download FASTA
# ==============================

def download_fasta(pdb_id):
    """
    Download FASTA sequence from RCSB PDB for a given PDB ID.
    """
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[ERROR] Failed for {pdb_id} | HTTP: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed for {pdb_id}: {e}")
        return None

# ==============================
# STEP 1: Extract FASTA
# ==============================

combined_sequences = []

for folder in main_folders:
    folder_path = os.path.join(working_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        for pdb_folder in os.listdir(subfolder_path):
            pdb_folder_path = os.path.join(subfolder_path, pdb_folder)
            if not os.path.isdir(pdb_folder_path):
                continue

            pdb_id = pdb_folder.split('_')[0]
            print(f"[INFO] Processing PDB ID: {pdb_id}")

            fasta_seq = download_fasta(pdb_id)

            if fasta_seq:
                fasta_file_path = os.path.join(pdb_folder_path, f"{pdb_id}.fasta")

                with open(fasta_file_path, "w") as f:
                    f.write(fasta_seq)

                combined_sequences.append(fasta_seq)
                print(f"[SAVED] {fasta_file_path}")

# ==============================
# STEP 2: Combine FASTA
# ==============================

ns3_sequences_folder = os.path.join(working_dir, "NS3_sequences")
os.makedirs(ns3_sequences_folder, exist_ok=True)

combined_fasta_path = os.path.join(ns3_sequences_folder, "combined.fasta")

with open(combined_fasta_path, "w") as f:
    f.write("\n".join(combined_sequences))

print(f"\n[INFO] Combined FASTA saved at: {combined_fasta_path}")

# ==============================
# STEP 3: MSA via Clustal Omega
# ==============================

clustal_url_run = "https://www.ebi.ac.uk/Tools/services/rest/clustalo/run"
clustal_url_status = "https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/"
clustal_url_result = "https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/"

with open(combined_fasta_path, "r") as f:
    combined_fasta = f.read()

params = {
    "email": USER_EMAIL,
    "sequence": combined_fasta,
    "stype": "protein"
}

print("\n[INFO] Submitting job to Clustal Omega...")

response = requests.post(clustal_url_run, data=params)

if response.status_code != 200:
    print("[ERROR] Job submission failed:", response.text)
    exit(1)

job_id = response.text.strip()
print(f"[INFO] Job ID: {job_id}")

# ==============================
# STEP 4: Check Job Status
# ==============================

while True:
    status_response = requests.get(clustal_url_status + job_id)
    status = status_response.text.strip()

    print(f"[STATUS] {status}")

    if status == "FINISHED":
        break
    elif status in ["ERROR", "FAILURE"]:
        print("[ERROR] Job failed")
        exit(1)

    time.sleep(10)

# ==============================
# STEP 5: Retrieve & Save Alignment
# ==============================

result_url = clustal_url_result + job_id + "/aln-clustal"
result_response = requests.get(result_url)

if result_response.status_code == 200:
    alignment_result = result_response.text

    alignment_file = os.path.join(ns3_sequences_folder, "alignment.aln")

    with open(alignment_file, "w") as f:
        f.write(alignment_result)

    print(f"\n[SUCCESS] Alignment saved at: {alignment_file}")

else:
    print("[ERROR] Failed to retrieve alignment:", result_response.text)
