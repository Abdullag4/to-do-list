import streamlit as st
import pandas as pd
import os

# File to store tasks
TASKS_FILE = "tasks.csv"

# Load tasks from CSV
def load_tasks():
    if os.path.exists(TASKS_FILE):
        return pd.read_csv(TASKS_FILE)
    return pd.DataFrame(columns=["Task", "Completed"])

# Save tasks to CSV
def save_tasks(tasks_df):
    tasks_df.to_csv(TASKS_FILE, index=False)

# Initialize app
st.title("✅ To-Do List App")

# Load existing tasks
tasks_df = load_tasks()

# Add new task
new_task = st.text_input("Enter a new task:")
if st.button("Add Task") and new_task.strip():
    tasks_df = pd.concat([tasks_df, pd.DataFrame([[new_task, False]], columns=["Task", "Completed"])], ignore_index=True)
    save_tasks(tasks_df)
    st.experimental_rerun()

# Display tasks
st.subheader("Your Tasks:")
for index, row in tasks_df.iterrows():
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
    col1.write(f"✅ {row['Task']}" if row["Completed"] else f"🔲 {row['Task']}")
    
    if col2.button("✔️ Done", key=f"done_{index}"):
        tasks_df.at[index, "Completed"] = True
        save_tasks(tasks_df)
        st.experimental_rerun()
    
    if col3.button("❌ Remove", key=f"remove_{index}"):
        tasks_df = tasks_df.drop(index).reset_index(drop=True)
        save_tasks(tasks_df)
        st.experimental_rerun()
