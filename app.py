import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Rare Nova", page_icon="🧪", layout="wide")

# ---------- USERS ----------
if "users" not in st.session_state:
    # Initial users
    st.session_state.users = {
        "admin": {"password": "1234", "role": "admin"},
        "teacher1": {"password": "pass123", "role": "user"},
        "teacher2": {"password": "abc456", "role": "user"},
    }

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "allocations" not in st.session_state:
    st.session_state.allocations = []

# ---------- LOGIN ----------
def login():
    st.title("🔐 Rare Nova - Login Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and password == st.session_state.users[username]["password"]:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful ✅")
            st.stop()
        else:
            st.error("Invalid Username or Password ❌")

# ---------- DASHBOARD ----------
def dashboard():
    if not st.session_state.logged_in or not st.session_state.user:
        st.error("User session not found. Please login again.")
        st.stop()

    role = st.session_state.users[st.session_state.user]["role"]

    # Sidebar
    st.sidebar.info(f"Logged in as: **{st.session_state.user}** ({role})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.stop()

    st.title("🚀 Rare Nova - AI Lab Resource Optimiser")

    tabs = st.tabs(["Lab Allocation", "AI Suggestions", "Current Allocations"] + (["Manage Users"] if role == "admin" else []))

    departments = ["CSE", "IT", "ECE", "EEE", "MECH"]
    classes = ["1st Year", "2nd Year", "3rd Year", "Final Year"]
    labs = ["AI Lab", "Networking Lab", "IoT Lab", "Programming Lab"]
    time_slots = [
        "9:00 AM - 10:00 AM",
        "10:00 AM - 11:00 AM",
        "11:00 AM - 12:00 PM",
        "1:00 PM - 2:00 PM",
        "2:00 PM - 3:00 PM"
    ]

    # ---------- LAB ALLOCATION ----------
    with tabs[0]:
        st.subheader("📌 Allocate Lab & Time Slot")
        col1, col2 = st.columns(2)
        with col1:
            selected_dept = st.selectbox("Department", departments)
            selected_class = st.selectbox("Class", classes)
        with col2:
            selected_lab = st.selectbox("Lab", labs)
            selected_time = st.selectbox("Time Slot", time_slots)

        students = st.number_input("Number of Students", 0, 100)

        dept_index = departments.index(selected_dept)
        class_index = classes.index(selected_class)
        predicted_max = 25 + class_index*5 + dept_index*2

        st.info(f"💡 AI Suggested Max Students: {predicted_max}")
        if students > predicted_max:
            st.warning("⚠ Above AI recommended capacity")
        else:
            st.success("✅ Lab Available")

        if role == "admin":
            if st.button("Save Allocation"):
                allocation = {
                    "Department": selected_dept,
                    "Class": selected_class,
                    "Lab": selected_lab,
                    "Time Slot": selected_time,
                    "Students": students,
                    "Saved By": st.session_state.user
                }
                st.session_state.allocations.append(allocation)
                st.success("✅ Allocation Saved")

    # ---------- AI SUGGESTIONS ----------
    with tabs[1]:
        st.subheader("🤖 AI Suggestions")
        for dept in departments:
            for cls in classes:
                suggested = 25 + classes.index(cls)*5 + departments.index(dept)*2
                st.success(f"{dept} - {cls}: Suggested Max Students = {suggested}")

    # ---------- CURRENT ALLOCATIONS ----------
    with tabs[2]:
        st.subheader("📋 Current Allocations")
        if not st.session_state.allocations:
            st.info("No allocations yet")
        else:
            for alloc in st.session_state.allocations:
                color = "#e0f7fa" if alloc["Lab"] == "AI Lab" else \
                        "#fff3e0" if alloc["Lab"] == "Networking Lab" else \
                        "#f3e5f5" if alloc["Lab"] == "IoT Lab" else "#e8f5e9"
                st.markdown(
                    f"""
                    <div style='background-color:{color}; padding:10px; border-radius:8px; margin-bottom:5px'>
                    <b>Department:</b> {alloc['Department']} | 
                    <b>Class:</b> {alloc['Class']} | 
                    <b>Lab:</b> {alloc['Lab']} | 
                    <b>Time Slot:</b> {alloc['Time Slot']} | 
                    <b>Students:</b> {alloc['Students']} | 
                    <b>Saved By:</b> {alloc['Saved By']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ---------- MANAGE USERS TAB (ADMIN ONLY) ----------
    if role == "admin":
        with tabs[3]:
            st.subheader("🛠 Manage Users")
            new_user = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            new_role = st.selectbox("Role", ["user", "admin"])
            if st.button("Add User"):
                if new_user in st.session_state.users:
                    st.error("User already exists ❌")
                elif new_user == "":
                    st.warning("Username cannot be empty ⚠")
                else:
                    st.session_state.users[new_user] = {"password": new_password, "role": new_role}
                    st.success(f"User '{new_user}' added ✅")

            st.markdown("**Current Users:**")
            for u, info in st.session_state.users.items():
                st.write(f"- {u} ({info['role']})")
            

# ---------- RUN APP ----------
if not st.session_state.logged_in:
    login()
else:
    dashboard()
