import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date, timedelta

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="SEU Portal | Batch 67",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. ADVANCED CSS & ANIMATIONS =================
st.markdown("""
<style>
    /* Global Animation */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .stApp { animation: fadeIn 0.6s ease-in-out; }

    /* Header Styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0px 4px 15px rgba(0, 114, 255, 0.3);
    }

    /* Sidebar Profile Card */
    .profile-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .profile-card:hover { transform: translateY(-5px); }
    
    .profile-img {
        border-radius: 50%;
        width: 130px;
        height: 130px;
        border: 4px solid #00C6FF;
        padding: 4px;
        object-fit: cover;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
    }

    /* Metric Box */
    .metric-box {
        background: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00C6FF;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: 0.3s;
    }
    .metric-box:hover {
        transform: scale(1.05);
        border-left-color: #0072FF;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.4);
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 12px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.5);
    }

    /* Result Card for CGPA */
    .result-card {
        background: linear-gradient(135deg, #1E1E1E, #252525);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #333;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.2);
    }
    
    /* Input Areas */
    .input-section {
        background-color: #262730;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. DATA & FUNCTIONS =================
# Raw Links for Images
PROFILE_PIC = "https://raw.githubusercontent.com/nahidmahmud71/SEU-Smart-Adviser/main/IMG_4180.jpg"
ROUTE_MAP_1 = "https://raw.githubusercontent.com/nahidmahmud71/SEU-Smart-Adviser/main/IMG_4559.jpeg"
ROUTE_MAP_2 = "https://raw.githubusercontent.com/nahidmahmud71/SEU-Smart-Adviser/main/IMG_4560.jpeg"

def calculate_end_time(start_time_str):
    try:
        start_time_str = start_time_str.strip().upper()
        fmt = "%I:%M %p" if "M" in start_time_str else "%H:%M"
        start_dt = datetime.strptime(start_time_str, fmt)
        end_dt = start_dt + timedelta(minutes=80) 
        return start_dt, end_dt
    except:
        return None, None

def parse_course_string(course_str):
    if '.' in course_str:
        parts = course_str.split('.')
        return parts[0].strip(), parts[1].strip()
    return course_str, "N/A"

def check_conflict(routine_list):
    for i in range(len(routine_list)):
        for j in range(i + 1, len(routine_list)):
            c1, c2 = routine_list[i], routine_list[j]
            if c1['Day'] == c2['Day']:
                if max(c1['Start'], c2['Start']) < min(c1['End'], c2['End']):
                    return True
    return False

# --- ROBUST CURRICULUM LOADER (FIX FOR COURSE ADVISER) ---
# This ensures the app works even if curriculum.csv is missing
try:
    curr_df = pd.read_csv("curriculum.csv")
    curr_df['Prerequisite'] = curr_df['Prerequisite'].fillna('None')
except:
    # FALLBACK DATA: Essential CSE Courses
    data = {
        'Course Code': ['CSE111', 'CSE121', 'CSE122', 'EEE111', 'MAT101', 'MAT102', 'ENG101', 'CSE211', 'CSE221', 'CSE281', 'MAT201'],
        'Course Title': ['Computer Fund.', 'Programming I', 'Programming II', 'Electrical Ckt', 'Diff Calc', 'Int Calc', 'English I', 'Data Structure', 'Algorithms', 'Digital Logic', 'Coord Geom'],
        'Credits': [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0],
        'Prerequisite': ['None', 'None', 'CSE121', 'MAT101', 'None', 'MAT101', 'None', 'CSE122', 'CSE211', 'CSE122', 'MAT102']
    }
    curr_df = pd.DataFrame(data)

# ================= 4. SIDEBAR =================
with st.sidebar:
    st.markdown(f"""
    <div class="profile-card">
        <img src="{PROFILE_PIC}" class="profile-img" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png';">
        <h2 style="color: white; margin: 10px 0 0 0;">Nahid Mahmud</h2>
        <p style="color: #00C6FF; font-weight: bold; margin: 0;">CSE Batch 67</p>
        <p style="color: #aaa; font-size: 13px;">ID: 2024100000194</p>
        <br>
        <div style="background: linear-gradient(90deg, #28a745, #20c997); padding: 5px; border-radius: 15px; display: inline-block;">
            <span style="color: white; font-weight: bold; font-size: 12px;">Active Student</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 MENU")
    menu = st.radio("Navigate:", 
        ["🏠 Dashboard", "🧮 CGPA Calculator", "📘 Course Adviser", "📅 Routine Maker", "💰 Tuition Calculator", "🚌 Bus & Map", "👨‍🏫 Faculty Info"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("© 2026 SEU Smart Portal | v8.0 Final")

# ================= 5. MAIN CONTENT =================

# --- 🏠 DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<div class='main-header'>Student Portal 🚀</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Academic Overview | Spring 2026</p>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-box'><h4>CGPA</h4><h2 style='color:#00C6FF'>3.80</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-box'><h4>Credits</h4><h2>15/150</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-box'><h4>Batch</h4><h2>67th</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-box'><h4>Waiver</h4><h2 style='color:#FFD700'>20%</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("⏳ Academic Countdown")
        days_left = (date(2026, 2, 25) - date.today()).days
        if days_left > 0:
            st.info(f"🔥 **Mid-Term Exam** in **{days_left} Days!**")
            st.progress(max(0, 100 - days_left*2))
        else:
            st.success("Exams are Ongoing!")
            
    with col2:
        st.subheader("📢 Notices")
        st.warning("💳 **Feb 15:** 2nd Installment Deadline")

# --- 🧮 CGPA CALCULATOR (TOTALLY REVAMPED) ---
elif menu == "🧮 CGPA Calculator":
    st.markdown("<div class='main-header'>🧮 Advanced CGPA Calculator</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#bbb;'>Calculate your semester GPA accurately with easy inputs.</p>", unsafe_allow_html=True)
    
    # Grading Scale Reference
    with st.expander("ℹ️ View SEU Grading Scale"):
        st.table(pd.DataFrame({
            "Marks": ["80+", "75-79", "70-74", "65-69", "60-64", "55-59", "50-54", "40-49", "<40"],
            "Grade": ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"],
            "Point": [4.00, 3.75, 3.50, 3.25, 3.00, 2.75, 2.50, 2.00, 0.00]
        }))

    st.write("---")
    
    # Input Section
    col_theory, col_lab = st.columns(2)
    
    credits = []
    points = []
    
    with col_theory:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.subheader("📘 Theory Courses")
        st.caption("Standard 3.0 Credit Courses")
        num_theory = st.number_input("How many Theory courses?", 1, 6, 4)
        
        for i in range(num_theory):
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f"**Subject {i+1}**")
            with c2: 
                g = st.selectbox(f"Select Grade", [4.0, 3.75, 3.5, 3.25, 3.0, 2.5, 2.0, 0.0], key=f"tg{i}")
                credits.append(3.0)
                points.append(3.0 * g)
            st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_lab:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.subheader("🧪 Lab / Sessional")
        st.caption("Labs or Projects (1.0 - 2.0 Credits)")
        num_lab = st.number_input("How many Lab courses?", 0, 4, 1)
        
        for i in range(num_lab):
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1: st.markdown(f"**Lab {i+1}**")
            with c2: cr = st.selectbox("Cr", [1.0, 1.5, 2.0], key=f"lcr{i}")
            with c3: 
                g = st.selectbox(f"Grade", [4.0, 3.75, 3.5, 3.25, 3.0, 2.5, 2.0, 0.0], key=f"lg{i}")
                credits.append(cr)
                points.append(cr * g)
            st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

    # Calculation Button
    if st.button("🚀 Calculate Result", type="primary"):
        total_cr = sum(credits)
        total_pts = sum(points)
        sgpa = total_pts / total_cr if total_cr > 0 else 0.0
        
        # Fancy Result Display
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color: #aaa; margin:0;">Your Semester GPA</h3>
            <h1 style="color: #00C6FF; font-size: 4rem; margin: 10px 0; font-weight:800;">{sgpa:.2f}</h1>
            <p style="font-size: 1.2rem;">Total Credits: <b style="color:#fff">{total_cr}</b> | Total Points: <b style="color:#fff">{total_pts:.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        if sgpa >= 3.80: st.balloons()
        elif sgpa >= 3.00: st.success("Good job! Keep it up.")
        else: st.warning("Push harder next semester!")

# --- 📘 COURSE ADVISER (FIXED) ---
elif menu == "📘 Course Adviser":
    st.header("📘 Smart Course Adviser")
    st.info("Select completed courses to see what opens up next.")
    
    all_courses = curr_df['Course Code'].tolist()
    completed = st.multiselect("Completed Courses:", all_courses, default=['CSE111', 'ENG101', 'MAT101'])
    
    if st.button("Check Eligibility 🔍"):
        eligible = []
        for _, row in curr_df.iterrows():
            course = row['Course Code']
            prereqs = str(row['Prerequisite'])
            
            if course in completed: continue
            
            # Logic Fix
            if prereqs == 'None' or prereqs == 'nan':
                eligible.append(row)
            else:
                reqs = [r.strip() for r in prereqs.split(';')]
                if all(r in completed for r in reqs):
                    eligible.append(row)
        
        if eligible:
            st.success(f"🎉 You can take these {len(eligible)} courses:")
            st.dataframe(pd.DataFrame(eligible)[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
        else:
            st.warning("⚠️ No new courses found based on your selection.")

# --- 📅 ROUTINE MAKER ---
elif menu == "📅 Routine Maker":
    st.header("📅 Routine Generator")
    sample = pd.DataFrame({'Course String': ['CSE121.1', 'CSE121.2'], 'Faculty': ['Mr. A', 'Ms. B'], 'Day': ['Sun', 'Tue'], 'Time': ['08:30 AM', '10:00 AM']})
    st.download_button("📥 Download Sample", sample.to_csv(index=False).encode('utf-8'), "sample.csv")
    
    uploaded_file = st.file_uploader("Upload UMS CSV", type=['csv'])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df[['Course Code', 'Section']] = df['Course String'].apply(lambda x: pd.Series(parse_course_string(x)))
            times = df['Time'].apply(calculate_end_time)
            df['Start_DT'] = [t[0] for t in times]
            df['End_DT'] = [t[1] for t in times]
            df = df.dropna(subset=['Start_DT'])
            
            selected = st.multiselect("Select Courses:", sorted(df['Course Code'].unique()))
            if st.button("Generate"):
                relevant = df[df['Course Code'].isin(selected)]
                if not relevant.empty:
                    st.success("Routine Generated!")
                    st.dataframe(relevant[['Course String', 'Day', 'Time', 'Faculty']])
                else:
                    st.warning("No courses selected or found in file.")
        except:
            st.error("Invalid File Format")

# --- 💰 TUITION CALCULATOR ---
elif menu == "💰 Tuition Calculator":
    st.header("💸 Tuition Calculator")
    rates = {"CSE": 4750, "EEE": 3450, "BBA": 4950, "English": 3700}
    
    c1, c2 = st.columns(2)
    with c1:
        dept = st.selectbox("Department", list(rates.keys()))
        cr = st.number_input("Total Credits", 3, 21, 12)
        waiver = st.select_slider("Waiver %", [0, 20, 40, 50, 60, 100], value=20)
    with c2:
        sem_fee = st.number_input("Semester Fee", value=6000)
        lab_fee = st.number_input("Lab Fee", value=2500)

    net_tuition = (cr * rates[dept]) * ((100-waiver)/100)
    total = net_tuition + sem_fee + lab_fee
    
    st.markdown(f"<div class='result-card'><h1>Total: {total:,.0f} BDT</h1><p>You Saved: {(cr*rates[dept])*(waiver/100):,.0f} BDT</p></div>", unsafe_allow_html=True)

# --- 🚌 BUS & MAP ---
elif menu == "🚌 Bus & Map":
    st.header("🚌 Transport & Map")
    t1, t2 = st.tabs(["🗺️ Live Map", "📷 Route Images"])
    
    with t1:
        st.info("🔴 SEU Campus | 🔵 Bus Stops")
        map_data = pd.DataFrame({
            'lat': [23.7692668, 23.7298, 23.8776], 
            'lon': [90.4049922, 90.3854, 90.3995],
            'color': ['#FF0000', '#0000FF', '#0000FF'],
            'size': [1000, 200, 200]
        })
        st.map(map_data, zoom=11, size='size', color='color')
        
    with t2:
        c1, c2 = st.columns(2)
        with c1: st.image(ROUTE_MAP_1, caption="Route 1", use_container_width=True)
        with c2: st.image(ROUTE_MAP_2, caption="Route 2", use_container_width=True)

# --- 👨‍🏫 FACULTY ---
elif menu == "👨‍🏫 Faculty Info":
    st.header("👨‍🏫 Faculty Directory")
    st.table(pd.DataFrame([
        {"Name": "Shahriar Manzoor", "Role": "Chairman", "Email": "cse.chair@seu.edu.bd"},
        {"Name": "Dr. Gazi Zahirul", "Role": "Professor", "Email": "gazi.islam@seu.edu.bd"}
    ]))
