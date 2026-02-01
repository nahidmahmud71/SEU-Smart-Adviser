import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="SEU Student Portal Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. PROFESSIONAL STYLING (CSS) =================
st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: 700; color: #4F8BF9; text-align: center; margin-bottom: 10px;}
    .profile-card {background-color: #1E1E1E; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; margin-bottom: 20px;}
    .profile-img {border-radius: 50%; width: 120px; height: 120px; border: 4px solid #4F8BF9; object-fit: cover; margin-bottom: 10px;}
    .metric-box {background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #4F8BF9; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);}
    .stButton>button {width: 100%; border-radius: 8px; font-weight: 600; transition: 0.3s;}
    .stButton>button:hover {transform: scale(1.02);}
</style>
""", unsafe_allow_html=True)

# ================= 3. HELPER FUNCTIONS =================
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

# Load Data Safely
try:
    curr_df = pd.read_csv("curriculum.csv")
    curr_df['Prerequisite'] = curr_df['Prerequisite'].fillna('None')
except:
    curr_df = pd.DataFrame(columns=['Course Code', 'Course Title', 'Credits', 'Prerequisite'])

# ================= 4. SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div class="profile-card">
        <img src="https://avatars.githubusercontent.com/u/10000000?v=4" class="profile-img">
        <h3 style="margin:0; color: white;">Nahid Mahmud</h3>
        <p style="color: #aaa; font-size: 14px; margin: 5px 0;">CSE Student | Batch 64</p>
        <p style="color: #4F8BF9; font-weight: bold; font-size: 14px;">ID: 2024100000194</p>
        <a href="https://github.com/nahidmahmud71" target="_blank" style="text-decoration: none;">
            <div style="background-color: #333; color: white; padding: 5px; border-radius: 5px; margin-top: 10px; font-size: 12px;">
                View GitHub Profile 🔗
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Go to:", 
        ["🏠 Dashboard", "📘 Course Adviser", "📅 Routine Maker", "💰 Tuition Calculator", "🗺️ Campus Map", "👨‍🏫 Faculty Info", "🧮 CGPA Calculator"]
    )
    st.divider()
    st.caption("© 2026 SEU Smart Portal | v5.0 Ultimate")

# ================= 5. MAIN CONTENT =================

if menu == "🏠 Dashboard":
    st.markdown("<div class='main-header'>Welcome Back, Nahid! 👋</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-box'><h4>Current CGPA</h4><h2>3.80</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-box'><h4>Completed Cr.</h4><h2>45/150</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-box'><h4>Next Payment</h4><h2>Feb 15</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-box'><h4>Waiver</h4><h2>20%</h2></div>", unsafe_allow_html=True)

elif menu == "📘 Course Adviser":
    st.header("📘 Smart Course Adviser")
    if curr_df.empty:
        st.error("⚠️ 'curriculum.csv' file not found!")
    else:
        all_courses = curr_df['Course Code'].tolist()
        completed = st.multiselect("Select courses you have ALREADY passed:", all_courses, default=['CSE141', 'MAT141', 'ENG101'])
        if st.button("Check Eligibility 🔍"):
            eligible = []
            for _, row in curr_df.iterrows():
                course = row['Course Code']
                prereqs = row['Prerequisite']
                if course in completed: continue
                if prereqs == 'None':
                    eligible.append(row)
                else:
                    reqs = prereqs.split(';')
                    if all(r in completed for r in reqs):
                        eligible.append(row)
            if eligible:
                st.success(f"🎉 You can take these {len(eligible)} courses:")
                st.dataframe(pd.DataFrame(eligible)[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
            else:
                st.info("✅ You are up to date!")

elif menu == "📅 Routine Maker":
    st.header("📅 Automatic Routine Generator")
    sample_data = pd.DataFrame({'Course String': ['CSE265.1', 'CSE265.2', 'MAT261.1'], 'Faculty': ['Mr. X', 'Ms. Y', 'Dr. Z'], 'Day': ['Sun', 'Tue', 'Mon'], 'Time': ['08:30 AM', '10:00 AM', '02:00 PM']})
    st.download_button("📥 Download Sample CSV", sample_data.to_csv(index=False).encode('utf-8'), "sample_routine.csv")
    uploaded_file = st.file_uploader("Upload Routine File", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df[['Course Code', 'Section']] = df['Course String'].apply(lambda x: pd.Series(parse_course_string(x)))
        times = df['Time'].apply(calculate_end_time)
        df['Start_DT'] = [t[0] for t in times]
        df['End_DT'] = [t[1] for t in times]
        df = df.dropna(subset=['Start_DT'])
        c1, c2 = st.columns(2)
        with c1: selected = st.multiselect("Select Courses:", sorted(df['Course Code'].unique()))
        with c2: priority = st.text_input("Preferred Faculty (Optional):")
        if st.button("Generate Routine ⚡"):
            relevant = df[df['Course Code'].isin(selected)].copy()
            relevant['Score'] = 0
            if priority:
                relevant.loc[relevant['Faculty'].str.contains(priority, case=False, na=False), 'Score'] = 10
            relevant = relevant.sort_values(by='Score', ascending=False)
            import itertools
            groups = [relevant[relevant['Course Code'] == c].to_dict('records') for c in selected if not relevant[relevant['Course Code'] == c].empty]
            if groups:
                combos = list(itertools.product(*groups))
                valid = []
                for combo in combos:
                    check = [{'Day': i['Day'], 'Start': i['Start_DT'], 'End': i['End_DT']} for i in combo]
                    if not check_conflict(check):
                        valid.append((combo, sum(i['Score'] for i in combo)))
                valid.sort(key=lambda x: x[1], reverse=True)
                if valid:
                    st.success(f"✅ Found {len(valid)} Options!")
                    for idx, (rout, sc) in enumerate(valid[:5]):
                        with st.expander(f"Option {idx+1} { '⭐' if sc > 0 else ''}", expanded=(idx==0)):
                            st.table(pd.DataFrame(rout)[['Course String', 'Faculty', 'Day', 'Time']])
                else:
                    st.error("❌ Conflict found!")

elif menu == "💰 Tuition Calculator":
    st.header("💸 Tuition Fee Calculator (Spring 2026)")
    dept_rates = {"CSE": 4750, "EEE": 3450, "Textile": 3300, "BBA": 4950, "English": 3700, "Pharmacy": 5350, "Architecture": 4250}
    c1, c2 = st.columns(2)
    with c1:
        dept = st.selectbox("Department", list(dept_rates.keys()))
        per_credit = st.number_input("Cost Per Credit", value=dept_rates[dept], step=50)
        credits = st.number_input("Credits Taking", 3, 20, 12)
        waiver = st.select_slider("Waiver %", [0, 10, 20, 30, 40, 50, 60, 70, 80, 100], value=20)
    with c2:
        semester_fee = st.number_input("Semester Fee", value=6000)
        lab_fee = st.number_input("Lab Fee", value=2500)
        other_fee = st.number_input("Others", value=0)
    gross = credits * per_credit
    waiver_amt = gross * (waiver / 100)
    net = gross - waiver_amt
    total = net + semester_fee + lab_fee + other_fee
    
    st.divider()
    k1, k2 = st.columns([1,1])
    with k1:
        st.subheader("📊 Breakdown")
        fig = go.Figure(data=[go.Pie(labels=['Tuition', 'Sem. Fee', 'Lab Fee'], values=[net, semester_fee, lab_fee], hole=.5)])
        fig.update_layout(height=300, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    with k2:
        st.success(f"💰 Total Payable: **{total:,.0f} BDT**")
        st.caption(f"You saved {waiver_amt:,.0f} BDT!")

elif menu == "🗺️ Campus Map":
    st.header("📍 SEU Permanent Campus")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.map(pd.DataFrame({'lat': [23.7692668], 'lon': [90.4049922]}), zoom=16)
    with c2:
        st.info("251/A & 252, Tejgaon I/A, Dhaka")
        st.link_button("🚗 Google Map", "https://maps.app.goo.gl/YourSEUMapLink")

elif menu == "👨‍🏫 Faculty Info":
    st.header("👨‍🏫 Faculty Directory")
    data = [
        {"Name": "Shahriar Manzoor", "Designation": "Chairman", "Room": "530", "Email": "cse.chair@seu.edu.bd"},
        {"Name": "Dr. Gazi Zahirul Islam", "Designation": "Assoc. Prof", "Room": "606", "Email": "gazi.islam@seu.edu.bd"},
        {"Name": "Dr. Ashikur Rahman", "Designation": "Coordinator", "Room": "529", "Email": "ashikur@seu.edu.bd"},
    ]
    st.table(pd.DataFrame(data))

# ================= 🧮 UPDATED CGPA CALCULATOR =================
elif menu == "🧮 CGPA Calculator":
    st.header("🧮 Advanced CGPA Calculator")
    st.markdown("Calculate your SGPA (Semester) and Total CGPA (Cumulative) accurately.")

    tab1, tab2 = st.tabs(["📝 Calculate SGPA", "ℹ️ Grading Sheet"])

    with tab1:
        # --- Previous Data Input ---
        with st.expander("➕ Add Previous Semesters (Optional for Total CGPA)", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                prev_cgpa = st.number_input("Previous CGPA", 0.00, 4.00, 0.00, step=0.01)
            with col2:
                prev_credits = st.number_input("Completed Credits", 0, 160, 0)

        # --- Current Semester Input ---
        st.subheader("Current Semester Courses")
        
        c1, c2 = st.columns(2)
        with c1:
            num_theory = st.number_input("Number of Theory Courses (3.0 Cr)", 0, 8, 3)
        with c2:
            num_lab = st.number_input("Number of Lab/Project Courses", 0, 5, 1)

        current_credits = []
        current_points = []

        # Theory Inputs
        if num_theory > 0:
            st.markdown("##### 📘 Theory Courses")
            cols = st.columns(3)
            for i in range(num_theory):
                with cols[i % 3]:
                    st.caption(f"Theory {i+1}")
                    cr = st.number_input(f"Cr.", value=3.0, key=f"th_cr_{i}", disabled=True)
                    gpa = st.selectbox(f"Grade", [4.00, 3.75, 3.50, 3.25, 3.00, 2.75, 2.50, 2.25, 2.00, 0.00], key=f"th_gp_{i}")
                    current_credits.append(cr)
                    current_points.append(cr * gpa)

        # Lab Inputs
        if num_lab > 0:
            st.markdown("##### 🧪 Lab / Project Courses")
            cols = st.columns(3)
            for i in range(num_lab):
                with cols[i % 3]:
                    st.caption(f"Lab {i+1}")
                    # Labs can be 1.0 or 1.5, allowing edit
                    cr = st.selectbox(f"Cr.", [1.0, 1.5, 2.0, 3.0], key=f"lab_cr_{i}") 
                    gpa = st.selectbox(f"Grade", [4.00, 3.75, 3.50, 3.25, 3.00, 2.75, 2.50, 2.25, 2.00, 0.00], key=f"lab_gp_{i}")
                    current_credits.append(cr)
                    current_points.append(cr * gpa)

        st.divider()

        if st.button("Calculate Result 🚀", type="primary"):
            # SGPA Calculation
            sem_total_credits = sum(current_credits)
            sem_total_points = sum(current_points)
            
            if sem_total_credits > 0:
                sgpa = sem_total_points / sem_total_credits
                
                # Total CGPA Calculation
                total_credits_all = prev_credits + sem_total_credits
                total_points_all = (prev_cgpa * prev_credits) + sem_total_points
                total_cgpa = total_points_all / total_credits_all if total_credits_all > 0 else 0.0

                # Display Results
                r1, r2, r3 = st.columns(3)
                with r1:
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center;">
                        <h4 style="margin:0; color: #aaa;">Semester SGPA</h4>
                        <h1 style="margin:0; color: #4CAF50;">{sgpa:.2f}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with r2:
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center;">
                        <h4 style="margin:0; color: #aaa;">Total Credits</h4>
                        <h1 style="margin:0; color: #4F8BF9;">{sem_total_credits}</h1>
                    </div>
                    """, unsafe_allow_html=True)

                if prev_credits > 0:
                    with r3:
                        st.markdown(f"""
                        <div style="background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #FFD700; text-align: center;">
                            <h4 style="margin:0; color: #FFD700;">New Total CGPA</h4>
                            <h1 style="margin:0; color: white;">{total_cgpa:.2f}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with r3:
                         st.info("Enter previous credits to see Total CGPA.")
                
                st.balloons()
            else:
                st.warning("Please select at least one course.")

    with tab2:
        st.subheader("📌 SEU Grading Sheet")
        grading_data = {
            "Marks (%)": ["80-100", "75-79", "70-74", "65-69", "60-64", "55-59", "50-54", "45-49", "40-44", "Below 40"],
            "Grade": ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"],
            "Point": ["4.00", "3.75", "3.50", "3.25", "3.00", "2.75", "2.50", "2.25", "2.00", "0.00"]
        }
        st.table(pd.DataFrame(grading_data))
