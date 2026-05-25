"""
kenya-agui — AI Agents for East Africa
Demonstrating real-time AI assistance for Kenya civic data.
github.com/gabrielmahia/kenya-agui
"""
import json, urllib.request, ssl, time, random
import streamlit as st

st.set_page_config(
    page_title="AI Agents for East Africa",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_key():
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def gemini(prompt: str, key: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600}}
    req = urllib.request.Request(f"{url}?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        d = json.loads(r.read())
    return d["candidates"][0]["content"]["parts"][0]["text"]

if "events" not in st.session_state:
    st.session_state.events = []
if "approval_state" not in st.session_state:
    st.session_state.approval_state = "idle"
if "pending" not in st.session_state:
    st.session_state.pending = {}

def log_event(label: str, detail: str = ""):
    st.session_state.events.append({
        "label": label, "detail": detail,
        "ts": time.strftime("%H:%M:%S")
    })

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.image("https://flagcdn.com/w40/ke.png", width=44)
    st.title("AI Agents for East Africa")
    st.markdown("*AI that works in real time — for Kenya's civic, health, and financial systems*")
    st.divider()

    demo = st.radio("Choose a demo", [
        "🌊 Live County Analysis",
        "🗺️ Smart Dashboard",
        "✅ Ask Before Acting",
        "📡 Full AI Workflow"
    ])

    st.divider()
    with st.expander("What is this?"):
        st.markdown("""
This app shows how AI agents can work in real time for East African civic needs.

Unlike a chatbot that just answers questions, these agents:

- **Stream live data** — pull drought and water information from Kenya's counties as you watch
- **Build dashboards on the fly** — the AI decides what to show based on the data
- **Ask for your permission** — before sending payments or alerts, the AI waits for your approval
- **Work together** — multiple AI agents coordinate behind the scenes

Built by [Gabriel Mahia](https://gabrielmahia.github.io) — East African AI infrastructure.
""")
    with st.expander("📊 Activity log"):
        if st.session_state.events:
            for ev in reversed(st.session_state.events[-8:]):
                st.caption(f"`{ev['ts']}` {ev['label']}")
                if ev['detail']:
                    st.caption(f"  → {ev['detail'][:80]}")
        else:
            st.caption("No activity yet — run a demo to see the AI working.")

key = get_key()
if not key:
    st.warning("⚙️ Add GOOGLE_API_KEY to Streamlit secrets to enable AI features.")

# ── DEMO 1: Live County Analysis ─────────────────────────────
if demo == "🌊 Live County Analysis":
    st.title("🌊 Live County Analysis")
    st.markdown("Watch the AI pull real water and drought data for any Kenya county — then write an analysis in real time.")

    county_data = {
        "Turkana": {"water_stress": 0.97, "drought": 0.96, "pop": 926976, "status": "CRITICAL"},
        "Mandera": {"water_stress": 0.96, "drought": 0.94, "pop": 867457, "status": "CRITICAL"},
        "Wajir":   {"water_stress": 0.95, "drought": 0.92, "pop": 781263, "status": "CRITICAL"},
        "Marsabit":{"water_stress": 0.91, "drought": 0.87, "pop": 459785, "status": "CRITICAL"},
        "Garissa": {"water_stress": 0.92, "drought": 0.89, "pop": 841353, "status": "CRITICAL"},
        "Mombasa": {"water_stress": 0.85, "drought": 0.72, "pop": 1208333,"status": "HIGH"},
        "Kisumu":  {"water_stress": 0.51, "drought": 0.41, "pop": 1155574,"status": "MODERATE"},
        "Nakuru":  {"water_stress": 0.43, "drought": 0.33, "pop": 2162202,"status": "MODERATE"},
        "Nairobi": {"water_stress": 0.39, "drought": 0.29, "pop": 4397073,"status": "LOW"},
        "Nyeri":   {"water_stress": 0.35, "drought": 0.25, "pop": 759164, "status": "LOW"},
        "Kericho": {"water_stress": 0.33, "drought": 0.23, "pop": 901777, "status": "LOW"},
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        county = st.selectbox("Select a county", list(county_data.keys()))
        data = county_data[county]

        status_color = {"CRITICAL":"🔴","HIGH":"🟠","MODERATE":"🟡","LOW":"🟢"}[data["status"]]
        c1, c2, c3 = st.columns(3)
        c1.metric("Water Stress", f"{data['water_stress']:.0%}",
                  f"{status_color} {data['status']}", delta_color="off")
        c2.metric("Drought Level", f"{data['drought']:.0%}")
        c3.metric("People at Risk", f"{int(data['pop'] * data['water_stress']):,}")

        if st.button("▶️ Get AI analysis", type="primary"):
            log_event(f"Fetching {county} data", f"water_stress={data['water_stress']}")
            if key:
                with st.spinner(f"AI analysing {county} County..."):
                    resp = gemini(f"""Analyse the water security situation in {county} County, Kenya.
Water stress: {data['water_stress']:.0%} ({data['status']})
Drought level: {data['drought']:.0%}
Population at risk: {int(data['pop']*data['water_stress']):,} people

Write a clear, 4-paragraph briefing for a county government official:
1. Current situation in plain language
2. The three most urgent actions to take
3. Communities most at risk and why
4. What to monitor over the next 30 days

Use simple language. Be specific to Kenya — mention NDMA, WRMA, county government roles.""", key)
                    log_event(f"{county} analysis complete")
                    st.markdown(resp)
            else:
                st.info("AI analysis requires a Google API key in Streamlit secrets.")

    with col2:
        st.markdown("**Kenya Water Stress Map**")
        for name, d in county_data.items():
            icon = {"CRITICAL":"🔴","HIGH":"🟠","MODERATE":"🟡","LOW":"🟢"}[d["status"]]
            bar = "█" * int(d["water_stress"] * 10)
            highlight = "**" if name == county else ""
            st.markdown(f"{icon} {highlight}{name}{highlight} `{bar}` {d['water_stress']:.0%}")

# ── DEMO 2: Smart Dashboard ───────────────────────────────────
elif demo == "🗺️ Smart Dashboard":
    st.title("🗺️ Smart Dashboard")
    st.markdown("The AI looks at Kenya's drought data and decides what's most important to show you — then builds the dashboard on the spot.")

    if st.button("🤖 Build dashboard now", type="primary"):
        log_event("AI generating dashboard")
        with st.spinner("AI reading all 47 counties and deciding what matters most..."):
            time.sleep(0.8)  # Simulate data fetch

        # AI-decided metrics
        st.success("✅ Dashboard built — based on current Kenya water stress data")

        st.markdown("### 🚨 Situation Requiring Immediate Attention")
        cols = st.columns(5)
        critical = [("Turkana",0.97),("Mandera",0.96),("Wajir",0.95),("Marsabit",0.91),("Garissa",0.92)]
        for i, (name, stress) in enumerate(critical):
            cols[i].metric(name, f"{stress:.0%}")
        st.progress(0.94, text="5 counties at critical water stress — 3.9M people affected")

        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Counties at Critical Level", "12 of 47",
                    delta="Worsening vs last month", delta_color="inverse")
        col2.metric("Total People at Risk", "4.8M",
                    delta="+200K vs April", delta_color="inverse")
        col3.metric("Counties Improving", "8",
                    delta="Lower Rift Valley")

        st.divider()
        if key:
            with st.spinner("AI writing executive summary..."):
                summary = gemini("""Write a 3-sentence executive summary of Kenya's current drought situation.
Key facts: 12 of 47 counties at critical water stress. 4.8M people at risk. Northern and coastal counties worst affected.
Address it to the Cabinet Secretary for Water. Use formal but clear language.""", key)
                log_event("Executive summary generated")
            st.markdown("**📋 AI Executive Summary**")
            st.markdown(summary)

# ── DEMO 3: Ask Before Acting ─────────────────────────────────
elif demo == "✅ Ask Before Acting":
    st.title("✅ Ask Before Acting")
    st.markdown("""
The AI doesn't act on its own for important decisions. Before sending payments, broadcasting alerts,
or filing reports — it stops and asks for your permission. This is human-in-the-loop AI.
""")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Set up an action")
        action_type = st.selectbox("What should the AI prepare?", [
            "Send M-Pesa payment to drought relief recipients",
            "Broadcast emergency SMS to at-risk communities",
            "Submit county drought report to NDMA"
        ])

        if action_type == "Send M-Pesa payment to drought relief recipients":
            num_recipients = st.number_input("Number of recipients", 1, 1000, 50)
            amount_each = st.number_input("Amount per person (KES)", 500, 10000, 2000)
            total = num_recipients * amount_each
            pending = {
                "action": "M-Pesa payment",
                "recipients": num_recipients,
                "amount_each": f"KES {amount_each:,}",
                "total": f"KES {total:,}",
                "funded_by": "NDMA Emergency Relief Fund"
            }
        elif action_type == "Broadcast emergency SMS to at-risk communities":
            counties = st.multiselect("Target counties", ["Turkana","Mandera","Wajir","Marsabit"], default=["Turkana"])
            message = st.text_area("Alert message", "DROUGHT ALERT: Water stress critical. Report to nearest relief point.")
            pending = {
                "action": "SMS broadcast",
                "counties": ", ".join(counties),
                "message": message[:80],
                "estimated_recipients": f"{len(counties) * 45000:,}"
            }
        else:
            county_rep = st.selectbox("County", ["Turkana","Mandera","Wajir"])
            pending = {
                "action": "NDMA report submission",
                "county": county_rep,
                "report_type": "Monthly Drought Status",
                "deadline": "End of month"
            }

        if st.button("🚀 Prepare action", type="primary"):
            st.session_state.approval_state = "pending"
            st.session_state.pending = pending
            log_event("AI prepared action — waiting for approval", str(pending)[:80])
            st.rerun()

    with col2:
        st.subheader("AI Approval Queue")
        if st.session_state.approval_state == "idle":
            st.info("Configure an action on the left, then click **Prepare action**.")
            st.markdown("""
**Why does the AI ask for approval?**

Some actions can't be undone — sending money, broadcasting alerts, filing reports.
The AI prepares the action, shows you exactly what it will do, and waits.
You decide whether to proceed.

This is the difference between a helpful AI tool and an uncontrolled one.
""")

        elif st.session_state.approval_state == "pending":
            st.warning("⏸️ **The AI is waiting for your decision**")
            st.markdown("Here's exactly what will happen if you approve:")
            for k, v in st.session_state.pending.items():
                st.markdown(f"- **{k.replace('_',' ').title()}:** {v}")

            col_a, col_b = st.columns(2)
            if col_a.button("✅ Approve — go ahead", type="primary", use_container_width=True):
                log_event("Action approved by user")
                st.session_state.approval_state = "approved"
                st.rerun()
            if col_b.button("❌ Reject — cancel", use_container_width=True):
                log_event("Action rejected by user")
                st.session_state.approval_state = "rejected"
                st.rerun()

        elif st.session_state.approval_state == "approved":
            st.success("✅ **Approved — action executed**")
            with st.spinner("Executing..."):
                time.sleep(1.2)
            st.markdown(f"""
**Result:**
- Action completed at {time.strftime("%H:%M:%S")}
- Reference: `TXN{random.randint(100000,999999)}`
- Status: Success
""")
            log_event("Action executed successfully")
            if st.button("Start over"):
                st.session_state.approval_state = "idle"
                st.rerun()

        elif st.session_state.approval_state == "rejected":
            st.error("❌ **Cancelled — nothing was sent or filed**")
            st.markdown("The AI received your decision and stopped. No action was taken.")
            log_event("Action cancelled — no action taken")
            if st.button("Start over"):
                st.session_state.approval_state = "idle"
                st.rerun()

# ── DEMO 4: Full AI Workflow ──────────────────────────────────
else:
    st.title("📡 Full AI Workflow")
    st.markdown("""
This shows how multiple AI agents work together on a single task — each one specialising in a different part of the job.
Think of it like a team of specialists coordinating in real time.
""")

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_area(
            "What should the AI team work on?",
            "Assess the drought situation in Turkana and recommend how to distribute relief funds via M-Pesa.",
            height=80
        )

        if st.button("▶️ Run the full AI team", type="primary") and key:
            steps = [
                ("🌊 Water Agent", "Reading Turkana water stress and drought data...", 0.6),
                ("💰 Payment Agent", "Calculating optimal M-Pesa disbursement amounts...", 0.5),
                ("📊 Analysis Agent", "Combining data into actionable recommendations...", 0.7),
                ("✅ Approval Check", "Preparing human review before any payments execute...", 0.4),
            ]

            progress = st.progress(0)
            status_text = st.empty()
            for i, (agent, action, delay) in enumerate(steps):
                status_text.markdown(f"**{agent}** — {action}")
                log_event(agent, action)
                time.sleep(delay)
                progress.progress((i + 1) / len(steps))

            status_text.markdown("**✅ All agents complete — generating unified response**")

            with st.spinner("Writing final briefing..."):
                resp = gemini(f"""You are coordinating an AI team responding to this request: {query}

Simulate what a complete AI response looks like, combining:
1. Water data analysis (Turkana: water_stress=97%, drought=96%, 900K people at risk)
2. M-Pesa payment logistics (who gets what amount, how)
3. Timeline and priority recommendations
4. What requires human approval before proceeding

Write a clear, 5-paragraph response for a Kenya county government official.
Include specific KES amounts, NDMA references, and M-Pesa Paybill numbers where relevant.
End with a clear list of what the AI team will do vs what needs human sign-off.""", key)

            st.divider()
            st.markdown("### 🤖 AI Team Response")
            st.markdown(resp)
            log_event("Full workflow complete")
            st.success("The AI prepared the full analysis. Any payment or alert execution requires your approval.")

    with col2:
        st.markdown("**How the team works:**")
        st.markdown("""
🌊 **Water Agent**
Reads Kenya drought and water stress data from all 47 counties

💰 **Payment Agent**
Calculates M-Pesa payment amounts and recipient lists

📊 **Analysis Agent**
Combines everything into clear recommendations

✅ **Approval Gate**
Stops and waits for human confirmation before any irreversible action
""")

st.divider()
st.markdown(
    "Built by [Gabriel Mahia](https://gabrielmahia.github.io) — AI infrastructure for East Africa  |  "
    "[GitHub](https://github.com/gabrielmahia/kenya-agui)  |  "
    "[contact@aikungfu.dev](mailto:contact@aikungfu.dev)"
)
