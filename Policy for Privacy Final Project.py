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
# IMPLEMENTATION GUIDANCE FUNCTION
# -----------------------------
def get_implementation_guidance(tech, data_type, access, sharing, update, collection,
                                 trust, adversary, accuracy, budget, multi, threats, regulation):
    """
    Returns use-case-specific implementation guidance based on the recommended
    technology AND the user's specific questionnaire inputs.
    """

    guidance = []

    if tech == "Central Differential Privacy":
        # Epsilon selection
        if "HIPAA" in regulation or "GDPR" in regulation:
            guidance.append("**Epsilon (ε) value:** Use ε ≤ 1.0. Strict regulations require tight privacy budgets. "
                            "Consider ε = 0.1–0.5 for highly sensitive PII under HIPAA/GDPR.")
        elif accuracy == "Small Error":
            guidance.append("**Epsilon (ε) value:** Use ε in the range of 1.0–3.0 to balance utility and privacy. "
                            "This allows small statistical error while maintaining meaningful protection.")
        elif accuracy == "Statistical":
            guidance.append("**Epsilon (ε) value:** ε = 3.0–10.0 is acceptable when only statistical patterns matter. "
                            "Higher epsilon means better utility but weaker privacy guarantees.")

        # Noise mechanism
        if sharing == "Results Only":
            guidance.append("**Noise mechanism:** Apply the Laplace mechanism for numeric query outputs (counts, sums, means). "
                            "Use the Gaussian mechanism if your downstream analysis requires bounded L2 sensitivity.")
        if sharing == "Model Shared":
            guidance.append("**Noise mechanism:** Use DP-SGD (differentially private stochastic gradient descent) "
                            "to inject noise during model training rather than at query time.")

        # Privacy budget management
        if update in ["Constant", "Periodic"]:
            guidance.append("**Privacy budget management:** Since data updates frequently, implement a rolling privacy budget "
                            "with composition tracking (e.g., using the moments accountant or Rényi DP). "
                            "Each query consumes budget — set a maximum total ε across the data lifecycle.")
        elif update in ["Rare", "Static"]:
            guidance.append("**Privacy budget management:** Static datasets allow a fixed global ε budget. "
                            "Define query categories in advance and pre-allocate budget per category.")

        # Sensitivity calibration
        if data_type == "PII":
            guidance.append("**Sensitivity calibration:** Carefully bound the global sensitivity of each query. "
                            "For PII (e.g., age, income), clip individual values before computing statistics "
                            "to limit how much one person can skew results.")

        # Auditing
        if "HIPAA" in regulation or "GDPR" in regulation:
            guidance.append("**Auditing:** Maintain a privacy loss ledger. Log every query with its ε consumption. "
                            "This supports regulatory audits and demonstrates accountability.")

    elif tech == "Local Differential Privacy":
        # Protocol selection
        if data_type == "PII" and sharing == "Results Only":
            guidance.append("**Protocol selection:** Use Randomized Response for binary/categorical attributes "
                            "(e.g., yes/no questions). For numerical values, use the Duchi, Kairouz & Wainwright "
                            "(square wave) mechanism or the Piecewise mechanism for better utility.")
        if update == "Constant":
            guidance.append("**Protocol selection:** For streaming/continuous data from user devices, "
                            "use memoization (consistent randomization per user per value) to prevent "
                            "longitudinal privacy leakage across repeated reports.")

        # Epsilon for LDP
        guidance.append("**Epsilon (ε) for LDP:** LDP requires higher ε than central DP for equivalent utility "
                        "(typically ε = 1–8). Apple uses ε ≈ 8 per day for keyboard/emoji analytics. "
                        "Google RAPPOR uses ε ≈ 2–4. Align with your accuracy requirement.")

        # Aggregation server
        if trust == "No":
            guidance.append("**Aggregation server:** Since you don't trust the server, LDP is the right call — "
                            "the server only receives already-privatized reports. Ensure the server cannot "
                            "link multiple reports to the same user (use anonymous submission or mixnets).")

        # Data collection
        if collection == "User Devices":
            guidance.append("**Client-side implementation:** Privatization must happen on the device before transmission. "
                            "Use a well-audited library (e.g., Google's DP library or Apple's DP framework). "
                            "Never send raw values to the server even temporarily.")

    elif tech == "Cryptography":
        # Encryption type
        if sharing == "Raw Shared":
            guidance.append("**Encryption at rest and in transit:** Use AES-256-GCM for data at rest. "
                            "Use TLS 1.3 for all data in transit. Never store encryption keys alongside data.")
        if trust == "No":
            guidance.append("**End-to-end encryption:** Since you don't trust the computation provider, "
                            "implement client-side encryption. The server should only ever see ciphertext. "
                            "Consider hybrid encryption: RSA/ECDH for key exchange, AES for bulk data.")
        if "Partners" in threats:
            guidance.append("**Key management:** Use separate encryption keys per partner. "
                            "Implement key rotation policies. Use an HSM (Hardware Security Module) "
                            "or a managed KMS (e.g., AWS KMS, Google Cloud KMS) if budget allows.")

        # Digital signatures / integrity
        if adversary in ["Active", "Both"]:
            guidance.append("**Integrity protection:** Against active adversaries, encryption alone is insufficient. "
                            "Add HMAC-SHA256 or use authenticated encryption (AES-GCM already provides this). "
                            "Sign data packages with ECDSA to detect tampering.")

        # Regulations
        if "Financial" in regulation:
            guidance.append("**Regulatory alignment:** Financial regulations (PCI-DSS, SOX) require documented "
                            "encryption standards, key management procedures, and access logs. "
                            "Ensure your implementation is FIPS 140-2 validated if applicable.")

    elif tech == "Secure MPC":
        # Protocol selection
        if trust == "No" and multi == "Yes":
            guidance.append("**Protocol selection:** With no trusted party and multiple computing parties, "
                            "use Secret Sharing-based MPC (e.g., SPDZ or BGW protocol) for arithmetic computations, "
                            "or Yao's Garbled Circuits for Boolean/comparison operations.")
        if adversary in ["Active", "Both"]:
            guidance.append("**Security model:** Use MPC protocols with active security (malicious model), "
                            "such as MASCOT or SPDZ2k. These tolerate cheating parties but have higher overhead "
                            "than semi-honest protocols. Do not use semi-honest-only protocols if adversaries may deviate.")
        elif adversary == "Passive":
            guidance.append("**Security model:** Semi-honest (passive) security is sufficient. "
                            "Consider ABY or MP-SPDZ framework for efficient semi-honest MPC. "
                            "This reduces communication overhead significantly compared to malicious-secure protocols.")

        # Communication
        if update == "Constant":
            guidance.append("**Communication overhead:** MPC has high round-trip communication cost. "
                            "For constantly updated data, batch computations and minimize interactive rounds. "
                            "Consider preprocessing (offline phase) to reduce online latency.")
        if budget == "Low":
            guidance.append("**Budget constraint:** MPC is computationally expensive. With a low budget, "
                            "limit MPC to the minimum necessary computation (e.g., only the final aggregation step). "
                            "Use open-source frameworks like MP-SPDZ or MOTION to avoid licensing costs.")

        # Number of parties
        guidance.append("**Party setup:** Define the number of computing parties and the corruption threshold upfront. "
                        "For 3-party computation with one allowed corrupt party, use replicated secret sharing "
                        "(very efficient). For more parties, use threshold secret sharing (Shamir's scheme).")

    elif tech == "Confidential Computing":
        # TEE selection
        if budget == "High":
            guidance.append("**TEE selection:** With a high budget, consider Intel TDX (Trust Domain Extensions) "
                            "for VM-level isolation, or AMD SEV-SNP for stronger memory encryption. "
                            "These are newer and more robust than SGX enclaves.")
        elif budget == "Moderate":
            guidance.append("**TEE selection:** Intel SGX (Software Guard Extensions) is the most widely supported "
                            "enclave technology. Use it for enclave-based computation where only specific code "
                            "runs in the trusted execution environment.")
        elif budget == "Low":
            guidance.append("**TEE selection:** Budget is constrained — consider ARM TrustZone if deploying on "
                            "mobile/edge devices. For cloud, use provider-managed confidential VMs "
                            "(e.g., Azure Confidential Computing) which reduce operational overhead.")

        # Attestation
        guidance.append("**Remote attestation:** Always verify the enclave before sending sensitive data. "
                        "Use remote attestation (Intel DCAP or third-party attestation services) to cryptographically "
                        "confirm the enclave is running the expected unmodified code.")

        # Threat model
        if "Internal" in threats:
            guidance.append("**Insider threat mitigation:** Confidential Computing is well-suited here. "
                            "Ensure the enclave code is open-source and auditable so insiders cannot hide backdoors. "
                            "Use sealed storage to persist encrypted enclave state.")

        if trust == "Partial":
            guidance.append("**Partial trust scenario:** Since you partially trust the provider, pair Confidential "
                            "Computing with audit logging outside the enclave. The provider cannot tamper with "
                            "enclave execution, but log integrity should be verified independently.")

    elif tech == "Anonymization":
        # Technique selection
        if data_type == "Research":
            guidance.append("**Technique selection:** For research data, apply k-anonymity (minimum k=5 recommended) "
                            "combined with l-diversity to protect against attribute disclosure. "
                            "For sensitive attributes, also apply t-closeness.")
        if update in ["Rare", "Static"]:
            guidance.append("**Static dataset anonymization:** Use generalization and suppression on quasi-identifiers "
                            "(age ranges instead of exact ages, region instead of ZIP code). "
                            "Validate re-identification risk using the ARX anonymization tool.")

        # Re-identification warning
        guidance.append("**Re-identification risk:** Anonymization alone is increasingly insufficient. "
                        "Always perform a re-identification risk assessment before release. "
                        "Use prosecutor model (worst-case) risk metrics. If risk > 5%, apply additional suppression or DP.")

        if access == "Public":
            guidance.append("**Public release:** For public datasets, apply differential privacy on top of anonymization "
                            "as a defense-in-depth measure. Anonymization protects direct identifiers; "
                            "DP protects against statistical inference attacks.")

    return guidance


# -----------------------------
# MAIN BUTTON
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

    top_tech = None
    second_tech = None
    show_second = False

    if ranked:
        top_tech, top_score = ranked[0]
        st.success(f"🏆 Recommended: {top_tech}")

        if len(ranked) > 1:
            second_tech, second_score = ranked[1]
            if second_score >= top_score - 3:
                show_second = True
                st.info(f"Also consider: {second_tech}")

        # Explanations
        explanations = {
            "Local Differential Privacy": "Local Differential Privacy ensures data is privatized on the user's device before collection.",
            "Central Differential Privacy": "Central Differential Privacy collects raw data in a trusted server and adds noise to outputs.",
            "Cryptography": "Cryptography encrypts data to protect it in storage, transit, and computation.",
            "Anonymization": "Anonymization removes identifying information but can be vulnerable to re-identification.",
            "Confidential Computing": "Confidential Computing protects data during processing using secure hardware.",
            "Secure MPC": "Secure MPC allows multiple parties to compute jointly without sharing raw data."
        }

        st.subheader("🧠 Why this?")
        st.write(explanations.get(top_tech, ""))

        if show_second:
            st.subheader("🤔 Alternative Option")
            st.write(explanations.get(second_tech, ""))

    # -----------------------------
    # IMPLEMENTATION GUIDANCE (NEW)
    # -----------------------------
    if top_tech:
        st.subheader("🛠️ Implementation Guidance")
        st.write(f"Based on your specific answers, here is how to implement **{top_tech}** for your use case:")

        impl_guidance = get_implementation_guidance(
            top_tech, data_type_input, access_input, sharing_input, update_input,
            collection_input, trust_input, adversary_input, accuracy_input,
            budget_input, multi_input, threats_input, regulation_input
        )

        if impl_guidance:
            for item in impl_guidance:
                st.markdown(f"- {item}")
        else:
            st.write("No specific implementation notes for this configuration.")

        if show_second and second_tech:
            st.subheader(f"🛠️ Implementation Guidance: {second_tech} (Alternative)")
            alt_guidance = get_implementation_guidance(
                second_tech, data_type_input, access_input, sharing_input, update_input,
                collection_input, trust_input, adversary_input, accuracy_input,
                budget_input, multi_input, threats_input, regulation_input
            )
            if alt_guidance:
                for item in alt_guidance:
                    st.markdown(f"- {item}")

    # -----------------------------
    # HYBRID LAYER
    # -----------------------------
    st.subheader("➕ Recommended Add-ons")

    addons = []

    if top_tech and top_tech != "Cryptography":
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
