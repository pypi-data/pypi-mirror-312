import os
import streamlit as st

script_path = os.path.dirname(os.path.realpath(__file__))


def run():
    pages = {
        "AdminPanel": [
            st.Page(f"{script_path}/nodes.py", title="Nodes", icon=":material/table:"),
            st.Page(f"{script_path}/services.py", title="Services", icon=":material/table:"),
            st.Page(f"{script_path}/tasks.py", title="Tasks", icon=":material/table:")
        ],
        "Documents": [
            st.Page(f"{script_path}/user_manual.py", title="UserManual")
        ]
    }

    pg = st.navigation(pages)
    pg.run()


if __name__ == '__main__':
    run()
