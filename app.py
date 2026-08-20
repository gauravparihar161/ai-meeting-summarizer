import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="AI Meeting & Content Summarizer Engine",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS Stylesheet
def load_css(file_path="styles.css"):
    try:
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("`styles.css` file not found. Please create it in the root directory.")

load_css("styles.css")

# 1. TOP HERO HEADER
st.markdown("""
<div class="hero-header">
    <div class="hero-title">✨ AI Content & Meeting Summarizer Engine</div>
    <div class="hero-subtitle">Transform audio & video recordings into structured summaries, key takeaways, decisions, and action items instantly.</div>
</div>
""", unsafe_allow_html=True)

# 2. MAIN IMPLEMENTATION SECTION
tab1, tab2 = st.tabs(["🚀 Process New Media", "📜 Processing History Log"])

# --- TAB 1: MEDIA UPLOADER & ANALYSIS ---
with tab1:
    col_upload, col_side = st.columns([2.5, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Audio or Video File",
            type=["mp3", "wav", "m4a", "ogg", "mp4", "mkv", "mov", "avi"],
            help="Supported: MP3, WAV, M4A, OGG, MP4, MKV, MOV, AVI"
        )

    with col_side:
        st.markdown("""
        <div class="stat-badge">
            <div class="stat-label">AI Engine Stack</div>
            <div class="stat-number">Groq + Whisper-v3</div>
            <div style="font-size: 0.85rem; color: #10b981; font-weight: 600; margin-top: 4px;">⚡ Real-time Processing</div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:
        st.write("")
        if st.button("🚀 Analyze Media File", type="primary", use_container_width=True):
            with st.status("⚡ Engine Processing Payload...", expanded=True) as status:
                st.write("📥 Preparing file upload...")
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                st.write("🎬 Compressing & extracting audio with FFmpeg...")
                try:
                    res = requests.post("http://localhost:8000/api/v1/process-audio", files=files)

                    if res.status_code == 200:
                        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                        data = res.json()
                        analysis = data.get("analysis", {})

                        st.divider()

                        # Category & File Badges
                        s1, s2, s3 = st.columns(3)
                        with s1:
                            st.markdown(f"""
                            <div class="stat-badge">
                                <div class="stat-label">Processed File</div>
                                <div style="font-weight: 600; color: #1e293b; font-size: 1.05rem; margin-top:4px;">{data.get('filename')}</div>
                            </div>""", unsafe_allow_html=True)
                        with s2:
                            category = analysis.get('category', 'meeting').upper()
                            st.markdown(f"""
                            <div class="stat-badge">
                                <div class="stat-label">Detected Category</div>
                                <div class="stat-number" style="font-size: 1.2rem; color: #4f46e5;">📌 {category}</div>
                            </div>""", unsafe_allow_html=True)
                        with s3:
                            action_count = len(analysis.get('action_items', []))
                            takeaways_count = len(analysis.get('key_takeaways', []))
                            stat_label = "Key Takeaways" if takeaways_count > 0 else "Action Items"
                            stat_value = takeaways_count if takeaways_count > 0 else action_count
                            
                            st.markdown(f"""
                            <div class="stat-badge">
                                <div class="stat-label">{stat_label}</div>
                                <div class="stat-number" style="color:#10b981;">{stat_value}</div>
                            </div>""", unsafe_allow_html=True)

                        st.write("")

                        # Executive Summary
                        st.markdown("""
                        <div class="info-card">
                            <h3 style="margin-top:0; color:#4f46e5; font-size:1.3rem;">📌 Executive Summary</h3>
                        """, unsafe_allow_html=True)
                        st.write(analysis.get("summary") or analysis.get("executive_summary") or "No summary generated.")
                        st.markdown("</div>", unsafe_allow_html=True)

                        # Key Takeaways Section (Rendered for tutorials, presentations, or general guides)
                        key_takeaways = analysis.get("key_takeaways") or []
                        if key_takeaways:
                            st.markdown("""
                            <div class="info-card">
                                <h3 style="margin-top:0; color:#d97706; font-size:1.2rem;">💡 Key Takeaways & Lessons</h3>
                            """, unsafe_allow_html=True)
                            for item in key_takeaways:
                                st.markdown(f"• {item}")
                            st.markdown("</div>", unsafe_allow_html=True)

                        # Decision & Action Items Section (Meeting focus)
                        key_decisions = analysis.get("key_decisions") or []
                        action_items = analysis.get("action_items") or []

                        if key_decisions or action_items or not key_takeaways:
                            c1, c2 = st.columns(2)

                            with c1:
                                st.markdown('<div class="info-card"><h3 style="margin-top:0; color:#2563eb; font-size:1.2rem;">💡 Key Decisions</h3>', unsafe_allow_html=True)
                                if key_decisions:
                                    for d in key_decisions:
                                        st.markdown(f'<div class="decision-pill">✓ {d}</div>', unsafe_allow_html=True)
                                else:
                                    st.info("No explicit key decisions detected.")
                                st.markdown('</div>', unsafe_allow_html=True)

                            with c2:
                                st.markdown('<div class="info-card"><h3 style="margin-top:0; color:#059669; font-size:1.2rem;">🎯 Action Items</h3>', unsafe_allow_html=True)
                                if action_items:
                                    st.dataframe(action_items, use_container_width=True, hide_index=True)
                                else:
                                    st.info("No action items assigned.")
                                st.markdown('</div>', unsafe_allow_html=True)

                        # Full Raw Transcript
                        with st.expander("📄 View Full Raw Transcript"):
                            st.text_area("Transcript Text", data.get("transcript", ""), height=220)

                    else:
                        status.update(label="❌ Error Processing File", state="error", expanded=True)
                        st.error(f"Backend Error: {res.text}")

                except Exception as e:
                    status.update(label="❌ Connection Failed", state="error", expanded=True)
                    st.error(f"Failed to connect to FastAPI backend: {str(e)}")

# --- TAB 2: HISTORY LOG & DELETE MANAGEMENT ---
with tab2:
    top_c1, top_c2, top_c3 = st.columns([3, 1, 1])

    with top_c1:
        st.subheader("📜 Historical Processing Logs")
    with top_c2:
        if st.button("🔄 Refresh History", use_container_width=True):
            st.rerun()
    with top_c3:
        if st.button("🗑️ Clear All Logs", type="secondary", use_container_width=True):
            try:
                del_res = requests.delete("http://localhost:8000/api/v1/history")
                if del_res.status_code == 200:
                    st.toast("History log completely cleared!", icon="✅")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to delete history: {e}")

    try:
        res = requests.get("http://localhost:8000/api/v1/history")
        if res.status_code == 200:
            history_data = res.json().get("history", [])

            if not history_data:
                st.info("No history records found. Process an audio or video file to populate this log!")
            else:
                for idx, item in enumerate(history_data):
                    analysis = item.get("analysis", {})
                    filename = item.get("filename", "Untitled Recording")
                    timestamp = item.get("timestamp", "N/A")
                    category = analysis.get("category", "meeting").upper()

                    with st.expander(f"📁 {filename} [{category}] — 🕒 {timestamp}"):
                        head_col, del_col = st.columns([5, 1])

                        with del_col:
                            if st.button("🗑️ Delete", key=f"del_btn_{idx}"):
                                del_item_res = requests.delete(f"http://localhost:8000/api/v1/history/{idx}")
                                if del_item_res.status_code == 200:
                                    st.toast(f"Deleted {filename}", icon="🗑️")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete item.")

                        st.markdown("**Summary:**")
                        st.write(analysis.get("summary") or analysis.get("executive_summary") or "N/A")

                        takeaways = analysis.get("key_takeaways", [])
                        if takeaways:
                            st.markdown("**Key Takeaways:**")
                            for tip in takeaways:
                                st.markdown(f"• {tip}")

                        decisions = analysis.get("key_decisions", [])
                        action_items = analysis.get("action_items", [])

                        if decisions or action_items:
                            hc1, hc2 = st.columns(2)
                            with hc1:
                                st.markdown("**Key Decisions:**")
                                for d in decisions:
                                    st.markdown(f"- {d}")
                            with hc2:
                                st.markdown("**Action Items:**")
                                if action_items:
                                    st.dataframe(action_items, use_container_width=True, hide_index=True)

                        st.divider()
                        st.text_area("Full Transcript", item.get("transcript", ""), height=150, key=f"hist_txt_{idx}")

    except Exception as e:
        st.error(f"Could not load history: {e}")

st.write("")
st.divider()

# 3. BOTTOM SECTION: HOW TO USE
st.markdown('<div class="section-label">🛠️ How To Use (3-Step Guide)</div>', unsafe_allow_html=True)

step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown("""
    <div class="step-card">
        <span class="step-badge">STEP 01</span>
        <div class="step-title">📁 Upload Media File</div>
        <div class="step-desc">Select any meeting audio or educational video file (<code>.mp3</code>, <code>.mp4</code>, <code>.m4a</code>, <code>.wav</code>). FFmpeg automatically compresses heavy media files locally.</div>
    </div>
    """, unsafe_allow_html=True)

with step_col2:
    st.markdown("""
    <div class="step-card">
        <span class="step-badge">STEP 02</span>
        <div class="step-title">⚡ High-Speed Extraction</div>
        <div class="step-desc">Groq Whisper converts audio to text in seconds, while the LLM extracts summaries, takeaways, decisions, and action items with strict Pydantic schemas.</div>
    </div>
    """, unsafe_allow_html=True)

with step_col3:
    st.markdown("""
    <div class="step-card">
        <span class="step-badge">STEP 03</span>
        <div class="step-title">📋 Review & Track</div>
        <div class="step-desc">View formatted takeaways, decision lists, action items, and raw transcripts. Every file is auto-saved in your persistent history log.</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# 4. BOTTOM SECTION: WHO CAN USE THIS?
st.markdown('<div class="section-label">👥 Who Is This For?</div>', unsafe_allow_html=True)

user_col1, user_col2, user_col3, user_col4 = st.columns(4)

with user_col1:
    st.markdown("""
    <div class="persona-card">
        <div class="persona-icon">👔</div>
        <div>
            <div class="persona-title">Executives & Leads</div>
            <div class="persona-desc">Get high-level 1-minute meeting debriefs without sitting through 1-hour calls.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with user_col2:
    st.markdown("""
    <div class="persona-card">
        <div class="persona-icon">💻</div>
        <div>
            <div class="persona-title">Product & Tech Teams</div>
            <div class="persona-desc">Convert technical syncs and sprint planning into clear action items with assignees.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with user_col3:
    st.markdown("""
    <div class="persona-card">
        <div class="persona-icon">🎯</div>
        <div>
            <div class="persona-title">Sales & Client Success</div>
            <div class="persona-desc">Automatically capture client feedback, feature requests, and follow-up deadlines.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with user_col4:
    st.markdown("""
    <div class="persona-card">
        <div class="persona-icon">🎓</div>
        <div>
            <div class="persona-title">Educators & Learners</div>
            <div class="persona-desc">Summarize educational videos, lectures, and research discussions into clean takeaways.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)