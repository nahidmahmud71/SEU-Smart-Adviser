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

# ================= 2. ADVANCED ANIMATIONS & STYLING =================
st.markdown("""
<style>
    /* Fade In Animation */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .stApp { animation: fadeIn 0.8s ease-in-out; }

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
    
    /* Profile Card with Glassmorphism */
    .profile-card {
        background: rgba(30, 30, 30, 0.8);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s;
    }
    .profile-card:hover { transform: translateY(-5px); }
    
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
    }
    .metric-box:hover {
        transform: scale(1.05);
        border-left-color: #00E5FF;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
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
        box-shadow: 0 0 20px rgba(79, 139, 249, 0.6);
        transform: scale(1.02);
    }
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

# Load Data
try:
    curr_df = pd.read_csv("curriculum.csv")
    curr_df['Prerequisite'] = curr_df['Prerequisite'].fillna('None')
except:
    curr_df = pd.DataFrame(columns=['Course Code', 'Course Title', 'Credits', 'Prerequisite'])

# ================= 4. SIDEBAR (PROFILE) =================
with st.sidebar:
    # 🔴 NOTE: GitHub-এ ছবি আপলোড করার পর এখানে লিংক অটো কাজ করবে যদি ফাইল নেম ঠিক থাকে।
    # অথবা আপনি সরাসরি GitHub থেকে ছবির 'Raw' লিংক কপি করে নিচে বসাতে পারেন।
    
    # Github Raw Link Format: https://raw.githubusercontent.com/USERNAME/REPO/main/FILENAME
    # Example below assumes you uploaded 'IMG_4180.jpg' to your repo
    
    profile_url = "https://raw.githubusercontent.com/nahidmahmud71/SEU-Smart-Adviser/main/IMG_4180.jpg" 
    
    st.markdown(f"""
    <div class="profile-card">
        <img src="{profile_url}" class="profile-img" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'">
        <h2 style="color: white; margin-top: 15px;">Nahid Mahmud</h2>
        <p style="color: #00E5FF; font-weight: bold; margin: 5px 0;">CSE Batch 67</p>
        <p style="color: #bbb; font-size: 13px;">ID: 2024100000194</p>
        <br>
        <span style="background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">Active Student</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Navigation")
    menu = st.radio("Go To:", 
        ["🏠 Dashboard", "📘 Course Adviser", "📅 Routine Maker", "💰 Tuition Calculator", "🚌 Bus & Map", "👨‍🏫 Faculty Info", "🧮 CGPA & Target"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Developed by **Nahid Mahmud**")

# ================= 5. MAIN CONTENT =================

# --- 🏠 DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<div class='main-header'>SEU Student Portal 🚀</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #bbb;'>Academic Dashboard | Spring 2026</p>", unsafe_allow_html=True)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-box'><h4>CGPA</h4><h2 style='color:#00E5FF'>3.80</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-box'><h4>Credits</h4><h2>15/150</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-box'><h4>Batch</h4><h2>67th</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-box'><h4>Waiver</h4><h2 style='color:#FFD700'>20%</h2></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Countdown
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("⏳ Exam Countdown")
        exam_date = date(2026, 2, 25)
        days = (exam_date - date.today()).days
        if days > 0:
            st.info(f"🔥 **Mid-Term Exam** starts in **{days} Days!**")
            st.progress(max(0, 100 - days*2))
        else:
            st.success("Exams are ongoing!")
            
    with col2:
        st.subheader("📢 Notice")
        st.warning("📅 **Feb 15:** Last date of 2nd Installment payment.")

# --- 🚌 BUS & MAP (UPDATED WITH MARKING) ---
elif menu == "🚌 Bus & Map":
    st.header("🚌 Transport Routes & Live Map")
    
    tab1, tab2 = st.tabs(["🗺️ Route Visualization (Map)", "📷 Official Route Maps"])
    
    with tab1:
        st.info("📍 **Blue Dots:** Bus Starting Points (Azimpur, Abdullahpur etc.) | 🔴 **Red Dot:** SEU Campus")
        
        # Coordinates for Marking
        map_data = pd.DataFrame({
            'lat': [23.7692668, 23.7298, 23.8776, 23.8510, 23.7561], 
            'lon': [90.4049922, 90.3854, 90.3995, 90.4085, 90.3872],
            'Location': ['SEU Campus (Tejgaon)', 'Azimpur (Start)', 'Abdullahpur (Start)', 'Airport', 'Farmgate'],
            'Type': ['Campus', 'Bus Stop', 'Bus Stop', 'Bus Stop', 'Bus Stop'],
            'color': ['#FF0000', '#0000FF', '#0000FF', '#0000FF', '#0000FF'], # Red for SEU, Blue for Stops
            'size': [200, 100, 100, 100, 100] # Bigger size for SEU
        })
        
        st.map(map_data, zoom=11, size='size', color='color')
        
    with tab2:
        st.write("### 📸 Official Route Maps")
        c1, c2 = st.columns(2)
        
        # Image Links (Assuming uploaded to GitHub)
        route1_url = "https://raw.githubusercontent.com/nahidmahmud71/SEU-Smart-Adviser/main/IMG_4559.jpeg"
        route2_url = "https://raw.githubusercontent.com/nahidmahmud71/SEU-Smart-Adviser/main/IMG_4560.jpeg"
        
        with c1:
            st.image(route1_url, caption="Route 1: Azimpur to SEU", use_container_width=True)
        with c2:
            st.image(route2_url, caption="Route 2: Abdullahpur/Tongi to SEU", use_container_width=True)

# --- 📘 COURSE ADVISER ---
elif menu == "📘 Course Adviser":
    st.header("📘 Smart Course Adviser")
    if curr_df.empty:
        st.error("⚠️ 'curriculum.csv' missing!")
    else:
        all_courses = curr_df['Course Code'].tolist()
        completed = st.multiselect("Completed Courses:", all_courses, default=['CSE111', 'ENG101', 'MAT101'])
        
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
                st.success(f"🎉 Recommended Courses ({len(eligible)} Available):")
                st.dataframe(pd.DataFrame(eligible)[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
            else:
                st.info("✅ No new courses available.")

# --- 📅 ROUTINE MAKER ---
elif menu == "📅 Routine Maker":
    st.header("📅 Routine Generator")
    sample = pd.DataFrame({'Course String': ['CSE121.1', 'CSE121.2'], 'Faculty': ['Mr. A', 'Ms. B'], 'Day': ['Sun', 'Tue'], 'Time': ['08:30 AM', '10:00 AM']})
    st.download_button("📥 Download Sample", sample.to_csv(index=False).encode('utf-8'), "sample.csv")
    
    uploaded_file = st.file_uploader("Upload Routine CSV", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df[['Course Code', 'Section']] = df['Course String'].apply(lambda x: pd.Series(parse_course_string(x)))
        times = df['Time'].apply(calculate_end_time)
        df['Start_DT'] = [t[0] for t in times]
        df['End_DT'] = [t[1] for t in times]
        df = df.dropna(subset=['Start_DT'])
        
        selected = st.multiselect("Select Courses:", sorted(df['Course Code'].unique()))
        priority = st.text_input("Preferred Faculty:")
        
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
                    st.success(f"✅ Found {len(valid)} Options!")
                    for idx, (rout, sc) in enumerate(valid[:3]):
                        with st.expander(f"Option {idx+1} { '⭐' if sc > 0 else ''}", expanded=(idx==0)):
                            st.table(pd.DataFrame(rout)[['Course String', 'Faculty', 'Day', 'Time']])
                else:
                    st.error("❌ Conflict found!")

# --- 💰 TUITION CALCULATOR ---
elif menu == "💰 Tuition Calculator":
    st.header("💸 Tuition Calculator")
    rates = {"CSE": 4750, "EEE": 3450, "BBA": 4950}
    
    c1, c2 = st.columns(2)
    with c1:
        dept = st.selectbox("Department", list(rates.keys()))
        cr = st.number_input("Credits", 3, 21, 12)
        waiver = st.select_slider("Waiver %", [0, 10, 20, 30, 40, 50, 60, 100], value=20)
    with c2:
        sem_fee = st.number_input("Semester Fee", value=6000)
        lab_fee = st.number_input("Lab Fee", value=2500)

    gross = cr * rates[dept]
    waiver_val = gross * (waiver / 100)
    total = (gross - waiver_val) + sem_fee + lab_fee
    
    st.plotly_chart(go.Figure(data=[go.Pie(labels=['Tuition', 'Sem. Fee', 'Lab Fee'], values=[gross-waiver_val, sem_fee, lab_fee], hole=.4)]), use_container_width=True)
    st.markdown(f"<h2 style='text-align:center; color:#00E5FF;'>Total: {total:,.0f} BDT</h2>", unsafe_allow_html=True)

# --- 👨‍🏫 FACULTY INFO ---
elif menu == "👨‍🏫 Faculty Info":
    st.header("👨‍🏫 Faculty Directory")
    data = [
        {"Name": "Shahriar Manzoor", "Role": "Chairman", "Room": "530", "Email": "cse.chair@seu.edu.bd"},
        {"Name": "Dr. Gazi Zahirul Islam", "Role": "Professor", "Room": "606", "Email": "gazi.islam@seu.edu.bd"},
    ]
    st.table(pd.DataFrame(data))

# --- 🧮 CGPA & TARGET ---
elif menu == "🧮 CGPA & Target":
    st.header("🧮 CGPA Manager")
    mode = st.radio("Mode:", ["📝 Calculate SGPA", "🎯 Target Estimator"], horizontal=True)
    
    if mode == "📝 Calculate SGPA":
        n = st.number_input("No. of Courses", 1, 10, 4)
        credits = []
        points = []
        cols = st.columns(3)
        for i in range(n):
            with cols[i%3]:
                c = st.number_input(f"Cr {i+1}", 1.0, 4.0, 3.0, key=f"c{i}")
                g = st.selectbox(f"GPA {i+1}", [4.0,3.75,3.5,3.0,0.0], key=f"g{i}")
                credits.append(c)
                points.append(c*g)
        if st.button("Calculate"):
            st.success(f"SGPA: {sum(points)/sum(credits):.2f}")
            
    elif mode == "🎯 Target Estimator":
        c1, c2 = st.columns(2)
        with c1: cur_cgpa = st.number_input("Current CGPA", 0.0, 4.0, 3.5)
        with c2: target = st.number_input("Target CGPA", 0.0, 4.0, 3.6)
        comp = st.number_input("Completed Cr", 0, 160, 45)
        next_cr = st.number_input("Next Sem Cr", 3, 21, 15)
        
        req = ((target * (comp + next_cr)) - (cur_cgpa * comp)) / next_cr
        if req > 4.0: st.error(f"Impossible! Need {req:.2f}")
        else: st.success(f"You need **{req:.2f}** GPA next semester.")
