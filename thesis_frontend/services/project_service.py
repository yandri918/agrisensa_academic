import json
import os
import streamlit as st

DATA_FILE = "data/rab_projects.json"

class ProjectManager:
    @staticmethod
    def _ensure_data_dir():
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    @staticmethod
    def _load_db():
        ProjectManager._ensure_data_dir()
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def _save_db(data):
        ProjectManager._ensure_data_dir()
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def save_project(name, project_data):
        """
        Save project data (dict) with a unique name.
        project_data should include: crop, params (pop, price, etc), items (list of dicts), area inputs.
        """
        db = ProjectManager._load_db()
        db[name] = project_data
        ProjectManager._save_db(db)
        # Update Session State to reflect active project
        st.session_state['active_project_name'] = name

    @staticmethod
    def delete_project(name):
        db = ProjectManager._load_db()
        if name in db:
            del db[name]
            ProjectManager._save_db(db)
            if st.session_state.get('active_project_name') == name:
                st.session_state['active_project_name'] = None

    @staticmethod
    def load_project(name):
        db = ProjectManager._load_db()
        return db.get(name, None)

    @staticmethod
    def get_all_projects_list():
        db = ProjectManager._load_db()
        return list(db.keys())
