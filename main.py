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
    /* Fade In Animation */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .stApp { animation: fadeIn 0.8s ease-in-out; }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #333;
    }

    /* Modern Gradient Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F8BF9, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0px 4px 10px rgba(0, 229, 255, 0.3);
        margin-bottom: 5px;
    }
    
    /* Profile Card */
    .profile-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .profile-img {
        border-radius: 50%;
        width: 140px;
        height: 140px;
        border: 4px solid #00E5FF;
        padding: 4px;
        object-fit: cover;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
    }
    
    /* Metric Cards */
    .metric-box {
        background: #262730;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4F8BF9;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: 0.3s;
        text-align: center;
    }
    .metric-box:hover {
        transform: translateY(-5px);
        border-left-color: #00E5FF;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #4F8BF9, #00E5FF);
        color: white;
        border: none;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.6);
        transform: scale(1.02);
    }
    
    /* Custom Tables */
    thead tr th:first-child {display:none}
    tbody th {display:none}
</style>
""", unsafe_allow_html=True)

# ================= 3. DATA & FUNCTIONS =================
# --- Image URLs (Raw GitHub Links) ---
# NOTE: Ensure file names match exactly (case sensitive)
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

# Load Curriculum
try:
    curr_df = pd.read_csv("curriculum.csv")
    curr_df['Prerequisite'] = curr_df['Prerequisite'].fillna('None')
except:
    curr_df = pd.DataFrame(columns=['Course Code', 'Course Title', 'Credits', 'Prerequisite'])

# ================= 4. SIDEBAR =================
with st.sidebar:
    st.markdown(f"""
    <div class="profile-card">
        <img src="{PROFILE_PIC}" class="profile-img" onerror="this.onerror=null;this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png';">
        <h2 style="color: white; margin: 10px 0 5px 0;">Nahid Mahmud</h2>
        <p style="color: #00E5FF; font-weight: bold; margin: 0;">CSE Batch 67</p>
        <p style="color: #bbb; font-size: 13px; margin: 5px 0;">ID: 2024100000194</p>
        <br>
        <span style="background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; box-shadow: 0 2px 10px rgba(40,167,69,0.4);">Active Student</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 MENU")
    menu = st.radio("Navigate:", 
        ["🏠 Dashboard", "📘 Course Adviser", "📅 Routine Maker", "💰 Tuition Calculator", "🚌 Bus & Map", "👨‍🏫 Faculty Info", "🧮 CGPA Manager"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 SEU Smart Portal | v7.0 Ultimate")

# ================= 5. MAIN CONTENT =================

# --- 🏠 DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<div class='main-header'>SEU Student Portal 🚀</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #bbb;'>Welcome back to your academic workspace!</p>", unsafe_allow_html=True)

    # 1. Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-box'><h4>CGPA</h4><h2 style='color:#00E5FF'>3.80</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-box'><h4>Credits</h4><h2>15/150</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-box'><h4>Batch</h4><h2>67th</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-box'><h4>Waiver</h4><h2 style='color:#FFD700'>20%</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Main Content Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("⏳ Academic Countdown")
        exam_date = date(2026, 2, 25)
        today = date.today()
        days_left = (exam_date - today).days
        
        if days_left > 0:
            st.info(f"🔥 **Mid-Term Exam** starts in **{days_left} Days!** (Feb 25)")
            st.progress(max(0, 100 - days_left*2))
        else:
            st.success("Exams are ongoing!")
            
        st.markdown("### 📢 Important Notices")
        st.warning("💳 **Feb 15:** 2nd Installment Payment Deadline.")
        st.success("🚌 **Bus Update:** New AC bus added to Uttara Route.")

    with col2:
        st.subheader("🌟 Club Activities")
        st.markdown("""
        * **CPC:** Weekly Coding Contest (Tue)
        * **IEEE:** Seminar on AI (Room 402)
        * **Cultural Club:** Spring Fest Prep
        """)
        st.link_button("🌐 Join CPC Facebook", "https://facebook.com")

# --- 📘 COURSE ADVISER ---
elif menu == "📘 Course Adviser":
    st.header("📘 Smart Course Adviser")
    st.markdown("Auto-detects courses based on SEU CSE Syllabus.")
    
    if curr_df.empty:
        st.error("⚠️ 'curriculum.csv' missing from repository.")
    else:
        all_courses = curr_df['Course Code'].tolist()
        completed = st.multiselect("Select Completed Courses:", all_courses, default=['CSE111', 'ENG101', 'MAT101'])
        
        if st.button("Check Eligibility 🔍"):
            eligible = []
            for _, row in curr_df.iterrows():
                course = row['Course Code']
                prereqs = row['Prerequisite']
                if course in completed: continue
                
                if prereqs == 'None': eligible.append(row)
                else:
                    reqs = prereqs.split(';')
                    if all(r in completed for r in reqs): eligible.append(row)
            
            if eligible:
                st.success(f"🎉 You can take these {len(eligible)} courses:")
                st.dataframe(pd.DataFrame(eligible)[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
            else:
                st.info("✅ You are strictly following the flow!")

# --- 📅 ROUTINE MAKER ---
elif menu == "📅 Routine Maker":
    st.header("📅 Routine Generator")
    
    # Sample Download
    sample = pd.DataFrame({'Course String': ['CSE121.1', 'CSE121.2', 'EEE111.1'], 'Faculty': ['Mr. A', 'Ms. B', 'Dr. C'], 'Day': ['Sun', 'Tue', 'Mon'], 'Time': ['08:30 AM', '10:00 AM', '11:30 AM']})
    st.download_button("📥 Download Sample CSV", sample.to_csv(index=False).encode('utf-8'), "routine_sample.csv")
    
    uploaded_file = st.file_uploader("Upload UMS Schedule (CSV)", type=['csv'])
    
    if uploaded_file:
        try:
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
                if priority: relevant.loc[relevant['Faculty'].str.contains(priority, case=False, na=False), 'Score'] = 10
                relevant = relevant.sort_values(by='Score', ascending=False)
                
                import itertools
                groups = [relevant[relevant['Course Code'] == c].to_dict('records') for c in selected if not relevant[relevant['Course Code'] == c].empty]
                
                if groups:
                    combos = list(itertools.product(*groups))
                    valid = []
                    for combo in combos:
                        check = [{'Day': i['Day'], 'Start': i['Start_DT'], 'End': i['End_DT']} for i in combo]
                        if not check_conflict(check): valid.append((combo, sum(i['Score'] for i in combo)))
                    
                    valid.sort(key=lambda x: x[1], reverse=True)
                    if valid:
                        st.success(f"✅ Found {len(valid)} Valid Options!")
                        for idx, (rout, sc) in enumerate(valid[:3]):
                            with st.expander(f"Option {idx+1} { '⭐' if sc > 0 else ''}", expanded=(idx==0)):
                                st.table(pd.DataFrame(rout)[['Course String', 'Faculty', 'Day', 'Time']])
                    else:
                        st.error("❌ Conflict Detected! Change Sections.")
        except:
            st.error("Invalid File Format. Please check the sample.")

# --- 💰 TUITION CALCULATOR ---
elif menu == "💰 Tuition Calculator":
    st.header("💸 Tuition Fee Calculator")
    st.caption("Spring 2026 Rates | Batch 67")
    
    rates = {"CSE": 4750, "EEE": 3450, "BBA": 4950, "English": 3700, "Pharmacy": 5350}
    
    c1, c2 = st.columns(2)
    with c1:
        dept = st.selectbox("Department", list(rates.keys()))
        per_cr = st.number_input("Cost Per Credit", value=rates[dept], step=50)
        cr = st.number_input("Total Credits", 3, 21, 12)
        waiver = st.select_slider("Waiver Percentage", [0, 10, 20, 25, 30, 40, 50, 60, 100], value=20)
    with c2:
        sem_fee = st.number_input("Semester Fee", value=6000)
        lab_fee = st.number_input("Lab Fee", value=2500)
        other_fee = st.number_input("Other Fees", value=0)

    gross = cr * per_cr
    waiver_val = gross * (waiver / 100)
    net = gross - waiver_val
    total = net + sem_fee + lab_fee + other_fee
    
    st.divider()
    
    k1, k2 = st.columns(2)
    with k1:
        st.subheader("📊 Breakdown")
        fig = go.Figure(data=[go.Pie(labels=['Net Tuition', 'Semester Fee', 'Lab Fee'], values=[net, sem_fee, lab_fee], hole=.5)])
        fig.update_layout(height=300, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    with k2:
        st.markdown(f"""
        <div style="background-color:#1a1a1a; padding:20px; border-radius:15px; text-align:center; border:1px solid #333;">
            <p style="color:#aaa;">Total Payable Amount</p>
            <h1 style="color:#00E5FF; margin:0;">{total:,.0f} BDT</h1>
            <p style="color:#28a745; font-size:14px; margin-top:5px;">You Saved: {waiver_val:,.0f} BDT</p>
        </div>
        """, unsafe_allow_html=True)

# --- 🚌 BUS & MAP (FIXED) ---
elif menu == "🚌 Bus & Map":
    st.header("🚌 Transport Routes & Live Map")
    
    tab1, tab2, tab3 = st.tabs(["🗺️ Live Map", "📷 Route Images", "🕒 Bus Schedule"])
    
    with tab1:
        st.info("📍 **Red:** SEU Campus | **Blue:** Bus Starting Points")
        
        # Fixed Coordinates
        map_data = pd.DataFrame({
            'lat': [23.7692668, 23.7298, 23.8776, 23.8510], 
            'lon': [90.4049922, 90.3854, 90.3995, 90.4085],
            'size': [1000, 200, 200, 200], # SEU bigger
            'color': ['#FF0000', '#0000FF', '#0000FF', '#0000FF'] # Red vs Blue
        })
        
        st.map(map_data, zoom=11, size='size', color='color')
        
    with tab2:
        st.write("### 📸 Official Route Maps")
        c1, c2 = st.columns(2)
        with c1:
            st.image(ROUTE_MAP_1, caption="Route 1: Azimpur - SEU", use_container_width=True)
        with c2:
            st.image(ROUTE_MAP_2, caption="Route 2: Tongi/Abdullahpur - SEU", use_container_width=True)
            
    with tab3:
        st.write("### 🕒 Departure Times")
        st.table(pd.DataFrame([
            {"Shift": "Morning", "From Campus": "1:40 PM"},
            {"Shift": "Evening", "From Campus": "5:20 PM"},
        ]))
        st.write("**Routes:** Azimpur, Mirpur, Uttara, Savar, Jatrabari.")

# --- 👨‍🏫 FACULTY INFO ---
elif menu == "👨‍🏫 Faculty Info":
    st.header("👨‍🏫 CSE Faculty Directory")
    
    fac_data = [
        {"Name": "Shahriar Manzoor", "Role": "Chairman", "Room": "530", "Email": "cse.chair@seu.edu.bd"},
        {"Name": "Dr. Gazi Zahirul Islam", "Role": "Professor", "Room": "606", "Email": "gazi.islam@seu.edu.bd"},
        {"Name": "Dr. Ashikur Rahman", "Role": "Coordinator", "Room": "529", "Email": "ashikur@seu.edu.bd"},
        {"Name": "Md. Shohel Babu", "Role": "Lecturer", "Room": "301", "Email": "shohel.babu@seu.edu.bd"},
        {"Name": "Lameya Islam", "Role": "Lecturer", "Room": "302", "Email": "lameya@seu.edu.bd"},
        {"Name": "Monirul Islam", "Role": "Lecturer", "Room": "303", "Email": "monirul@seu.edu.bd"},
    ]
    st.table(pd.DataFrame(fac_data))

# --- 🧮 CGPA MANAGER ---
elif menu == "🧮 CGPA Manager":
    st.header("🧮 CGPA Manager")
    
    mode = st.radio("Select Mode:", ["📝 Calculate SGPA", "🎯 Target Estimator"], horizontal=True)
    
    if mode == "📝 Calculate SGPA":
        n = st.number_input("Number of Courses", 1, 10, 4)
        cols = st.columns(3)
        credits = []
        points = []
        
        for i in range(n):
            with cols[i%3]:
                c = st.number_input(f"Cr {i+1}", 1.0, 4.0, 3.0, key=f"c{i}")
                g = st.selectbox(f"GPA {i+1}", [4.0,3.75,3.5,3.25,3.0,2.5,2.0,0.0], key=f"g{i}")
                credits.append(c)
                points.append(c*g)
        
        if st.button("Calculate Result"):
            sgpa = sum(points)/sum(credits)
            st.balloons()
            st.success(f"🎯 SGPA: **{sgpa:.2f}**")
            
    elif mode == "🎯 Target Estimator":
        c1, c2 = st.columns(2)
        with c1: cur_cgpa = st.number_input("Current CGPA", 0.0, 4.0, 3.50)
        with c2: target = st.number_input("Target CGPA", 0.0, 4.0, 3.65)
        
        comp = st.number_input("Completed Credits", 0, 160, 45)
        next_cr = st.number_input("Next Sem Credits", 3, 21, 15)
        
        req = ((target * (comp + next_cr)) - (cur_cgpa * comp)) / next_cr
        
        if req > 4.0: st.error(f"❌ Impossible! You need {req:.2f} GPA.")
        elif req < 0: st.success("🎉 Target already achieved!")
        else: st.success(f"✅ You need to score **{req:.2f}** GPA next semester.")
