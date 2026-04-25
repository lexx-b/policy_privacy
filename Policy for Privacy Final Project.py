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

    technologies = ["Anonymization", "Differential Privacy", "Cryptography", "Confidential Computing"]
    scores = {tech: 0 for tech in technologies}

    def remove(tech):
        if tech in technologies:
            technologies.remove(tech)

    # -------- Layer 1 --------
    if data_type_input == "PII":
        scores["Differential Privacy"] += 2
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 1
        remove("Anonymization")

    elif data_type_input == "Aggregate":
        scores["Anonymization"] += 2
        scores["Differential Privacy"] += 1

    elif data_type_input == "Business":
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 2

    elif data_type_input == "Research":
        scores["Anonymization"] += 1
        scores["Differential Privacy"] += 1

    if access_input == "Internal":
        scores["Confidential Computing"] += 1

    elif access_input == "Partners":
        scores["Cryptography"] += 2

    elif access_input == "Public":
        scores["Differential Privacy"] += 3
        remove("Anonymization")

    if sharing_input == "Raw Shared":
        scores["Anonymization"] += 2
        remove("Cryptography")
        remove("Confidential Computing")

    elif sharing_input == "Results Only":
        scores["Differential Privacy"] += 3
        remove("Anonymization")

    elif sharing_input == "Model Shared":
        scores["Differential Privacy"] += 2

    if update_input == "Constant":
        remove("Anonymization")

    elif update_input in ["Rare", "Static"]:
        scores["Anonymization"] += 1

    # -------- Layer 2 --------
    if "External" in threats_input:
        scores["Cryptography"] += 1
        scores["Differential Privacy"] += 1

    if "Internal" in threats_input:
        scores["Confidential Computing"] += 2

    if "Partners" in threats_input:
        scores["Cryptography"] += 2

    if "Government" in threats_input:
        scores["Differential Privacy"] += 1

    if trust_input == "Yes":
        scores["Anonymization"] += 1

    elif trust_input == "Partial":
        scores["Confidential Computing"] += 2

    elif trust_input == "No":
        scores["Cryptography"] += 3
        remove("Anonymization")

    if adversary_input in ["Active", "Both"]:
        scores["Cryptography"] += 2
        remove("Anonymization")

    elif adversary_input == "Passive":
        scores["Differential Privacy"] += 1

    # -------- Layer 3 --------
    if accuracy_input == "Exact":
        remove("Differential Privacy")
        scores["Cryptography"] += 2
        scores["Confidential Computing"] += 2

    elif accuracy_input == "Small Error":
        scores["Differential Privacy"] += 2

    elif accuracy_input == "Statistical":
        scores["Differential Privacy"] += 3

    if budget_input == "Low":
        remove("Cryptography")
        remove("Confidential Computing")
        scores["Anonymization"] += 1

    elif budget_input == "High":
        scores["Cryptography"] += 1
        scores["Confidential Computing"] += 1

    if multi_input == "Yes":
        scores["Cryptography"] += 3
        remove("Anonymization")

    elif multi_input == "No":
        scores["Anonymization"] += 1

    if "HIPAA" in regulation_input or "GDPR" in regulation_input:
        scores["Differential Privacy"] += 2
        remove("Anonymization")

    if "Financial" in regulation_input:
        scores["Cryptography"] += 2

    if "None" in regulation_input:
        scores["Anonymization"] += 1

    # -----------------------------
    # RESULTS
    # -----------------------------
    filtered_scores = {tech: scores[tech] for tech in technologies}
    ranked = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)

    st.subheader("📊 Recommended Technologies")

    for tech, score in ranked:
        st.write(f"**{tech}** — Score: {score}")

    if ranked:
        top = ranked[0][0]
        st.success(f"🏆 Top Recommendation: {top}")

        # Optional explanation
        explanations = {
            "Differential Privacy": "Best for sharing statistical insights while protecting individual-level data.",
            "Cryptography": "Best when data must remain hidden during computation, especially across multiple parties.",
            "Anonymization": "Best for low-risk datasets in trusted environments.",
            "Confidential Computing": "Best for processing sensitive data securely in cloud environments."
        }

        st.info(explanations.get(top, ""))
