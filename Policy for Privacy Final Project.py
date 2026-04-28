import streamlit as st

st.set_page_config(page_title="Privacy Decision Tool", layout="centered")

st.title("🔐 Privacy Decision Tool")
st.write("Answer the questions below to determine the best privacy-preserving technology for your use case.")

# -----------------------------
# USER INPUTS
# -----------------------------
data_type_input = st.selectbox(
    "What type of data do you work with?",
    ["PII", "Aggregate", "Business", "Research"]
)

access_input = st.selectbox(
    "Who needs access to results?",
    ["Internal", "Partners", "Public"]
)

sharing_input = st.selectbox(
    "How is data shared?",
    ["Raw Shared", "Results Only", "Model Shared", "Not Sure"]
)

update_input = st.selectbox(
    "How often is data updated?",
    ["Constant", "Periodic", "Rare", "Static"]
)

collection_input = st.selectbox(
    "Where is data collected?",
    ["User Devices", "Central Server"]
)

trust_input = st.selectbox(
    "Do you trust the computation provider?",
    ["Yes", "Partial", "No"]
)

adversary_input = st.selectbox(
    "Adversary type?",
    ["Passive", "Active", "Both", "Not Sure"]
)

accuracy_input = st.selectbox(
    "Accuracy requirement?",
    ["Exact", "Small Error", "Statistical"]
)

budget_input = st.selectbox(
    "Budget?",
    ["Low", "Moderate", "High"]
)

multi_input = st.selectbox(
    "Multiple parties computing together?",
    ["Yes", "No"]
)

threats_input = st.multiselect(
    "Who are you protecting data from?",
    ["External", "Internal", "Partners", "Government"]
)

regulation_input = st.multiselect(
    "What regulations apply?",
    ["HIPAA", "GDPR", "CCPA", "Financial", "None"]
)

# -----------------------------
# DECISION LOGIC
# -----------------------------
if st.button("Get Recommendation"):

    technologies = [
        "Anonymization",
        "Local Differential Privacy",
        "Central Differential Privacy",
        "Cryptography",
        "Confidential Computing",
        "Secure MPC"
    ]

    scores = {tech: 0 for tech in technologies}

    def remove(tech):
        if tech in technologies:
            technologies.remove(tech)

    def remove_dp():
        remove("Local Differential Privacy")
        remove("Central Differential Privacy")

    # -------- Layer 1 --------
    if data_type_input == "PII":
        scores["Local Differential Privacy"] += 2
        scores["Central Differential Privacy"] += 2
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 1
        remove("Anonymization")

    elif data_type_input == "Aggregate":
        scores["Anonymization"] += 2
        scores["Central Differential Privacy"] += 1

    elif data_type_input == "Business":
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 2

    elif data_type_input == "Research":
        scores["Anonymization"] += 1
        scores["Central Differential Privacy"] += 1

    # Access
    if access_input == "Internal":
        scores["Confidential Computing"] += 1
    elif access_input == "Partners":
        scores["Cryptography"] += 2
    elif access_input == "Public":
        scores["Local Differential Privacy"] += 2
        scores["Central Differential Privacy"] += 3
        remove("Anonymization")

    # Sharing
    if sharing_input == "Raw Shared":
        scores["Anonymization"] += 2
        remove("Cryptography")
        remove("Confidential Computing")
    elif sharing_input == "Results Only":
        scores["Local Differential Privacy"] += 2
        scores["Central Differential Privacy"] += 3
        remove("Anonymization")
    elif sharing_input == "Model Shared":
        scores["Central Differential Privacy"] += 2

    # Updates
    if update_input == "Constant":
        remove("Anonymization")
        scores["Local Differential Privacy"] += 2
    elif update_input in ["Rare", "Static"]:
        scores["Anonymization"] += 1

    # -------- Layer 2 --------
    if "External" in threats_input:
        scores["Cryptography"] += 1
        scores["Central Differential Privacy"] += 1
    if "Internal" in threats_input:
        scores["Confidential Computing"] += 2
    if "Partners" in threats_input:
        scores["Cryptography"] += 2
    if "Government" in threats_input:
        scores["Central Differential Privacy"] += 1

    # Trust
    if trust_input == "Yes":
        scores["Anonymization"] += 1
    elif trust_input == "Partial":
        scores["Confidential Computing"] += 2
    elif trust_input == "No":
        scores["Cryptography"] += 3
        remove("Anonymization")

    # Adversary
    if adversary_input in ["Active", "Both"]:
        scores["Cryptography"] += 2
        remove("Anonymization")
    elif adversary_input == "Passive":
        scores["Central Differential Privacy"] += 1

    # -------- Layer 3 --------
    if accuracy_input == "Exact":
        remove_dp()
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 2
    elif accuracy_input == "Small Error":
        scores["Central Differential Privacy"] += 2
    elif accuracy_input == "Statistical":
        scores["Central Differential Privacy"] += 3

    # Budget
    if budget_input == "Low":
        remove("Cryptography")
        remove("Confidential Computing")
        scores["Anonymization"] += 1
    elif budget_input == "High":
        scores["Cryptography"] += 1
        scores["Confidential Computing"] += 1

    # Multi-party
    if multi_input == "Yes":
        scores["Secure MPC"] += 3
        scores["Cryptography"] += 1
        remove("Anonymization")
    else:
        scores["Anonymization"] += 1

    if multi_input == "Yes" and trust_input == "No":
        scores["Secure MPC"] += 3

    # Regulations
    if "HIPAA" in regulation_input or "GDPR" in regulation_input:
        scores["Central Differential Privacy"] += 2
        remove("Anonymization")
    if "Financial" in regulation_input:
        scores["Cryptography"] += 2
    if "None" in regulation_input:
        scores["Anonymization"] += 1

    # Prefer correct DP type
    if collection_input == "User Devices":
        scores["Local Differential Privacy"] += 2
    else:
        scores["Central Differential Privacy"] += 2

# -----------------------------
# RESULTS
    # -----------------------------
    filtered_scores = {tech: scores[tech] for tech in technologies}
    ranked = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
    
    st.subheader("📊 Recommendation")
    
    if ranked:
        top_tech, top_score = ranked[0]
        st.success(f"🏆 Recommended: {top_tech}")
    
        # show second option only if it's close
        if len(ranked) > 1:
            second_tech, second_score = ranked[1]
            
            # "close" threshold (you can tweak this)
            if second_score >= top_score - 1:
                st.info(f"Also consider: {second_tech}")
    
        # -----------------------------
        # EXPLANATIONS
        # -----------------------------
        explanations = {
            "Local Differential Privacy": "Local Differential Privacy ensures data is privatized on the user's device before collection. Each user adds noise, so even the server cannot see raw data. This provides very strong privacy but can reduce accuracy.",
            "Central Differential Privacy": "Central Differential Privacy collects raw data in a trusted server and adds noise when releasing results. It balances strong privacy guarantees with higher accuracy.",
            "Cryptography": "Cryptography protects data by encrypting it during storage and transmission. Advanced methods allow computation on encrypted data, making it essential for untrusted environments.",
            "Anonymization": "Anonymization removes identifying information from data. While simple and low-cost, it can be vulnerable to re-identification attacks and is weaker than other methods.",
            "Confidential Computing": "Confidential Computing uses secure hardware to protect data during processing, ensuring even cloud providers cannot access sensitive data.",
            "Secure MPC": "Secure Multi-Party Computation allows multiple parties to compute jointly without sharing their raw data, preserving privacy across organizations."
        }
    
        st.subheader("🧠 Why this?")
        st.write(explanations.get(top_tech, ""))
    
        if len(ranked) > 1 and second_score >= top_score - 1:
            st.subheader("🤔 Alternative Option")
            st.write(explanations.get(second_tech, ""))

    # -----------------------------
    # HYBRID LAYER
    # -----------------------------
    st.subheader("➕ Recommended Add-ons")

    addons = []

    if top != "Cryptography":
        addons.append("Encryption (baseline security)")

    if access_input == "Public" or "HIPAA" in regulation_input or "GDPR" in regulation_input:
        if collection_input == "User Devices":
            addons.append("Local Differential Privacy")
        else:
            addons.append("Central Differential Privacy")

    if multi_input == "Yes" and trust_input == "No":
        addons.append("Secure MPC")

    if trust_input == "Partial":
        addons.append("Confidential Computing")

    if data_type_input == "PII" or access_input == "Public":
        addons.append("Avoid relying solely on Anonymization")

    if addons:
        for a in addons:
            st.write(f"- {a}")
    else:
        st.write("No additional technologies recommended.")
