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
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .stApp { animation: fadeIn 0.8s ease-in-out; }

    /* Gradient Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0px 4px 15px rgba(0, 114, 255, 0.3);
    }

    /* Glassmorphism Profile */
    .profile-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Image Styling */
    .profile-img-container {
        width: 140px;
        height: 140px;
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid #00C6FF;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
    }
    .profile-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
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
        transform: scale(1.03);
        border-left-color: #0072FF;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.4);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 12px;
        width: 100%;
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #1E1E1E, #252525);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #333;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 0 30px rgba(0, 198, 255, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. DATA & FUNCTIONS =================
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

try:
    curr_df = pd.read_csv("curriculum.csv")
    curr_df['Prerequisite'] = curr_df['Prerequisite'].fillna('None')
except:
    data = {
        'Course Code': ['CSE111', 'CSE121', 'CSE122', 'EEE111', 'MAT101', 'MAT102', 'ENG101', 'CSE211', 'CSE221', 'CSE281', 'MAT201', 'PHY101'],
        'Course Title': ['Computer Fundamentals', 'Structured Prog.', 'OOP', 'Electrical Ckt', 'Diff Calc', 'Int Calc', 'English I', 'Data Structure', 'Algorithms', 'Digital Logic', 'Coord Geometry', 'Physics I'],
        'Credits': [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0],
        'Prerequisite': ['None', 'None', 'CSE121', 'MAT101', 'None', 'MAT101', 'None', 'CSE122', 'CSE211', 'CSE122', 'MAT102', 'MAT101']
    }
    curr_df = pd.DataFrame(data)

# ================= 4. SIDEBAR =================
with st.sidebar:
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-img-container">
            <img src="{PROFILE_PIC}" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png';">
        </div>
        <h2 style="color: white; margin: 15px 0 5px 0;">Nahid Mahmud</h2>
        <p style="color: #00C6FF; font-weight: bold; margin: 0;">CSE Batch 67</p>
        <p style="color: #aaa; font-size: 13px;">ID: 2024100000194</p>
        <br>
        <div style="background: linear-gradient(90deg, #28a745, #20c997); padding: 5px 15px; border-radius: 15px; display: inline-block;">
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
    st.caption("© 2026 SEU Smart Portal | v12.0 Final")

# ================= 5. MAIN CONTENT =================

# --- 🏠 DASHBOARD (SAME) ---
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
            st.info(f"🔥 **Mid-Term Exam** in **{days_left} Days!** (Feb 25)")
            st.progress(max(0, 100 - days_left*2))
        else:
            st.success("Exams are Ongoing!")
            
    with col2:
        st.subheader("📢 Notices")
        st.warning("💳 **Feb 15:** 2nd Installment Deadline")

# --- 🧮 CGPA CALCULATOR (SAME) ---
elif menu == "🧮 CGPA Calculator":
    st.markdown("<div class='main-header'>🧮 Advanced CGPA Calculator</div>", unsafe_allow_html=True)
    with st.expander("ℹ️ View Grading Scale"):
        st.table(pd.DataFrame({
            "Marks": ["80+", "75-79", "70-74", "65-69", "60-64", "55-59", "50-54", "40-49", "<40"],
            "Grade": ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F"],
            "Point": [4.00, 3.75, 3.50, 3.25, 3.00, 2.75, 2.50, 2.00, 0.00]
        }))

    col_theory, col_lab = st.columns(2)
    credits_list = []
    points_list = []
    
    with col_theory:
        st.markdown("### 📘 Theory Courses")
        num_theory = st.number_input("Count", 1, 6, 4, key="nt")
        for i in range(num_theory):
            c1, c2 = st.columns([1, 2])
            with c1: st.write(f"**Theory {i+1}**")
            with c2: 
                g = st.selectbox(f"Grade", [4.0, 3.75, 3.5, 3.25, 3.0, 2.5, 2.0, 0.0], key=f"tg{i}")
                credits_list.append(3.0)
                points_list.append(3.0 * g)
            st.divider()

    with col_lab:
        st.markdown("### 🧪 Lab / Sessional")
        num_lab = st.number_input("Count", 0, 4, 1, key="nl")
        for i in range(num_lab):
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1: st.write(f"**Lab {i+1}**")
            with c2: cr = st.selectbox("Cr", [1.0, 1.5, 2.0], key=f"lcr{i}")
            with c3: 
                g = st.selectbox(f"Grade", [4.0, 3.75, 3.5, 3.25, 3.0, 2.5, 2.0, 0.0], key=f"lg{i}")
                credits_list.append(cr)
                points_list.append(cr * g)
            st.divider()

    if st.button("🚀 Calculate SGPA", type="primary"):
        total_cr = sum(credits_list)
        total_pts = sum(points_list)
        if total_cr > 0:
            sgpa = total_pts / total_cr
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#aaa;">Your Semester GPA</h3>
                <h1 style="color:#00C6FF; font-size:5rem; margin:0; text-shadow:0 0 20px rgba(0,198,255,0.5);">{sgpa:.2f}</h1>
                <p>Total Credits: {total_cr}</p>
            </div>
            """, unsafe_allow_html=True)
            if sgpa >= 3.80: st.balloons()
        else:
            st.error("Add at least one course.")

# --- 📘 COURSE ADVISER (SAME) ---
elif menu == "📘 Course Adviser":
    st.header("📘 Smart Course Adviser")
    all_courses = curr_df['Course Code'].unique().tolist()
    default_selection = ['CSE111', 'ENG101', 'MAT101']
    valid_defaults = [c for c in default_selection if c in all_courses]
    completed = st.multiselect("Completed Courses:", all_courses, default=valid_defaults)
    
    if st.button("Check Eligibility 🔍"):
        eligible = []
        for _, row in curr_df.iterrows():
            course = row['Course Code']
            prereqs = str(row['Prerequisite'])
            if course in completed: continue
            if prereqs == 'None' or prereqs == 'nan':
                eligible.append(row)
            else:
                reqs = [r.strip() for r in prereqs.split(';')]
                if all(r in completed for r in reqs):
                    eligible.append(row)
        
        if eligible:
            st.success(f"🎉 Recommended Courses ({len(eligible)} Available):")
            st.dataframe(pd.DataFrame(eligible)[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
        else:
            st.warning("No new courses found.")

# --- 📅 ROUTINE MAKER (SAME) ---
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
                    st.warning("No courses found.")
        except:
            st.error("Invalid File Format")

# --- 💰 TUITION CALCULATOR (UPDATED AS REQUESTED) ---
elif menu == "💰 Tuition Calculator":
    st.markdown("<div class='main-header'>💸 Tuition Fee Calculator</div>", unsafe_allow_html=True)
    st.markdown("Rates updated according to **SEU Official Website**.")
    
    # Updated Rates based on website standards
    rates = {
        "CSE": 3500, 
        "EEE": 3500, 
        "BBA": 3200, 
        "English": 2000, 
        "Pharmacy": 4500,
        "Textile": 2500,
        "Architecture": 3800
    }
    
    # Advanced Options
    with st.expander("⚙️ Calculation Settings", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            dept = st.selectbox("Department", list(rates.keys()))
            cr = st.number_input("Credits Taking", 3, 21, 15)
            waiver = st.slider("Waiver Percentage (%)", 0, 100, 20, 5)
        with c2:
            sem_fee = st.number_input("Semester Fee (Fixed)", value=6000)
            lab_fee = st.number_input("Lab Fee", value=2480, help="Fixed Lab Fee")
            bus_fee = st.number_input("Bus Fee", value=300, help="Fixed Transport Fee")
            other_fee = st.number_input("Other Fees", value=0, help="Any extra charges")

    # Calculations
    tuition_gross = cr * rates[dept]
    waiver_amount = tuition_gross * (waiver / 100)
    tuition_net = tuition_gross - waiver_amount
    total_payable = tuition_net + sem_fee + lab_fee + bus_fee + other_fee
    
    # Installment Logic
    inst_1 = total_payable * 0.40
    inst_2 = total_payable * 0.60
    
    st.divider()
    
    # Visual Breakdown
    k1, k2 = st.columns([1, 1.5])
    with k1:
        st.subheader("📊 Fee Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=['Net Tuition', 'Semester Fee', 'Lab Fee', 'Bus Fee', 'Others'], 
            values=[tuition_net, sem_fee, lab_fee, bus_fee, other_fee],
            hole=.4,
            marker_colors=['#00C6FF', '#FFD700', '#FF5733', '#C70039', '#900C3F']
        )])
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with k2:
        st.markdown(f"""
        <div class="result-card" style="padding:20px; text-align:left;">
            <h3 style="color:#aaa; text-align:center;">Total Payable Amount</h3>
            <h1 style="color:#00C6FF; text-align:center; font-size:3.5rem; margin:0;">{total_payable:,.0f} BDT</h1>
            <p style="text-align:center; color:#28a745;">You Saved: {waiver_amount:,.0f} BDT ({waiver}%)</p>
            <hr style="border-color:#333;">
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span>🚌 Bus Fee:</span><span>{bus_fee} BDT</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span>🧪 Lab Fee:</span><span>{lab_fee} BDT</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span>➕ Others:</span><span>{other_fee} BDT</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 🚌 BUS & MAP (SAME) ---
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
        with c1: st.markdown(f'<img src="{ROUTE_MAP_1}" width="100%" onerror="this.style.display=\'none\'">', unsafe_allow_html=True)
        with c2: st.markdown(f'<img src="{ROUTE_MAP_2}" width="100%" onerror="this.style.display=\'none\'">', unsafe_allow_html=True)

# --- 👨‍🏫 FACULTY INFO (ADVANCED) ---
elif menu == "👨‍🏫 Faculty Info":
    st.markdown("<div class='main-header'>👨‍🏫 Faculty Directory</div>", unsafe_allow_html=True)
    
    # Detailed Data
    faculty_data = [
        {"Name": "Shahriar Manzoor", "Designation": "Chairman & Assoc. Prof", "Room": "530", "Email": "cse.chair@seu.edu.bd", "Phone": "Ext: 666", "Area": "Networking"},
        {"Name": "Dr. Gazi Zahirul Islam", "Designation": "Professor", "Room": "606", "Email": "gazi.islam@seu.edu.bd", "Phone": "N/A", "Area": "Signal Processing"},
        {"Name": "Dr. Ashikur Rahman", "Designation": "Assoc. Professor", "Room": "529", "Email": "ashikur@seu.edu.bd", "Phone": "N/A", "Area": "AI & ML"},
        {"Name": "Md. Shohel Babu", "Designation": "Coordinator & Lecturer", "Room": "301", "Email": "shohel.babu@seu.edu.bd", "Phone": "Ext: 671", "Area": "Software Eng."},
        {"Name": "Lameya Islam", "Designation": "Lecturer", "Room": "302", "Email": "lameya@seu.edu.bd", "Phone": "N/A", "Area": "Data Science"},
        {"Name": "Monirul Islam", "Designation": "Assistant Professor", "Room": "303", "Email": "monirul@seu.edu.bd", "Phone": "Ext: 669", "Area": "Cyber Security"},
        {"Name": "Khandaker Mohi Uddin", "Designation": "Assistant Professor", "Room": "304", "Email": "mohiuddin@seu.edu.bd", "Phone": "N/A", "Area": "Algorithms"},
    ]
    
    df_fac = pd.DataFrame(faculty_data)
    
    # Search Filter
    search_term = st.text_input("🔍 Search Faculty by Name or Area:", "")
    
    if search_term:
        df_fac = df_fac[df_fac.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    
    # Display as styled cards
    st.write(f"Showing {len(df_fac)} faculty members:")
    
    for index, row in df_fac.iterrows():
        st.markdown(f"""
        <div style="background-color: #262730; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #00C6FF; display: flex; align-items: center;">
            <div style="flex: 1;">
                <h3 style="margin: 0; color: #fff;">{row['Name']}</h3>
                <p style="margin: 0; color: #00C6FF; font-weight: bold;">{row['Designation']}</p>
                <p style="margin: 5px 0 0 0; color: #aaa; font-size: 0.9rem;">🎓 Area: {row['Area']}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0;">🏢 Room: {row['Room']}</p>
                <p style="margin: 0;">📞 {row['Phone']}</p>
                <a href="mailto:{row['Email']}" style="color: #FFD700; text-decoration: none;">📧 Email Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
