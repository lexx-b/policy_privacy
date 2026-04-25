#!/usr/bin/env python
# coding: utf-8

# In[2]:


technologies = ["Anonymization", "Differential Privacy", "Cryptography", "Confidential Computing"]
scores = {tech: 0 for tech in technologies}


def remove(tech):
    if tech in technologies:
        technologies.remove(tech)


# -----------------------------
# Layer 1: Data and Context
# -----------------------------
# Q1: Data Type
def data_type(answer):
    # Options: "PII", "Aggregate", "Business", "Research"
    if answer == "PII":
        scores["Differential Privacy"] += 2
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 1
        remove("Anonymization")

    elif answer == "Aggregate":
        scores["Anonymization"] += 2
        scores["Differential Privacy"] += 1

    elif answer == "Business":
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 2

    elif answer == "Research":
        scores["Anonymization"] += 1
        scores["Differential Privacy"] += 1


# Q2: Access Level
def access(answer):
    # Options: "Internal", "Partners", "Public"
    if answer == "Internal":
        scores["Confidential Computing"] += 1

    elif answer == "Partners":
        scores["Cryptography"] += 2

    elif answer == "Public":
        scores["Differential Privacy"] += 3
        remove("Anonymization")


# Q3: Data Sharing Requirement (TIGHTENED)
def sharing(answer):
    # Options:
    # "Raw Shared" → raw dataset leaves your org
    # "Results Only" → only aggregates/statistics shared
    # "Model Shared" → trained model shared, not raw data
    # "Not Sure"
    
    if answer == "Raw Shared":
        scores["Anonymization"] += 2
        remove("Cryptography")
        remove("Confidential Computing")

    elif answer == "Results Only":
        scores["Differential Privacy"] += 3
        remove("Anonymization")

    elif answer == "Model Shared":
        scores["Differential Privacy"] += 2

    elif answer == "Not Sure":
        pass  # no strong signal


# Q4: Data Update Frequency
def update_frequency(answer):
    # Options: "Constant", "Periodic", "Rare", "Static"
    if answer == "Constant":
        remove("Anonymization")

    elif answer in ["Rare", "Static"]:
        scores["Anonymization"] += 1


# -----------------------------
# Layer 2: Threats and Trust
# -----------------------------
# Q5: Threat Model (TIGHTENED labels)
def threats(answer_list):
    # Options inside list: "External", "Internal", "Partners", "Government"
    
    if "External" in answer_list:
        scores["Cryptography"] += 1
        scores["Differential Privacy"] += 1

    if "Internal" in answer_list:
        scores["Confidential Computing"] += 2

    if "Partners" in answer_list:
        scores["Cryptography"] += 2

    if "Government" in answer_list:
        scores["Differential Privacy"] += 1


# Q6: Trust in Processor
def trust(answer):
    # Options: "Yes", "Partial", "No"
    if answer == "Yes":
        scores["Anonymization"] += 1

    elif answer == "Partial":
        scores["Confidential Computing"] += 2

    elif answer == "No":
        scores["Cryptography"] += 3
        remove("Anonymization")


# Q7: Adversary Type
def adversary_type(answer):
    # Options: "Passive", "Active", "Both", "Not Sure"
    if answer in ["Active", "Both"]:
        scores["Cryptography"] += 2
        remove("Anonymization")

    elif answer == "Passive":
        scores["Differential Privacy"] += 1


# -----------------------------
# Layer 3: Operational Requirements
# -----------------------------
# Q8: Accuracy Requirement
def accuracy(answer):
    # Options: "Exact", "Small Error", "Statistical"
    if answer == "Exact":
        remove("Differential Privacy")
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 2

    elif answer == "Small Error":
        scores["Differential Privacy"] += 2

    elif answer == "Statistical":
        scores["Differential Privacy"] += 3


# Q9: Budget
def budget(answer):
    # Options: "Low", "Moderate", "High"
    if answer == "Low":
        remove("Cryptography")
        remove("Confidential Computing")
        scores["Anonymization"] += 1

    elif answer == "High":
        scores["Cryptography"] += 1
        scores["Confidential Computing"] += 1


# Q10: Compute Constraints (TIGHTENED wording)
def compute_constraints(answer):
    # Options: "Real-time", "Batch", "Flexible"
    if answer == "Real-time":
        remove("Cryptography")

    elif answer == "Flexible":
        scores["Cryptography"] += 1


# Q11: Multi-party Computation
def multi_party(answer):
    # Options: "Yes", "No"
    if answer == "Yes":
        scores["Cryptography"] += 3
        remove("Anonymization")

    elif answer == "No":
        scores["Anonymization"] += 1


# Q12: Regulation (TIGHTENED labels)
def regulation(answer_list):
    # Options: "HIPAA", "GDPR", "CCPA", "Financial", "None"
    
    if "HIPAA" in answer_list or "GDPR" in answer_list:
        scores["Differential Privacy"] += 2
        remove("Anonymization")

    if "Financial" in answer_list:
        scores["Cryptography"] += 2

    if "None" in answer_list:
        scores["Anonymization"] += 1


# -----------------------------
# Example Run
# -----------------------------
data_type("PII")
access("Public")
sharing("Results Only")
update_frequency("Constant")

threats(["External", "Partners"])
trust("No")
adversary_type("Active")

accuracy("Small Error")
budget("Moderate")
compute_constraints("Batch")
multi_party("No")
regulation(["GDPR"])


# -----------------------------
# Final Ranking
# -----------------------------
filtered_scores = {tech: scores[tech] for tech in technologies}
ranked = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)

print("\nRecommended Technologies:")
for tech, score in ranked:
    print(f"{tech}: {score}")

if ranked:
    print(f"\nTop Choice: {ranked[0][0]}")


# In[ ]:




