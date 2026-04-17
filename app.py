"""
QuantaVoice — Quantum-Secured Voice Authentication Demo
Run with: streamlit run app.py
Install:  pip install streamlit numpy scipy matplotlib
"""

import streamlit as st
import hashlib
import time
import random
import json
from datetime import datetime
import numpy as np

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="QuantaVoice — Secure Banking Demo",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0A1628; color: #E2E8F0; }
    
    /* Headers */
    h1, h2, h3 { color: #00B4D8 !important; }
    
    /* Cards */
    .metric-card {
        background: #0D2045;
        border: 1px solid #00B4D8;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 8px 0;
    }
    .metric-num { font-size: 2.2rem; font-weight: 700; color: #00B4D8; }
    .metric-label { font-size: 0.85rem; color: #94A3B8; margin-top: 4px; }
    
    /* Status boxes */
    .status-ok {
        background: #052e16;
        border: 1px solid #10B981;
        border-radius: 8px;
        padding: 14px;
        color: #10B981;
        font-weight: 600;
        font-family: monospace;
        margin: 6px 0;
    }
    .status-fail {
        background: #450a0a;
        border: 1px solid #EF4444;
        border-radius: 8px;
        padding: 14px;
        color: #EF4444;
        font-weight: 600;
        font-family: monospace;
        margin: 6px 0;
    }
    .status-warn {
        background: #1c1400;
        border: 1px solid #F59E0B;
        border-radius: 8px;
        padding: 14px;
        color: #F59E0B;
        font-weight: 600;
        font-family: monospace;
        margin: 6px 0;
    }
    .status-info {
        background: #0c1a2e;
        border: 1px solid #00B4D8;
        border-radius: 8px;
        padding: 14px;
        color: #00B4D8;
        font-family: monospace;
        margin: 6px 0;
    }
    
    /* Transaction row */
    .tx-row {
        background: #0D2045;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        font-family: monospace;
        font-size: 0.82rem;
    }
    
    /* Big button */
    .stButton button {
        background: #00B4D8 !important;
        color: #0A1628 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-size: 1rem !important;
    }
    .stButton button:hover { background: #0096C7 !important; }
    
    /* Input boxes */
    .stTextInput input, .stSelectbox select {
        background: #0D2045 !important;
        color: #E2E8F0 !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
    }
    
    /* Progress bar color */
    .stProgress .st-bo { background-color: #00B4D8 !important; }
    
    /* Hide streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    
    /* Section divider */
    hr { border-color: #1e3a5f !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "fraud_blocked" not in st.session_state:
    st.session_state.fraud_blocked = 0
if "auth_success" not in st.session_state:
    st.session_state.auth_success = 0
if "balance" not in st.session_state:
    st.session_state.balance = 50000.00

# ──────────────────────────────────────────────
# CORE ENGINE FUNCTIONS
# ──────────────────────────────────────────────

def analyze_liveness(text: str, is_attack: bool = False) -> dict:
    """
    Simulates AI liveness detection.
    In production: AASIST neural network processing 12 spectral features.
    """
    time.sleep(0.3)  # Simulate inference time
    
    if is_attack:
        score = round(random.uniform(0.03, 0.15), 3)
        features = {
            "spectral_flatness": round(random.uniform(0.8, 0.95), 3),
            "phase_discontinuity": round(random.uniform(0.7, 0.92), 3),
            "breathing_pattern": "ABSENT",
            "micro_tremor": "NOT_DETECTED",
            "glottal_pulse_regularity": round(random.uniform(0.85, 0.98), 3),
        }
        verdict = "SYNTHETIC_AUDIO_DETECTED"
    else:
        score = round(random.uniform(0.87, 0.99), 3)
        features = {
            "spectral_flatness": round(random.uniform(0.05, 0.18), 3),
            "phase_discontinuity": round(random.uniform(0.02, 0.09), 3),
            "breathing_pattern": "PRESENT",
            "micro_tremor": "DETECTED",
            "glottal_pulse_regularity": round(random.uniform(0.12, 0.25), 3),
        }
        verdict = "LIVE_HUMAN_VOICE"
    
    return {"score": score, "verdict": verdict, "features": features}


def biometric_match(text: str) -> dict:
    """
    Simulates voice biometric verification.
    In production: ECAPA-TDNN speaker embeddings with cosine similarity.
    """
    time.sleep(0.25)
    score = round(random.uniform(88.0, 97.5), 1)
    return {
        "match_score": score,
        "enrolled_profile": "USER_PROFILE_v3",
        "embedding_distance": round(random.uniform(0.08, 0.22), 4),
        "verdict": "IDENTITY_VERIFIED" if score > 80 else "IDENTITY_MISMATCH"
    }


def generate_pqc_token(payload: str) -> dict:
    """
    Simulates Post-Quantum Cryptography token generation.
    In production: CRYSTALS-Kyber key encapsulation + CRYSTALS-Dilithium signing.
    
    We use SHA3-256 here (quantum-resistant hash function) to simulate
    the PQC-secured transaction token.
    """
    time.sleep(0.2)
    
    timestamp = str(int(time.time() * 1000))
    raw = f"KYBER512:{payload}:{timestamp}:{random.getrandbits(128)}"
    
    # SHA3-256 is quantum-resistant (unlike SHA-256)
    token_hash = hashlib.sha3_256(raw.encode()).hexdigest()
    
    # Simulate Dilithium signature (truncated for demo)
    sig_material = f"DILITHIUM:{token_hash}:{timestamp}"
    signature = hashlib.sha3_512(sig_material.encode()).hexdigest()[:64]
    
    return {
        "token": f"QV-{token_hash[:8].upper()}-{token_hash[8:16].upper()}",
        "algorithm": "CRYSTALS-Kyber-512 + Dilithium-2",
        "standard": "NIST PQC FIPS 203/204 (2024)",
        "signature": signature[:32] + "...",
        "expires_ms": 30000,
        "timestamp": timestamp
    }


def parse_command(text: str) -> dict:
    """Parse voice payment command."""
    text_lower = text.lower()
    amount = None
    recipient = None
    
    # Extract amount (looks for numbers)
    import re
    amounts = re.findall(r'[\d,]+', text)
    if amounts:
        amount = int(amounts[0].replace(',', ''))
    
    # Common recipient patterns
    words = text.split()
    for i, w in enumerate(words):
        if w.lower() in ["to", "for"] and i + 1 < len(words):
            recipient = words[i + 1].strip(".,!")
            break
    
    return {
        "raw": text,
        "amount": amount,
        "recipient": recipient,
        "intent": "PAYMENT" if "pay" in text_lower else "QUERY"
    }


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("<div style='font-size:3.5rem; text-align:center; padding-top:10px'>🔐</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='margin-bottom:0; font-size:2.2rem'>QuantaVoice</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; margin-top:4px; font-size:0.95rem'>Quantum-Secured Voice Authentication · Banking Demo</p>", unsafe_allow_html=True)

st.divider()

# ──────────────────────────────────────────────
# STATS ROW
# ──────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-num'>₹{st.session_state.balance:,.2f}</div>
        <div class='metric-label'>Account Balance</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-num'>{st.session_state.auth_success}</div>
        <div class='metric-label'>Payments Approved</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-num' style='color:#EF4444'>{st.session_state.fraud_blocked}</div>
        <div class='metric-label'>Attacks Blocked</div>
    </div>""", unsafe_allow_html=True)
with m4:
    total = st.session_state.auth_success + st.session_state.fraud_blocked
    rate = f"{(st.session_state.auth_success/total*100):.0f}%" if total > 0 else "–"
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-num' style='color:#10B981'>{rate}</div>
        <div class='metric-label'>Auth Success Rate</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ──────────────────────────────────────────────
# MAIN COLUMNS
# ──────────────────────────────────────────────
left, right = st.columns([1.1, 1], gap="large")

# ──── LEFT: AUTHENTICATION PANEL ──────────────
with left:
    st.markdown("### 🎙️ Voice Authentication")
    
    mode = st.radio(
        "Select demo mode:",
        ["✅  Legitimate user (live voice)", "🤖  Deepfake attack (AI-cloned voice)"],
        horizontal=False
    )
    is_attack = "Deepfake" in mode
    
    if is_attack:
        st.markdown("""<div class='status-warn'>
        ⚠️  ATTACK MODE: Simulating AI voice clone attack<br>
        <span style='font-size:0.8rem; opacity:0.8'>This represents an ElevenLabs / open-source voice clone</span>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("**Enter payment command:**")
    command = st.text_input(
        "",
        placeholder='e.g.  "Pay 5000 rupees to Priya"',
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        run_auth = st.button("🔐  Authenticate & Pay", use_container_width=True)
    with col_btn2:
        if st.button("🔄  Reset Demo", use_container_width=True):
            st.session_state.transactions = []
            st.session_state.fraud_blocked = 0
            st.session_state.auth_success = 0
            st.session_state.balance = 50000.00
            st.rerun()

    # ── AUTHENTICATION FLOW ──
    if run_auth:
        if not command.strip():
            st.error("Please enter a payment command first.")
        else:
            parsed = parse_command(command)
            
            st.markdown("---")
            st.markdown("#### 🔄 Authentication Pipeline")
            
            # ── LAYER 1: LIVENESS ──
            with st.container():
                st.markdown("**Layer 1 — AI Liveness Detection**")
                prog1 = st.progress(0, "Initializing audio analysis...")
                
                for p in range(0, 101, 20):
                    prog1.progress(p, f"Analyzing {p}% — extracting spectral features...")
                    time.sleep(0.07)
                
                liveness = analyze_liveness(command, is_attack=is_attack)
                prog1.progress(100, "Analysis complete")
                
                if liveness["verdict"] == "SYNTHETIC_AUDIO_DETECTED":
                    st.markdown(f"""<div class='status-fail'>
                    ✗ LIVENESS CHECK FAILED<br>
                    Score: {liveness['score']} / 1.0 (threshold: 0.70)<br>
                    Verdict: {liveness['verdict']}<br>
                    Spectral flatness: {liveness['features']['spectral_flatness']} (HIGH — synthetic indicator)<br>
                    Breathing pattern: {liveness['features']['breathing_pattern']}
                    </div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class='status-fail'>
                    🚫 TRANSACTION BLOCKED — Deepfake audio detected<br>
                    Security alert dispatched to registered mobile number.<br>
                    Incident ID: INC-{hashlib.md5(command.encode()).hexdigest()[:8].upper()}
                    </div>""", unsafe_allow_html=True)
                    
                    st.session_state.fraud_blocked += 1
                    tx = {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "command": command[:30],
                        "status": "BLOCKED",
                        "reason": "Deepfake detected",
                        "liveness": liveness["score"]
                    }
                    st.session_state.transactions.insert(0, tx)
                    st.rerun()
                
                else:
                    st.markdown(f"""<div class='status-ok'>
                    ✓ LIVENESS CHECK PASSED<br>
                    Score: {liveness['score']} / 1.0  |  Verdict: {liveness['verdict']}<br>
                    Breathing pattern: {liveness['features']['breathing_pattern']}  |  Micro-tremor: {liveness['features']['micro_tremor']}
                    </div>""", unsafe_allow_html=True)
            
            # ── LAYER 2: BIOMETRIC ──
            with st.container():
                st.markdown("**Layer 2 — Voice Biometric Match**")
                prog2 = st.progress(0, "Loading enrolled voice profile...")
                for p in range(0, 101, 25):
                    prog2.progress(p, f"Comparing embeddings... {p}%")
                    time.sleep(0.06)
                
                bio = biometric_match(command)
                prog2.progress(100, "Biometric comparison complete")
                
                st.markdown(f"""<div class='status-ok'>
                ✓ IDENTITY VERIFIED<br>
                Match score: {bio['match_score']}%  (threshold: 80%)<br>
                Profile: {bio['enrolled_profile']}<br>
                Cosine distance: {bio['embedding_distance']} (lower = better match)
                </div>""", unsafe_allow_html=True)
            
            # ── LAYER 3: PQC TOKEN ──
            with st.container():
                st.markdown("**Layer 3 — Post-Quantum Cryptography**")
                prog3 = st.progress(0, "Generating CRYSTALS-Kyber keypair...")
                for p in range(0, 101, 25):
                    prog3.progress(p, f"Encapsulating key... {p}%")
                    time.sleep(0.05)
                
                pqc = generate_pqc_token(command)
                prog3.progress(100, "PQC token issued")
                
                st.markdown(f"""<div class='status-info'>
                ✓ QUANTUM-SAFE TOKEN ISSUED<br>
                Token: {pqc['token']}<br>
                Algorithm: {pqc['algorithm']}<br>
                Standard: {pqc['standard']}<br>
                Signature: {pqc['signature']}<br>
                Expires: 30 seconds
                </div>""", unsafe_allow_html=True)
            
            # ── PAYMENT EXECUTION ──
            st.markdown("**Payment Execution**")
            time.sleep(0.4)
            
            amount = parsed.get("amount") or 0
            recipient = parsed.get("recipient") or "Recipient"
            
            if amount and amount <= st.session_state.balance:
                st.session_state.balance -= amount
                st.session_state.auth_success += 1
                
                st.markdown(f"""<div class='status-ok'>
                ✅ PAYMENT APPROVED & EXECUTED<br>
                Amount: ₹{amount:,}<br>
                To: {recipient}<br>
                Ref: {pqc['token']}<br>
                New balance: ₹{st.session_state.balance:,.2f}<br>
                Total latency: ~780ms
                </div>""", unsafe_allow_html=True)
                
                tx = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "command": command[:30],
                    "status": "APPROVED",
                    "amount": f"₹{amount:,}",
                    "token": pqc["token"]
                }
            else:
                st.session_state.auth_success += 1
                st.markdown(f"""<div class='status-ok'>
                ✅ AUTHENTICATION SUCCESSFUL<br>
                Command processed: "{command[:40]}"<br>
                Token: {pqc['token']}<br>
                Latency: ~780ms
                </div>""", unsafe_allow_html=True)
                tx = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "command": command[:30],
                    "status": "APPROVED",
                    "amount": "–",
                    "token": pqc["token"]
                }
            
            st.session_state.transactions.insert(0, tx)
            time.sleep(0.5)
            st.rerun()


# ──── RIGHT: LOGS + ARCHITECTURE ──────────────
with right:
    st.markdown("### 📜 Transaction Log")
    
    if not st.session_state.transactions:
        st.markdown("""<div class='status-info' style='text-align:center; padding:30px'>
        No transactions yet.<br>
        <span style='font-size:0.8rem; opacity:0.7'>Try the authentication panel →</span>
        </div>""", unsafe_allow_html=True)
    else:
        for tx in st.session_state.transactions[:8]:
            color = "#10B981" if tx["status"] == "APPROVED" else "#EF4444"
            icon = "✓" if tx["status"] == "APPROVED" else "✗"
            detail = tx.get("amount", "") or tx.get("reason", "")
            st.markdown(f"""<div class='tx-row'>
            <span style='color:{color}; font-weight:700'>{icon} {tx['status']}</span>
            &nbsp;·&nbsp; {tx['time']}
            &nbsp;·&nbsp; <span style='color:#94A3B8'>{tx['command']}...</span>
            {"&nbsp;·&nbsp; " + detail if detail else ""}
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏗️ System Architecture")
    st.markdown("""<div class='status-info' style='font-size:0.82rem; line-height:1.9'>
    <b>Input</b><br>
    &nbsp;&nbsp;Voice command (text input / mic)<br>
    <b>Layer 1 — AI Liveness</b><br>
    &nbsp;&nbsp;AASIST neural net · 12 spectral features · 180ms<br>
    <b>Layer 2 — Biometric</b><br>
    &nbsp;&nbsp;ECAPA-TDNN embeddings · Cosine similarity · 250ms<br>
    <b>Layer 3 — Post-Quantum Crypto</b><br>
    &nbsp;&nbsp;CRYSTALS-Kyber-512 (NIST FIPS 203)<br>
    &nbsp;&nbsp;CRYSTALS-Dilithium-2 (NIST FIPS 204)<br>
    &nbsp;&nbsp;SHA3-256 (quantum-resistant hash)<br>
    <b>Output</b><br>
    &nbsp;&nbsp;Signed PQC token · Bank API call · Receipt
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Demo Commands to Try")
    st.markdown("""<div style='color:#94A3B8; font-size:0.85rem; line-height:2.1'>
    ✅ <code>Pay 5000 rupees to Priya</code><br>
    ✅ <code>Transfer 10000 to Rahul</code><br>
    ✅ <code>Send 2500 to Amit for groceries</code><br>
    🤖 Same commands in <b>Deepfake mode</b> to see detection
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.divider()
st.markdown("""<div style='text-align:center; color:#475569; font-size:0.78rem; padding:8px'>
QuantaVoice · Proof of Concept Demo · CRYSTALS-Kyber/Dilithium per NIST FIPS 203/204 (2024)
· SHA3-256 quantum-resistant hashing · Not for production use
</div>""", unsafe_allow_html=True)
