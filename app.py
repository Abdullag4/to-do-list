import streamlit as st
import json
import requests
import os

# GitHub Repo Settings
GITHUB_REPO = "your_github_username/your_repo_name"
GITHUB_FILE = "tasks.json"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Store token in Streamlit secrets

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"

# Load tasks from GitHub
def load_tasks():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code == 200:
        content = response.json()
        return json.loads(requests.get(content["download_url"]).text)
    else:
        return []

# Save tasks to GitHub
def save_tasks(tasks):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    # Get current file SHA (needed for updating the file)
    response = requests.get(GITHUB_API_URL, headers=headers)
    sha = response.json().get("sha", "")

    # Prepare request payload
    payload = {
        "message": "Update tasks",
        "content": json.dumps(tasks, indent=2).encode("utf-8").decode("utf-8"),
        "sha": sha,
    }

    # Update the file
    requests.put(GITHUB_API_URL, headers=headers, json=payload)

# Streamlit App Layout
st.title("📝 Personal To-Do List")

# Load existing tasks
tasks = load_tasks()

# Display tasks
st.subheader("Your Tasks:")
for i, task in enumerate(tasks):
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

    col1.text(task["task"])
    if col2.button("✅ Done", key=f"done_{i}"):
        tasks.pop(i)
        save_tasks(tasks)
        st.experimental_rerun()
    if col3.button("❌ Remove", key=f"remove_{i}"):
        tasks.pop(i)
        save_tasks(tasks)
        st.experimental_rerun()

# Add a new task
st.subheader("Add a New Task:")
new_task = st.text_input("Enter task:", key="new_task")
if st.button("➕ Add Task"):
    if new_task:
        tasks.append({"task": new_task})
        save_tasks(tasks)
        st.experimental_rerun()
    else:
        st.warning("Task cannot be empty!")

st.success("✅ Tasks are saved automatically!")
