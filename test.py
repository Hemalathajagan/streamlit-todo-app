import streamlit as st

st.set_page_config(page_title="Simple To-Do App", page_icon="✅", layout="centered")

# --- Helpers -------------------------------------------------
def add_task(task_text):
    if task_text:
        st.session_state.todos.append({"text": task_text, "done": False})

def remove_task(idx):
    st.session_state.todos.pop(idx)

def toggle_done(idx):
    st.session_state.todos[idx]["done"] = not st.session_state.todos[idx]["done"]

def edit_task(idx, new_text):
    if new_text:
        st.session_state.todos[idx]["text"] = new_text

def clear_completed():
    st.session_state.todos = [t for t in st.session_state.todos if not t["done"]]

# --- Initialize session state --------------------------------
if "todos" not in st.session_state:
    st.session_state.todos = []  # list of {"text": str, "done": bool}

# --- UI ------------------------------------------------------
st.title("✅ Simple To-Do List")
st.write("Add tasks, mark them done, edit, or delete. Tasks persist while this session runs.")

# Form to add a new task
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("New task", placeholder="e.g. Finish assignment")
    submitted = st.form_submit_button("Add task")
    if submitted:
        add_task(new_task)

st.markdown("---")

# Show counts and controls
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.info(f"Total: {len(st.session_state.todos)}")
with col2:
    done_count = sum(1 for t in st.session_state.todos if t["done"])
    st.success(f"Done: {done_count}")
with col3:
    if st.button("Clear completed"):
        clear_completed()

st.markdown("### Tasks")

# If no tasks
if not st.session_state.todos:
    st.write("No tasks yet. Add one above! 🎉")
else:
    # Display tasks. Use enumerate so keys are stable.
    for idx, task in enumerate(st.session_state.todos):
        # container to nicely group controls for each task
        with st.container():
            cols = st.columns([0.05, 0.6, 0.35])
            # checkbox (toggle done)
            checked = cols[0].checkbox("", value=task["done"], key=f"chk-{idx}", on_change=toggle_done, args=(idx,))
            # text or editable input
            if task["done"]:
                cols[1].markdown(f"~~{task['text']}~~")
            else:
                cols[1].write(task["text"])
            # action buttons: edit and delete
            if cols[2].button("Edit", key=f"edit-{idx}"):
                # show edit input in a modal-like simple way
                new_text = st.text_input("Edit task", value=task["text"], key=f"edit-input-{idx}")
                if st.button("Save", key=f"save-{idx}"):
                    edit_task(idx, new_text)
                    st.experimental_rerun()
            if cols[2].button("Delete", key=f"del-{idx}"):
                remove_task(idx)
                st.experimental_rerun()
