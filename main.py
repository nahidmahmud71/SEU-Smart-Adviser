import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ================= 1. PAGE CONFIGURATION =================
st.set_page_config(
    page_title="SEU Smart Portal | Nahid",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. PROFESSIONAL STYLING (CSS) =================
st.markdown("""
<style>
    /* Global Styles */
    .main-header {
        font-size: 2.2rem; 
        font-weight: 700; 
        color: #4F8BF9; 
        text-align: center; 
        margin-bottom: 10px;
    }
    .profile-card {
        background-color: #1E1E1E; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #333; 
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .profile-img {
        border-radius: 50%; 
        width: 120px; 
        height: 120px;
        border: 4px solid #4F8BF9; 
        object-fit: cover;
        margin-bottom: 10px;
    }
    .metric-box {
        background-color: #262730; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #4F8BF9;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button {
        width: 100%; 
        border-radius: 8px; 
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
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
        end_dt = start_dt + timedelta(minutes=80) # 1 hr 20 min class
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

# ================= 4. SIDEBAR (PROFILE & NAVIGATION) =================
with st.sidebar:
    # --- Profile Section ---
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
    
    st.write("### 🧭 Navigation")
    menu = st.radio(
        "Go to:", 
        ["🏠 Dashboard", "📘 Course Adviser", "📅 Routine Maker", "💰 Tuition Calculator", "🗺️ Campus Map", "👨‍🏫 Faculty Info", "🧮 CGPA Calculator"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 SEU Smart Portal | v3.0 Pro")

# ================= 5. MAIN CONTENT =================

# --- 🏠 DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<div class='main-header'>Welcome Back, Nahid! 👋</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa;'>Southeast University Student Portal</p>", unsafe_allow_html=True)
    
    # Quick Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-box'><h4>Current CGPA</h4><h2>3.80</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-box'><h4>Completed Cr.</h4><h2>45/150</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-box'><h4>Next Payment</h4><h2>Feb 15</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-box'><h4>Waiver</h4><h2>40%</h2></div>", unsafe_allow_html=True)

    st.markdown("### 🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Planning for Next Semester?**\nCheck the 'Course Adviser' to see which courses unlock next.")
    with col2:
        st.success("💰 **Payment Calculation**\nUse the 'Tuition Calculator' to see your net payable amount after waiver.")

# --- 📘 COURSE ADVISER ---
elif menu == "📘 Course Adviser":
    st.header("📘 Smart Course Adviser")
    st.write("Based on **SEU CSE Curriculum**, check your eligibility.")
    
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
                
                # Prerequisite Logic
                if prereqs == 'None':
                    eligible.append(row)
                else:
                    reqs = prereqs.split(';')
                    if all(r in completed for r in reqs):
                        eligible.append(row)
            
            if eligible:
                st.balloons()
                st.success(f"🎉 You can take these {len(eligible)} courses:")
                st.dataframe(pd.DataFrame(eligible)[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
            else:
                st.info("✅ You are up to date! No new courses available.")

# --- 📅 ROUTINE MAKER ---
elif menu == "📅 Routine Maker":
    st.header("📅 Automatic Routine Generator")
    st.caption("Upload your UMS Class Schedule CSV to find conflict-free routines.")
    
    # Sample Download
    sample_data = pd.DataFrame({'Course String': ['CSE265.1', 'CSE265.2', 'MAT261.1'], 'Faculty': ['Mr. X', 'Ms. Y', 'Dr. Z'], 'Day': ['Sun', 'Tue', 'Mon'], 'Time': ['08:30 AM', '10:00 AM', '02:00 PM']})
    st.download_button("📥 Download Sample CSV", sample_data.to_csv(index=False).encode('utf-8'), "sample_routine.csv")
    
    uploaded_file = st.file_uploader("Upload Routine File", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        # Pre-processing
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
            
            # Cartesian Product Logic
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
                    st.error("❌ Conflict found in all combinations. Try changing sections.")

# --- 💰 TUITION CALCULATOR ---
elif menu == "💰 Tuition Calculator":
    st.header("💸 SEU Tuition Fee Calculator")
    st.markdown("Calculate your exact payable amount including **Waiver & Extra Costs**.")
    
    # Tuition Rates (Updated for Spring 2026 Approx)
    dept_rates = {
        "CSE": 3500, "EEE": 3400, "BBA": 3200, "English": 2500, "Textile": 3000, "Pharmacy": 4000
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Course Details")
        dept = st.selectbox("Department", list(dept_rates.keys()))
        per_credit = st.number_input("Cost Per Credit (BDT)", value=dept_rates[dept], step=100)
        credits = st.number_input("Total Credits Taking", min_value=3, max_value=20, value=12)
        
        st.subheader("🎁 Waiver Percentage")
        waiver = st.select_slider("Select Waiver %", options=[0, 10, 20, 30, 40, 50, 60, 70, 80, 100], value=20)
        
    with col2:
        st.subheader("➕ Additional Semester Costs")
        semester_fee = st.number_input("Semester Fee (Fixed)", value=6000, help="Library, Student Activity, etc.")
        lab_fee = st.number_input("Lab Fee (Total)", value=3000, help="Usually 1500-3000 based on labs.")
        bus_fee = st.number_input("Transport/Bus Fee", value=0)
        other_fee = st.number_input("Club/Other Fees", value=0)

    # Calculation
    gross_tuition = credits * per_credit
    waiver_amount = gross_tuition * (waiver / 100)
    net_tuition = gross_tuition - waiver_amount
    total_fixed = semester_fee + lab_fee + bus_fee + other_fee
    total_payable = net_tuition + total_fixed
    
    st.divider()
    
    # Visualization
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("📊 Cost Breakdown")
        labels = ['Net Tuition', 'Semester Fee', 'Lab Fee', 'Bus Fee', 'Others']
        values = [net_tuition, semester_fee, lab_fee, bus_fee, other_fee]
        
        # Donut Chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
        fig.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("💵 Payment Summary")
        st.markdown(f"""
        <div style="background-color: #2E2E2E; padding: 20px; border-radius: 10px;">
            <p style="margin:0;">Gross Tuition: <b>{gross_tuition:,.0f} BDT</b></p>
            <p style="margin:0; color: #ff4b4b;">Less Waiver ({waiver}%): <b>- {waiver_amount:,.0f} BDT</b></p>
            <hr>
            <h2 style="margin:0; color: #4CAF50;">Total Payable: {total_payable:,.0f} BDT</h2>
            <p style="font-size: 12px; color: #aaa;">(Including all non-waivable fees)</p>
        </div>
        """, unsafe_allow_html=True)

# --- 🗺️ CAMPUS MAP ---
elif menu == "🗺️ Campus Map":
    st.header("📍 SEU Permanent Campus (Tejgaon)")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        # SEU Coordinates
        seu_map = pd.DataFrame({'lat': [23.768603], 'lon': [90.402638]})
        st.map(seu_map, zoom=16)
    
    with col2:
        st.info("**Address:**\n251/A & 252, Tejgaon I/A, Dhaka-1208, Bangladesh")
        st.write("**Contact:** 02-8878502")
        st.link_button("🚗 Google Maps Direction", "https://goo.gl/maps/ExampleLink")

# --- 👨‍🏫 FACULTY INFO ---
elif menu == "👨‍🏫 Faculty Info":
    st.header("👨‍🏫 CSE Faculty Members")
    
    fac_data = [
        {"Name": "Shahriar Manzoor", "Designation": "Chairman & Assoc. Prof", "Room": "402", "Email": "chairman@seu.edu.bd"},
        {"Name": "Dr. Gazi Zahirul Islam", "Designation": "Professor", "Room": "405", "Email": "zahirul@seu.edu.bd"},
        {"Name": "Md. Shohel Babu", "Designation": "Lecturer (Coordinator)", "Room": "301", "Email": "shohel@seu.edu.bd"},
        {"Name": "Lameya Islam", "Designation": "Lecturer", "Room": "302", "Email": "lameya@seu.edu.bd"},
    ]
    st.table(pd.DataFrame(fac_data))

# --- 🧮 CGPA CALCULATOR ---
elif menu == "🧮 CGPA Calculator":
    st.header("🧮 Semester CGPA Calculator")
    
    col1, col2 = st.columns(2)
    with col1: num = st.number_input("Number of Courses", 1, 10, 4)
    
    credits = []
    points = []
    
    st.write("Enter Course Details:")
    cols = st.columns(4)
    for i in range(num):
        with cols[i % 4]:
            c = st.number_input(f"Cr. {i+1}", 1.0, 4.0, 3.0, key=f"c{i}")
            g = st.selectbox(f"GPA {i+1}", [4.0, 3.75, 3.5, 3.25, 3.0, 2.75, 2.5, 2.0, 0.0], key=f"g{i}")
            credits.append(c)
            points.append(c * g)
            
    if st.button("Calculate SGPA"):
        total_p = sum(points)
        total_c = sum(credits)
        sgpa = total_p / total_c
        
        st.balloons()
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #4F8BF9; border-radius: 10px;">
            <h1 style="color: white; margin:0;">SGPA: {sgpa:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)
