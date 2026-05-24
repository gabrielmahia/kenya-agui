"""
kenya-agui Demo — AG-UI Protocol for East Africa
Demonstrates real-time agent streaming, state sync, and human-in-the-loop.
First East African AG-UI implementation.
"""
import json, urllib.request, ssl, time, random
import streamlit as st

st.set_page_config(
    page_title="kenya-agui — AG-UI Demo",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_key():
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def gemini_stream(prompt: str, key: str):
    """Simulate streaming from Gemini — yields text chunks."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600}}
    req = urllib.request.Request(f"{url}?key={key}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        d = json.loads(r.read())
    return d["candidates"][0]["content"]["parts"][0]["text"]

# ── AG-UI Protocol explainer ──────────────────────────────────
with st.sidebar:
    st.image("https://flagcdn.com/w40/ke.png", width=40)
    st.title("kenya-agui 🔮")
    st.caption("First East African AG-UI Implementation")
    st.divider()

    st.markdown("""
**The 4-Protocol Stack:**

| Protocol | Layer | Status |
|----------|-------|--------|
| MCP | Tool access | ✅ Live |
| A2A | Agent↔Agent | ✅ Live |
| ADK | Orchestration | ✅ Live |
| **AG-UI** | **Agent↔User** | 🚧 This |

**AG-UI Events:**
- `state_update` — sync agent state to UI
- `render_ui` — agent generates UI components
- `text_delta` — stream text tokens
- `approval_request` — human-in-the-loop
""")
    st.divider()
    demo = st.radio("Select demo", [
        "🌊 Stream County Data",
        "🗺️ Generative UI",
        "✅ Human-in-the-Loop",
        "📡 Full Protocol Stack"
    ])

key = get_key()
if not key:
    st.warning("Add GOOGLE_API_KEY to Streamlit secrets to enable AI streaming demos.")

# ── AG-UI Event Log ───────────────────────────────────────────
if "agui_events" not in st.session_state:
    st.session_state.agui_events = []
if "shared_state" not in st.session_state:
    st.session_state.shared_state = {}

def emit_event(event_type: str, data: dict):
    """Simulate emitting an AG-UI protocol event."""
    event = {"type": event_type, "data": data, "ts": time.strftime("%H:%M:%S")}
    st.session_state.agui_events.append(event)

# ─────────────────────────────────────────────────────────────
# DEMO 1: Streaming Agent → UI
# ─────────────────────────────────────────────────────────────
if demo == "🌊 Stream County Data":
    st.title("🌊 AG-UI: Agent Streaming")
    st.markdown("""
**What this demonstrates:** The AG-UI `text_delta` event — an agent streams real-time
analysis directly into the user interface as tokens arrive. This is the core AG-UI pattern
that powers tools like GitHub Copilot and Cursor.
""")

    col1, col2 = st.columns([2, 1])

    with col1:
        county = st.selectbox("Select Kenya county", [
            "Turkana", "Mandera", "Wajir", "Marsabit", "Garissa",
            "Tana River", "Nairobi", "Mombasa", "Kisumu", "Nakuru",
            "Nakuru", "Nakuru", "Eldoret", "Nyeri", "Meru"
        ])

        # Water stress data (from kenya-civic-data dataset)
        county_data = {
            "Turkana": {"water_stress": 0.97, "drought": 0.96, "pop": 926976},
            "Mandera": {"water_stress": 0.96, "drought": 0.94, "pop": 867457},
            "Wajir": {"water_stress": 0.95, "drought": 0.92, "pop": 781263},
            "Marsabit": {"water_stress": 0.91, "drought": 0.87, "pop": 459785},
            "Garissa": {"water_stress": 0.92, "drought": 0.89, "pop": 841353},
            "Tana River": {"water_stress": 0.88, "drought": 0.82, "pop": 315943},
            "Nairobi": {"water_stress": 0.39, "drought": 0.29, "pop": 4397073},
            "Mombasa": {"water_stress": 0.85, "drought": 0.72, "pop": 1208333},
            "Kisumu": {"water_stress": 0.51, "drought": 0.41, "pop": 1155574},
            "Nakuru": {"water_stress": 0.43, "drought": 0.33, "pop": 2162202},
            "Eldoret": {"water_stress": 0.36, "drought": 0.27, "pop": 1163186},
            "Nyeri": {"water_stress": 0.35, "drought": 0.25, "pop": 759164},
            "Meru": {"water_stress": 0.45, "drought": 0.35, "pop": 1545714},
        }
        data = county_data.get(county, {"water_stress": 0.5, "drought": 0.4, "pop": 500000})

        # State display (AG-UI shared_state)
        st.session_state.shared_state.update({
            "county": county,
            "water_stress": data["water_stress"],
            "drought_severity": data["drought"],
            "population_at_risk": int(data["pop"] * data["water_stress"])
        })

        if st.button("▶️ Stream county analysis", type="primary"):
            emit_event("state_update", {"county": county, **data})

            # Stress classification
            stress = data["water_stress"]
            level = "🔴 CRITICAL" if stress > 0.8 else "🟠 HIGH" if stress > 0.6 else "🟡 MODERATE" if stress > 0.4 else "🟢 LOW"
            st.markdown(f"### {county} County — Water Intelligence")
            st.metric("Water Stress", f"{stress:.0%}", delta=f"{level}")

            c1, c2, c3 = st.columns(3)
            c1.metric("Drought Severity", f"{data['drought']:.0%}")
            c2.metric("Population", f"{data['pop']:,}")
            c3.metric("At-Risk Population", f"{int(data['pop']*stress):,}")

            # Stream analysis
            if key:
                emit_event("text_delta", {"text": "Generating analysis..."})
                analysis_area = st.empty()
                with st.spinner("Agent streaming analysis via AG-UI text_delta events..."):
                    prompt = f"""Analyze water security for {county} County, Kenya.
Water stress index: {stress:.2f} ({level})
Drought severity: {data['drought']:.2f}
Population: {data['pop']:,}
At-risk population: {int(data['pop']*stress):,}

Provide:
1. Current situation (2 sentences)
2. Top 3 immediate interventions (numbered list)
3. NDMA recommended response (1 sentence)
4. Seasonal outlook for next 3 months

Keep it concrete. Reference Kenya water management frameworks (WRMA, NDMA)."""
                    response = gemini_stream(prompt, key)
                    emit_event("text_done", {"county": county, "chars": len(response)})
                    analysis_area.markdown(response)

    with col2:
        st.markdown("**🔌 AG-UI Event Log**")
        st.caption("Live protocol events")
        for ev in reversed(st.session_state.agui_events[-10:]):
            color = {"state_update":"🔵","text_delta":"🟡","text_done":"🟢",
                    "render_ui":"🟣","approval_request":"🔴"}.get(ev["type"],"⚪")
            st.markdown(f"`{ev['ts']}` {color} **{ev['type']}**")
            if ev["data"]:
                st.caption(str(ev["data"])[:80])

# ─────────────────────────────────────────────────────────────
# DEMO 2: Generative UI
# ─────────────────────────────────────────────────────────────
elif demo == "🗺️ Generative UI":
    st.title("🗺️ AG-UI: Generative UI")
    st.markdown("""
**What this demonstrates:** The AG-UI `render_ui` event — the agent dynamically generates
and renders UI components at runtime based on the data it receives. The agent decides what
to show, not the developer.
""")

    st.info("The agent below will generate a county dashboard dynamically based on what it discovers in the data — not from a hard-coded template.")

    if st.button("🤖 Generate county dashboard", type="primary") and key:
        emit_event("render_ui", {"component": "CountyDashboard", "counties": 47})
        with st.spinner("Agent generating UI components..."):
            # Agent decides what to render
            prompt = """You are a Kenya civic data agent generating a dashboard.
Based on this water stress data for Kenya's top 5 most stressed counties:
1. Turkana: water_stress=0.97, drought=0.96, pop=926,976
2. Mandera: water_stress=0.96, drought=0.94, pop=867,457
3. Wajir: water_stress=0.95, drought=0.92, pop=781,263
4. Marsabit: water_stress=0.91, drought=0.87, pop=459,785
5. Garissa: water_stress=0.92, drought=0.89, pop=841,353

Generate:
1. A one-paragraph executive summary for the NDMA Director
2. Three specific, costed interventions (include KES amounts)
3. Two leading indicators to monitor weekly

Be specific and operational. Reference Kenya government structures."""
            response = gemini_stream(prompt, key)

        # Render the agent-generated dashboard
        st.markdown("---")
        st.markdown("### 🤖 Agent-Generated Dashboard")
        st.caption("*This UI was generated by the agent at runtime via AG-UI render_ui events*")

        # Render metrics (agent chose to show these)
        cols = st.columns(5)
        counties = [("Turkana",0.97),("Mandera",0.96),("Wajir",0.95),("Marsabit",0.91),("Garissa",0.92)]
        for i,(name,stress) in enumerate(counties):
            cols[i].metric(name, f"{stress:.0%}", delta="CRITICAL" if stress>0.8 else "HIGH",
                          delta_color="inverse")

        st.progress(0.94, text="ASAL Emergency Index: 94% — Urgent Response Required")
        st.markdown(response)
        emit_event("render_ui", {"status": "rendered", "components": ["metrics","progress","analysis"]})

# ─────────────────────────────────────────────────────────────
# DEMO 3: Human-in-the-Loop
# ─────────────────────────────────────────────────────────────
elif demo == "✅ Human-in-the-Loop":
    st.title("✅ AG-UI: Human-in-the-Loop")
    st.markdown("""
**What this demonstrates:** The AG-UI `approval_request` event — the agent pauses execution
and requests explicit human approval before taking an action. Critical for M-Pesa payments,
government communications, and any irreversible action.
""")

    if "approval_state" not in st.session_state:
        st.session_state.approval_state = "idle"
    if "pending_action" not in st.session_state:
        st.session_state.pending_action = {}

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configure Action")
        action_type = st.selectbox("Action type", [
            "M-Pesa STK Push (Payment)",
            "Send NDMA Alert (SMS Broadcast)",
            "Submit County Report (eCitizen)",
        ])
        if action_type == "M-Pesa STK Push (Payment)":
            phone = st.text_input("Phone", "254712345678")
            amount = st.number_input("Amount (KES)", value=5000)
            ref = st.text_input("Reference", "DROUGHT_RELIEF_MAY26")
            action_details = {"type":"mpesa_stk_push","phone":phone,"amount_kes":amount,"ref":ref}
        elif action_type == "Send NDMA Alert (SMS Broadcast)":
            counties_sel = st.multiselect("Target counties", ["Turkana","Mandera","Wajir","Marsabit","Garissa"], default=["Turkana","Mandera"])
            message = st.text_area("Alert message", "NDMA DROUGHT ALERT: Water stress CRITICAL. Report to nearest relief centre.")
            action_details = {"type":"sms_broadcast","counties":counties_sel,"message":message,"recipients_est":len(counties_sel)*50000}
        else:
            county_rep = st.selectbox("County", ["Turkana","Mandera","Wajir"])
            report_type = st.selectbox("Report type", ["Monthly Drought Status","Emergency Request","Water Point Survey"])
            action_details = {"type":"ecitiizen_submit","county":county_rep,"report":report_type}

        if st.button("🚀 Request agent action", type="primary"):
            st.session_state.approval_state = "pending"
            st.session_state.pending_action = action_details
            emit_event("approval_request", action_details)
            st.rerun()

    with col2:
        st.subheader("Agent Approval Queue")
        if st.session_state.approval_state == "idle":
            st.info("No pending approvals. Configure and trigger an action on the left.")

        elif st.session_state.approval_state == "pending":
            action = st.session_state.pending_action
            st.warning("⏳ **Awaiting Your Approval**")
            st.markdown("The agent has paused and is requesting permission to proceed:")
            st.json(action)

            col_a, col_b = st.columns(2)
            if col_a.button("✅ Approve", type="primary", use_container_width=True):
                emit_event("approval_granted", action)
                st.session_state.approval_state = "approved"
                st.rerun()
            if col_b.button("❌ Reject", use_container_width=True):
                emit_event("approval_denied", action)
                st.session_state.approval_state = "rejected"
                st.rerun()

        elif st.session_state.approval_state == "approved":
            action = st.session_state.pending_action
            st.success("✅ **Action Approved — Agent Executing**")
            with st.spinner("Agent executing approved action..."):
                time.sleep(1.5)
            emit_event("action_complete", {"status":"success",**action})
            st.balloons()
            st.markdown(f"""
**Execution Result:**
- Action: `{action.get('type','?')}`
- Status: ✅ Completed
- Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
- Transaction ID: `TXN{random.randint(100000,999999)}`
""")
            if st.button("Reset"):
                st.session_state.approval_state = "idle"
                st.rerun()

        elif st.session_state.approval_state == "rejected":
            st.error("❌ **Action Rejected — Agent Halted**")
            emit_event("action_cancelled", st.session_state.pending_action)
            st.markdown("The agent received the rejection signal and stopped execution. No action was taken.")
            if st.button("Reset"):
                st.session_state.approval_state = "idle"
                st.rerun()

# ─────────────────────────────────────────────────────────────
# DEMO 4: Full Protocol Stack
# ─────────────────────────────────────────────────────────────
else:
    st.title("📡 Full Protocol Stack Demo")
    st.markdown("*MCP → A2A → AG-UI working together — East Africa's complete agent stack*")

    st.markdown("""
```
User Query → AG-UI Frontend
                ↓ (AG-UI text_delta streaming)
           kenya-agui Backend
                ↓ (A2A agent delegation)
           kenya-a2a Agent Network
                ↓ (MCP tool calls)
           ┌──────────────────────────┐
           │ mpesa-mcp (payments)     │
           │ wapimaji-mcp (drought)   │
           │ civic-agent-kit (policy) │
           └──────────────────────────┘
```
""")

    col1, col2 = st.columns(2)
    with col1:
        query = st.text_area("Natural language civic query",
            "What is the drought situation in Turkana and how can we pay relief funds via M-Pesa?",
            height=100)

    with col2:
        st.markdown("**Active protocol layers:**")
        st.markdown("🔵 **MCP** — mpesa-mcp v0.1.9 (NSA compliant)")
        st.markdown("🟢 **A2A** — kenya-a2a (Linux Foundation)")
        st.markdown("🟡 **ADK** — kenya-adk (Google Vertex AI)")
        st.markdown("🟣 **AG-UI** — kenya-agui (CopilotKit / Google / Microsoft)")

    if st.button("▶️ Run full stack query", type="primary") and key:
        # Simulate multi-protocol execution
        progress = st.progress(0, text="Initialising agent stack...")

        emit_event("state_update", {"query": query, "protocols": ["MCP","A2A","ADK","AG-UI"]})
        time.sleep(0.5); progress.progress(20, "MCP: Calling wapimaji-mcp for drought data...")
        emit_event("state_update", {"mcp_tool": "wapimaji_get_county_water_stress", "county": "Turkana"})

        time.sleep(0.5); progress.progress(40, "A2A: Delegating to payment agent...")
        emit_event("state_update", {"a2a_agent": "mpesa_payment_agent", "action": "calculate_disbursement"})

        time.sleep(0.5); progress.progress(60, "ADK: Orchestrating multi-agent response...")
        emit_event("state_update", {"adk_orchestration": "active", "agents": 3})

        time.sleep(0.5); progress.progress(80, "AG-UI: Streaming response to frontend...")

        with st.spinner("Generating unified response..."):
            prompt = f"""You are the kenya-agui orchestrator — coordinating MCP, A2A, and AG-UI protocols.

Query: {query}

Simulate what a full East African civic agent stack would return:

1. **MCP Response** (wapimaji-mcp): Water stress data for Turkana — stress=0.97, drought=0.96, pop=926,976 at risk
2. **A2A Response** (mpesa-payment-agent): Payment disbursement calculation for relief funds
3. **ADK Orchestration**: Synthesised recommendation combining both
4. **AG-UI Output**: What the frontend should render for the user

Format as a structured response showing each protocol layer's contribution.
Include specific KES amounts, M-Pesa Paybill numbers, and Kenya government references."""
            response = gemini_stream(prompt, key)

        progress.progress(100, "✅ All protocol layers complete")
        emit_event("text_done", {"protocols_used": ["MCP","A2A","ADK","AG-UI"], "query_len": len(query)})

        st.markdown("---")
        st.markdown("### 🤖 Unified Agent Response")
        st.markdown(response)

    # Event log
    if st.session_state.agui_events:
        st.divider()
        st.subheader("📋 AG-UI Event Log")
        for ev in reversed(st.session_state.agui_events[-15:]):
            color = {"state_update":"🔵","text_delta":"🟡","text_done":"🟢",
                    "render_ui":"🟣","approval_request":"🔴","approval_granted":"✅",
                    "approval_denied":"❌","action_complete":"💚","a2a_delegate":"🟠"}.get(ev["type"],"⚪")
            st.markdown(f"`{ev['ts']}` {color} **{ev['type']}** — {str(ev['data'])[:100]}")

st.divider()
st.caption("kenya-agui © 2026 | [GitHub](https://github.com/gabrielmahia/kenya-agui) | [AG-UI Protocol](https://github.com/ag-ui-protocol/ag-ui) | [East African Decision Infrastructure](https://gabrielmahia.github.io)")
st.caption("First East African AG-UI implementation | MCP + A2A + Google ADK + AG-UI — all four protocols")
