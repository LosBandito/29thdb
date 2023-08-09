import random
import sqlite3


class MilitaryDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_tables(self):
        with self.conn:
            # Soldiers table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS soldiers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    address TEXT NOT NULL,
                    rank TEXT NOT NULL,
                    ait TEXT NOT NULL,
                    unit_id INTEGER,
                    leadership INTEGER DEFAULT 0,
                    FOREIGN KEY (unit_id) REFERENCES units (id)
                )
            """)


            # Units table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS units (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    image TEXT NOT NULL,
                    parent_unit_id INTEGER,
                    FOREIGN KEY (parent_unit_id) REFERENCES units (id)
                )
            """)
            # Soldier-Unit relationship table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS soldier_units (
                    soldier_id INTEGER NOT NULL,
                    unit_id INTEGER NOT NULL,
                    PRIMARY KEY (soldier_id, unit_id),
                    FOREIGN KEY (soldier_id) REFERENCES soldiers (id),
                    FOREIGN KEY (unit_id) REFERENCES units (id)
                )
            """)

    def retrieve_all_soldiers(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM soldiers")
            return cur.fetchall()

    def retrieve_units_by_parent(self, parent_unit_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM units WHERE parent_unit_id=?", (parent_unit_id,))
            return cur.fetchall()

    def add_soldier(self, name, age, address, rank, ait, unit_id, leadership):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO soldiers (name, age, address, rank, ait, unit_id, leadership) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, age, address, rank, ait, unit_id, int(leadership)))
            return cur.lastrowid

    def get_leadership(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM soldiers WHERE leadership = 1")
            return cur.fetchall()

    def add_unit(self, name, unit_type, image, parent_unit_id=None):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO units (name, type, image, parent_unit_id) VALUES (?, ?, ?, ?)",
                (name, unit_type, image, parent_unit_id))
            return cur.lastrowid

    def assign_soldier_to_unit(self, soldier_id, unit_id):
        with self.conn:
            self.conn.execute("INSERT INTO soldier_units (soldier_id, unit_id) VALUES (?, ?)",
                              (soldier_id, unit_id))

    def retrieve_all_units(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT id, name FROM units")
            units = [dict(zip(["id", "name", "image"], row)) for row in cur.fetchall()]
            return units

    def update_unit_image(self, unit_id, new_image):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE units SET image = ? WHERE id = ?",
                (new_image, unit_id))

    def get_soldiers_by_unit(self, unit_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM soldiers WHERE unit_id=?", (unit_id,))
            return cur.fetchall()


    def close(self):
        self.conn.close()


class MilitaryUnit:
    def __init__(self, name, db, image, unit_type, parent_unit_id=None, ):
        self.name = name
        self.soldiers = []
        self.db = db
        self.image = image
        self.unit_type = unit_type
        self.parent_unit_id = parent_unit_id
        self.id = self.db.add_unit(name, unit_type, image, parent_unit_id)

    def add_soldier(self, soldier):
        self.soldiers.append(soldier)
        soldier_id = self.db.add_soldier(soldier.name, soldier.age, soldier.address, soldier.rank, soldier.ait, self.id,
                                         soldier.leadership)

    def get_subordinate_units(self):
        return self.db.retrieve_units_by_parent(self.id)

    def set_image(self, image):
        self.image = image
        self.db.update_unit_image(self.id, image)


class Battalion(MilitaryUnit):
    def __init__(self, name, db, image):
        super().__init__(name, db, image, unit_type="Battalion")

    def add_soldier(self, profile):
        super().add_soldier(profile)
        profile.battalion = self.name

    def delete_soldier(self, profile, name, age):
        super().delete_soldier(name, age)

        if profile.squad is not None:
            profile.squad = None
            profile.platoon = None
            profile.company = None
            profile.battalion = None

    def change_image(self, image):
        super().change_image(image)


class Company(MilitaryUnit):
    def __init__(self, name, db, image, parent_unit_id):
        super().__init__(name, db, image, unit_type="Company", parent_unit_id=parent_unit_id)

    def add_soldier(self, profile):
        super().add_soldier(profile)
        profile.company = self.name

    def delete_soldier(self, profile, name, age):
        super().delete_soldier(name, age)

        if profile.squad is not None:
            profile.squad = None
            profile.platoon = None
            profile.company = None


class Platoon(MilitaryUnit):
    def __init__(self, name, db, image, parent_unit_id):
        super().__init__(name, db, image, unit_type="Platoon", parent_unit_id=parent_unit_id)

    def add_soldier(self, profile):
        super().add_soldier(profile)
        profile.platoon = self.name

    def delete_soldier(self, profile, name, age):
        super().delete_soldier(name, age)

        if profile.squad is not None:
            profile.squad = None
            profile.platoon = None

    def change_image(self, image):
        super().change_image(image)


class Squad(MilitaryUnit):
    def __init__(self, name, db, image, parent_unit_id):
        super().__init__(name, db, image, unit_type="Squad", parent_unit_id=parent_unit_id)

    def add_soldier(self, profile):
        super().add_soldier(profile)
        profile.squad = self.name

    def delete_soldier(self, profile, name, age):
        super().delete_soldier(name, age)

        profile.squad = None

    def change_image(self, image):
        super().change_image(image)


class Profile:
    def __init__(self, name, age, address, id=random.randint(0, 100000), rank="Private", ait="Rifle", company=None,
                 platoon=None, squad=None, battalion=None, leadership=None,awards=None):
        self.id = id
        self.name = name
        self.age = age
        self.address = address
        self.rank = rank
        self.ait = ait
        self.demerit = []
        self.company = company
        self.platoon = platoon
        self.squad = squad
        self.battalion = battalion
        self.leadership = leadership
        self.awards = awards

    def __str__(self):
        assignment = f"Assigment: {self.battalion or '-'} {self.company or '-'} {self.platoon or '-'} {self.squad or '-'}"
        return f"{assignment}\nID: {self.id}\nName: {self.name}\nAge: {self.age}\nAddress: {self.address} \nRank: {self.rank}\nait: {self.ait}\nDemerits: {self.demerit}"


class ProfileManager:
    def __init__(self, ):
        self.profiles = []
        self.rankList = ["Private", "Corporal", "Sergeant", "Lieutenant", "Captain", "Major", "Colonel", "General"]
        self.ait = ["Rifle", "CE", "Medic", "GL", "AR"]

    def add_profile(self, profile):
        profile.id = random.randint(0, 100000)
        self.profiles.append(profile)

    def get_profiles(self, ):
        for i in self.profiles:
            print(i)

    def search_profile(self, name, age):
        for i in self.profiles:
            if i.name == name and i.age == age:
                print("Profile found")
                return i

    def delete_profile(self, name, age):
        for i in self.profiles:
            if i.name == name and i.age == age:
                self.profiles.remove(i)
                break

    def update_rank(self, name, age, ):
        for i in self.profiles:
            if i.name == name and i.age == age:
                print("Select new rank")
                for rank in self.rankList:
                    print(rank)
                newRank = input("Enter new rank: ")
                if newRank in self.rankList:
                    i.rank = newRank
                else:
                    print("Invalid rank")
                break

    def update_ait(self, name, age):
        for i in self.profiles:
            if i.name == name and i.age == age:
                print("Select new AIT")
                for i in self.ait:
                    print(i)
                newAIT = input("Enter new AIT: ")
                if newAIT in self.ait:
                    continue
                else:
                    print("Invalid AIT")
                    break
            i.ait = newAIT

    def add_demerit(self, name, age):
        for i in self.profiles:
            if i.name == name and i.age == age:
                print("Add demerit")
                demerit = input("Enter demerit: ")
                i.demerit.append(demerit)
                print("Demerit added")


names = ["John", "Sam", "Jack", "Jill", "Mike", "Anna", "Chris", "Ella", "David", "Sophia",
         "Ryan", "Grace", "Brian", "Chloe", "Dylan", "Ava", "Ethan", "Emma", "Mason", "Olivia"]

addresses = ["123 Elm St", "456 Maple Ave", "789 Oak Dr", "101 Pine Rd", "202 Birch Ln"]

ranks = ["Private", "Private First Class", "Corporal", "Sergeant", "Staff Sergant", "Master Sergant",
         "Second Lieutenant", "First Lieutenant", "Captain", "Major", "Colonel", ]

aits = ["AR", "CE", "GL", "Rifle", "Crewman"]

# Generate a list of 20 soldiers
soldiers = [
    Profile(
        name=random.choice(names),
        age=random.randint(20, 40),
        address=random.choice(addresses),
        rank=random.choice(ranks),
        ait=random.choice(aits)
    )
    for _ in range(20)
]

# Initialize the database and create tables
db = MilitaryDatabase('29test.db')
db.create_tables()
first_names = ["John", "Sam", "Jack", "Jill", "Mike", "Anna", "Chris", "Ella", "David", "Sophia"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]

# Generate the hierarchy
battalion_names = ["1st Battalion", "2nd Battalion"]
company_names = ["Easy", "Charlie", "Fox", "Dog"]
image = "https://placehold.co/600x400"
"""
for battalion_name in battalion_names:
    battalion = Battalion(battalion_name, db, image)
    # Add 1-2 leaders for each battalion
    for _ in range(random.randint(1, 2)):
        soldier_name = random.choice(first_names) + " " + random.choice(last_names)
        is_leader = 1
        soldier = Profile(name=soldier_name, age=random.randint(20, 40),
                          address=random.choice(addresses), rank=random.choice(ranks),
                          ait=random.choice(aits), leadership=is_leader)
        battalion.add_soldier(soldier)

    for company_name in company_names:
        company = Company(company_name, db, image, battalion.id)
        # Add 1-2 leaders for each company
        for _ in range(random.randint(1, 2)):
            soldier_name = random.choice(first_names) + " " + random.choice(last_names)
            is_leader = 1
            soldier = Profile(name=soldier_name, age=random.randint(20, 40),
                              address=random.choice(addresses), rank=random.choice(ranks),
                              ait=random.choice(aits), leadership=is_leader)
            company.add_soldier(soldier)

        for platoon_num in range(1, 5):  # 4 platoons per company
            platoon_name = f"Platoon {platoon_num} of {company_name}"
            platoon = Platoon(platoon_name, db, image, company.id)
            # Add 1-2 leaders for each platoon
            for _ in range(random.randint(1, 2)):
                soldier_name = random.choice(first_names) + " " + random.choice(last_names)
                is_leader = 1
                soldier = Profile(name=soldier_name, age=random.randint(20, 40),
                                  address=random.choice(addresses), rank=random.choice(ranks),
                                  ait=random.choice(aits), leadership=is_leader)
                platoon.add_soldier(soldier)

            for squad_num in range(1, 5):  # 4 squads per platoon
                squad_name = f"Squad {squad_num} of {platoon_name}"
                squad = Squad(squad_name, db, image, platoon.id)

                # For the sake of this example, let's assign 10 soldiers to each squad
                for i in range(1, 11):
                    soldier_name = random.choice(first_names) + " " + random.choice(last_names)
                    # Make the first soldier in each squad a leader
                    is_leader = i == 1
                    soldier = Profile(name=soldier_name, age=random.randint(20, 40),
                                      address=random.choice(addresses), rank=random.choice(ranks),
                                      ait=random.choice(aits), leadership=is_leader)
                    squad.add_soldier(soldier)


"""
