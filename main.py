import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Page Setup ---
st.set_page_config(page_title="SEU Smart Adviser", page_icon="🎓", layout="wide")
st.title("🎓 SEU Student Course Planner")

# --- Tabs ---
tab1, tab2 = st.tabs(["📘 Course Advising (Syllabus)", "📅 Routine Generator (Future)"])

# ==========================================
# TAB 1: SYLLABUS & PREREQUISITE CHECKER
# ==========================================
with tab1:
    st.header("Step 1: Which courses can I take?")
    
    # Load Curriculum Data
    try:
        curr_df = pd.read_csv("curriculum.csv")
        curr_df['Prerequisite'] = curr_df['Prerequisite'].fillna('None')
    except FileNotFoundError:
        st.error("❌ 'curriculum.csv' not found. Please create it first.")
        st.stop()

    # User Input: Completed Courses
    all_courses_list = curr_df['Course Code'].tolist()
    
    st.write("### Select courses you have ALREADY completed:")
    completed = st.multiselect("Completed Courses", all_courses_list, default=['CSE141', 'MAT141'])
    
    # Logic: Check Eligibility
    eligible_courses = []
    
    if st.button("Check Eligibility"):
        st.subheader("✅ You are eligible for these courses:")
        
        for index, row in curr_df.iterrows():
            course = row['Course Code']
            prereqs = row['Prerequisite']
            
            # Skip if already completed
            if course in completed:
                continue
            
            # Logic for Freshers (No Prereq)
            if prereqs == 'None':
                eligible_courses.append(row)
                continue
                
            # Logic for Advanced Courses
            req_list = prereqs.split(';') # Handle multiple prereqs (e.g., CSE241;CSE242)
            is_eligible = True
            for req in req_list:
                if req not in completed:
                    is_eligible = False
                    break
            
            if is_eligible:
                eligible_courses.append(row)
        
        # Display Result
        if eligible_courses:
            res_df = pd.DataFrame(eligible_courses)
            st.dataframe(res_df[['Course Code', 'Course Title', 'Credits', 'Prerequisite']], use_container_width=True)
            st.info(f"Total Available Credits: {sum(c['Credits'] for c in eligible_courses)}")
        else:
            st.warning("No new courses available based on your selection.")

# ==========================================
# TAB 2: SMART ROUTINE GENERATOR
# ==========================================
with tab2:
    st.header("Step 2: Generate Routine (When published)")
    st.markdown("""
    When the university publishes the **Class Routine**, create a CSV file named `ums_data.csv` 
    with columns: `Course String`, `Faculty`, `Day`, `Time`.
    """)
    
    # File Uploader for Future Use
    uploaded_file = st.file_uploader("Upload your Routine CSV", type=["csv"])
    
    if uploaded_file is not None:
        # --- SAME LOGIC AS BEFORE ---
        df = pd.read_csv(uploaded_file)
        
        # Helper Functions
        def calculate_end_time(start_time_str):
            try:
                # Assuming standard format handling
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

        # Data Processing
        df[['Course Code', 'Section']] = df['Course String'].apply(lambda x: pd.Series(parse_course_string(x)))
        times = df['Time'].apply(calculate_end_time)
        df['Start_DT'] = [t[0] for t in times]
        df['End_DT'] = [t[1] for t in times]
        df = df.dropna(subset=['Start_DT']) # Remove invalid times

        # Selection UI
        st.divider()
        unique_codes = sorted(df['Course Code'].unique())
        selected_for_routine = st.multiselect("Select Courses for Routine:", unique_codes)
        
        priority_faculty = st.text_input("Preferred Faculty Name (Optional):")
        
        if st.button("Generate Routine"):
            # Filtering Logic
            relevant_data = df[df['Course Code'].isin(selected_for_routine)].copy()
            
            # Faculty Scoring
            relevant_data['Score'] = 0
            if priority_faculty:
                relevant_data.loc[relevant_data['Faculty'].str.contains(priority_faculty, case=False, na=False), 'Score'] = 10
            
            relevant_data = relevant_data.sort_values(by='Score', ascending=False)
            
            # Combination Logic
            course_groups = []
            for code in selected_for_routine:
                secs = relevant_data[relevant_data['Course Code'] == code]
                if not secs.empty:
                    course_groups.append(secs.to_dict('records'))
            
            import itertools
            if course_groups:
                combinations = list(itertools.product(*course_groups))
                valid_routines = []
                
                for combo in combinations:
                    r_check = [{'Day': i['Day'], 'Start': i['Start_DT'], 'End': i['End_DT']} for i in combo]
                    score_sum = sum(i['Score'] for i in combo)
                    
                    if not check_conflict(r_check):
                        valid_routines.append((combo, score_sum))
                
                # Show Results
                valid_routines.sort(key=lambda x: x[1], reverse=True)
                
                if valid_routines:
                    st.success(f"Found {len(valid_routines)} Options!")
                    for idx, (routine, score) in enumerate(valid_routines[:3]):
                        st.write(f"**Option {idx+1}** {'⭐ Recommended' if score > 0 else ''}")
                        st.table(pd.DataFrame(routine)[['Course String', 'Faculty', 'Day', 'Time']])
                else:
                    st.error("Conflict found in all combinations!")
    else:
        st.info("👋 Routine file not uploaded yet. You can use the 'Advising' tab for now!")