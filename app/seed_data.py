import random
from faker import Faker
from app.database import SessionLocal
from app import models
from app.utils.security import hash_password

fake = Faker('en_IN')  # Using Indian locale for realistic SIT names

# --- BRANCH DATA CONFIG ---
BRANCH_DATA = {
    "AIML": ["Supervised Machine Learning", "NLP", "Deep Learning", "Computer Vision", "Reinforcement Learning",
             "PyTorch", "TensorFlow", "RAG", "Agentic AI", "Prompt Engineering"],
    "CSE": ["Data Structures", "Operating Systems", "Cloud Computing", "FastAPI", "Docker", "Kubernetes",
            "Cybersecurity", "React", "GoLang", "PostgreSQL", "System Design"],
    "ENTC": ["Embedded Systems", "VLSI Design", "Signal Processing", "Arduino", "Raspberry Pi", "IoT", "PCB Design",
             "Digital Communication", "MATLAB", "FPGA"],
    "RNA": ["Robot Kinematics", "ROS (Robot Operating System)", "Control Systems", "PLC Programming", "SolidWorks",
            "Path Planning", "Industrial Automation", "Computer-Aided Manufacturing"],
    "MECH": ["Thermodynamics", "Fluid Mechanics", "AutoCAD", "Ansys", "Mechatronics", "IC Engines", "Heat Transfer",
             "Finite Element Analysis", "CNC Programming"],
    "CIVIL": ["Structural Analysis", "Geotechnical Engineering", "Surveying", "Revit", "Transportation Engineering",
              "Construction Management", "Hydrology", "Concrete Technology"]
}

BATCH_MAP = {
    "2022-26": "btech2022",
    "2023-27": "btech2023",
    "2024-28": "btech2024",
    "2025-29": "btech2025"
}


def seed_campus():
    db = SessionLocal()
    print("🚀 Starting Mega-Seed: Generating 120 Students...")

    for i in range(120):
        # 1. Generate Identity
        first_name = fake.first_name()
        last_name = fake.last_name()
        branch = random.choice(list(BRANCH_DATA.keys()))
        batch = random.choice(list(BATCH_MAP.keys()))

        # 2. Construct SIT Email: firstname.lastname.btechXXXX@sitpune.edu.in
        email_year = BATCH_MAP[batch]
        email = f"{first_name.lower()}.{last_name.lower()}.{email_year}{i}@sitpune.edu.in"

        # 3. Create User
        user = models.User(
            full_name=f"{first_name} {last_name}",
            email=email,
            hashed_password=hash_password("password123"),
            branch=branch,
            batch=batch
        )
        db.add(user)
        db.flush()  # Get user ID

        # 4. Pick Skills (3 from branch, 2 from "Extra/General")
        branch_skills = random.sample(BRANCH_DATA[branch], 3)
        # Mix in 2 random skills from ANY other branch to simulate "Interdisciplinary" students
        all_other_skills = [s for b, s_list in BRANCH_DATA.items() if b != branch for s in s_list]
        extra_skills = random.sample(all_other_skills, 2)

        final_skill_names = branch_skills + extra_skills

        for s_name in final_skill_names:
            # Check if skill exists globally, if not, create
            db_skill = db.query(models.Skill).filter(models.Skill.name == s_name).first()
            if not db_skill:
                db_skill = models.Skill(name=s_name)
                db.add(db_skill)
                db.flush()

            user.skills.append(db_skill)

    db.commit()
    db.close()
    print(f"✅ SIT Campus Seeded! 120 students added across {len(BRANCH_DATA)} branches.")


if __name__ == "__main__":
    seed_campus()