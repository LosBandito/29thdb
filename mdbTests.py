import random
import sqlite3
from datetime import datetime


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

            self.conn.execute("""
                       CREATE TABLE IF NOT EXISTS awards (
                           id INTEGER PRIMARY KEY,
                           award_name TEXT NOT NULL,
                           award_description TEXT ,
                           award_image_bg TEXT ,
                           award_image_sm TEXT 
                       )
                   """)

            # Soldier Awards Linking table
            self.conn.execute("""
                       CREATE TABLE IF NOT EXISTS soldier_awards (
                           soldier_id INTEGER NOT NULL,
                           award_id INTEGER NOT NULL,
                           award_date DATE,
                           PRIMARY KEY (soldier_id, award_id),
                           FOREIGN KEY (soldier_id) REFERENCES soldiers (id),
                           FOREIGN KEY (award_id) REFERENCES awards (id)
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
            # Demerits table
            self.conn.execute("""
               CREATE TABLE IF NOT EXISTS demerits (
                    id INTEGER PRIMARY KEY,
                    demerit_name TEXT NOT NULL,
                    demerit_description TEXT,
                    demerit_signature TEXT NOT NULL
                )

           """)

            # Soldier Awards Linking table
            self.conn.execute("""
               CREATE TABLE IF NOT EXISTS soldier_demerits (
                   soldier_id INTEGER NOT NULL,
                   demerit_id INTEGER NOT NULL,
                   demerit_date DATE,
                   PRIMARY KEY (soldier_id, demerit_id),
                   FOREIGN KEY (soldier_id) REFERENCES soldiers (id),
                   FOREIGN KEY (demerit_id) REFERENCES demerits (id)
               )
           """)

    # Solider Functions
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

    def remove_soldier(self, soldier_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM soldiers WHERE id=?", (soldier_id,))

    def get_leadership(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM soldiers WHERE leadership = 1")
            return cur.fetchall()

    # Units functions
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

    def get_soldiers_by_unit(self, unit_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM soldiers WHERE unit_id=?", (unit_id,))
            return [dict(zip(["id", "name", "age", "address", "rank", "ait", "unit_id"], row)) for row in
                    cur.fetchall()]

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

    # Award Functions
    def add_award_to_soldier(self, soldier_id, award_id, ):
        now = datetime.now()
        now = now.strftime("%m/%d/%Y, %H:%M:%S")
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO soldier_awards (soldier_id, award_id, award_date) VALUES (?, ?, ?)",
                (soldier_id, award_id, now))

    def remove_award_from_soldier(self, soldier_id, award_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "DELETE FROM soldier_awards WHERE soldier_id = ? AND award_id = ?",
                (soldier_id, award_id))

    def get_all_awards(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM awards")
            return cur.fetchall()

    def get_awards_by_soldier(self, soldier_id):
        with self.conn:
            cur = self.conn.cursor()

            # Use a JOIN to get award details
            query = """
            SELECT a.award_name, a.award_description, a.award_image_bg, a.award_image_sm
            FROM soldier_awards sa
            JOIN awards a ON sa.award_id = a.id
            WHERE sa.soldier_id = ?
            """

            cur.execute(query, (soldier_id,))
            return cur.fetchall()

    def create_award(self, award_name, award_desc, award_image_bg, award_image_sm):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO awards (award_name ,award_description , award_image_bg, award_image_sm) VALUES (?, ?, ?, ?)",
                (award_name, award_desc, award_image_bg, award_image_sm))
            return cur.lastrowid

    # Demerit Functions

    from datetime import datetime

    def add_demerit_to_soldier(self, soldier_id, demerit_name, demerit_description=None, demerit_signature=None):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO demerits (demerit_name, demerit_description, demerit_signature) VALUES (?, ?, ?)",
                (demerit_name, demerit_description, demerit_signature))
            demerit_id = cur.lastrowid

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO soldier_demerits (soldier_id, demerit_id, demerit_date) VALUES (?, ?, ?)",
                (soldier_id, demerit_id, now))

    def remove_demerit_from_soldier(self, soldier_id, demerit_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "DELETE FROM soldier_demerits WHERE soldier_id = ? AND demerit_id = ?",
                (soldier_id, demerit_id))

    def get_soldier_demerits(self, soldier_id):
        with self.conn:
            cur = self.conn.cursor()

            # Use a JOIN to get demerit details for a specific soldier
            query = """
            SELECT d.id, d.demerit_name, d.demerit_description, d.demerit_signature
            FROM soldier_demerits sd
            JOIN demerits d ON sd.demerit_id = d.id
            WHERE sd.soldier_id = ?
            """

            cur.execute(query, (soldier_id,))
            return cur.fetchall()

    def get_all_soldier_demerits(self):
        with self.conn:
            cur = self.conn.cursor()
            query = """
            SELECT s.id as soldier_id, s.name as soldier_name, 
                   d.id as demerit_id, d.demerit_name, d.demerit_description, d.demerit_signature
            FROM soldier_demerits sd
            JOIN demerits d ON sd.demerit_id = d.id
            JOIN soldiers s ON sd.soldier_id = s.id
            """

            cur.execute(query)
            return cur.fetchall()

    def get_demerits_for_soldier(self, soldier_id):
        with self.conn:
            cur = self.conn.cursor()

            query = """
            SELECT s.id as soldier_id, s.name as soldier_name, 
                   d.id as demerit_id, d.demerit_name, d.demerit_description, d.demerit_signature
            FROM soldier_demerits sd
            JOIN demerits d ON sd.demerit_id = d.id
            JOIN soldiers s ON sd.soldier_id = s.id
            WHERE s.id = ?
            """

            cur.execute(query, (soldier_id,))
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
                 platoon=None, squad=None, battalion=None, leadership=None, awards=None):
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
db = MilitaryDatabase('29awards.db')
db.create_tables()

first_names = ["John", "Sam", "Jack", "Jill", "Mike", "Anna", "Chris", "Ella", "David", "Sophia"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
awards = [['Distinguished Service Cross',
           'Exceptional in every regard. The highest honor attainable in the 29th Infantry Division.',
           'https://uploads.29th.org/personnel/award/dsc/presentation_image/b79e8800dada91614c77412317017e5a.gif',
           'https://uploads.29th.org/personnel/award/dsc/ribbon_image/77e8dd1aad7e22e2305aa9dd703f298b.gif'],
          ['Silver Star',
           "This soldier has demonstrated perfect performance whilst engaging with the enemy, that not only single-handedly secured victory for his team, but demonstrated the core principles of being an effective soldier in the 29th Infantry Division. This medal is only awarded when the soldier's game-play was at a level of the highest calibre.",
           'https://uploads.29th.org/personnel/award/sstar/presentation_image/efd943ea578bc16743301fb119b8e922.gif',
           'https://uploads.29th.org/personnel/award/sstar/ribbon_image/a2c2dec1825bad54c05acc2cc8e78740.gif'],
          ['Legion of Merit', 'Awarded for leading and winning an Official Scrimmage.',
           'https://uploads.29th.org/personnel/award/lom/presentation_image/a22de3df6fa15027a314966c752e3a25.gif',
           'https://uploads.29th.org/personnel/award/lom/ribbon_image/922d220d43e3f1f3ed03b60c257e7831.gif'],
          ["Soldier's Medal",
           "This soldier's extensive preparation during practice or drills prior to a scrimmage or drill prevented casualties by providing vital intelligence or training for his team.",
           'https://uploads.29th.org/personnel/award/sm/presentation_image/71b755fff6d8fff3fd12c76ca5efd3cd.gif',
           'https://uploads.29th.org/personnel/award/sm/ribbon_image/34ec26747edc64cb2a19995895e90c51.gif'],
          ['Bronze Star',
           'This soldier has demonstrated exemplary performance while engaging the enemy in a realism scrimmage. While not single handedly securing victory, his actions must have been of significance.',
           'https://uploads.29th.org/personnel/award/bstar/presentation_image/b71b61aab40d25c7f7a77231a8ba274f.gif',
           'https://uploads.29th.org/personnel/award/bstar/ribbon_image/d2172c3a3f6f28d200621ace4ec0f3c3.gif'],
          ['Purple Heart',
           'This soldier has selflessly put him self in peril to successfully aid his comrades and in doing so was wounded or killed.',
           'https://uploads.29th.org/personnel/award/pheart/presentation_image/772cd1e4a151684782765456e7d4830a.gif',
           'https://uploads.29th.org/personnel/award/pheart/ribbon_image/53b2b5223bbbb70d8b830c5a51169228.gif'],
          ['Distinguished Service Medal',
           'Awarded to soldiers who have carried out duty successfully and responsibly. Contributing not only what is expected in the 29th, but who has made contributions above and beyond the expectations of any member in the 29th.',
           'https://uploads.29th.org/personnel/award/dsm/presentation_image/65eb048d8c1520a6e7651caa43f4dbf4.gif',
           'https://uploads.29th.org/personnel/award/dsm/ribbon_image/140a00e3eb2ca01534fcad49b98474ab.gif'],
          ['Good Conduct Medal',
           "In addition to performing his duties with a clean record of discipline and exemplary attendance, this soldier's positive attitude and involvement in 29th related activities, other than his drills or staff commitments, has benefited the unit.",
           'https://uploads.29th.org/personnel/award/gcon/presentation_image/74269cddf500529872f82f12d28a9e2a.gif',
           'https://uploads.29th.org/personnel/award/gcon/ribbon_image/126ccda7cbd2d77b01d7a7c98d9bd70b.gif'],
          ['Army Commendation Medal',
           'This soldier has maintained composure and made an effective contribution towards his teams victory without necessarily engaging the enemy. This award is for actions of significance not covered by a Bronze or Silver Star.',
           'https://uploads.29th.org/personnel/award/arcom/presentation_image/89fc85a59efaded2ae12081dcd03c3ea.gif',
           'https://uploads.29th.org/personnel/award/arcom/ribbon_image/673819ba64647452cfa212989195ac19.gif'],
          ['Army of Occupation Medal', 'Served six months of service in the 29th Infantry Division',
           'https://uploads.29th.org/personnel/award/aocc/presentation_image/f69328bdf4e8ae6e2deee0233e73e3d7.gif',
           'https://uploads.29th.org/personnel/award/aocc/ribbon_image/2dd7294808a1ee00b1481c57310ca5f0.gif'],
          ['European-African-Middle Eastern Campaign Medal',
           'Only awarded to the participants that win an attack round of an official scrimmage.',
           'https://uploads.29th.org/personnel/award/eamc/presentation_image/272608c50605d98d881bb9ddd9b4c846.gif',
           'https://uploads.29th.org/personnel/award/eamc/ribbon_image/a1e56dd4b180ec7c2c7bc4c4da08c02b.gif'],
          ['American Defense Service Medal', "Soldier has graduated the 29th ID's Basic Training program",
           'https://uploads.29th.org/personnel/award/adef/presentation_image/c8e7f6a9114999106cdd3a29a7c87e63.gif',
           'https://uploads.29th.org/personnel/award/adef/ribbon_image/2b4c6cd8614bd60c16f3810673e5cbb5.gif'],
          ['French Croix de Guerre Medal',
           'Awarded for leadership contributions that greatly benefit the Battalion as a whole.',
           'https://uploads.29th.org/personnel/award/french/presentation_image/d0d530dfe57b39078d19f910774ce6a5.gif',
           'https://uploads.29th.org/personnel/award/french/ribbon_image/c583b5135fe7fc9d666d4d0b13f282a0.gif'],
          ['Drill Sergeant Badge', 'Unit Drill Sergeant',
           'https://uploads.29th.org/personnel/award/drillsergeant/presentation_image/2f47d92166657e5c0f07f5dee1c0a557.gif',
           None], ['Combat Infantry Badge, 1st Award',
                   'Awarded to a soldier after their 1st scrimmage with another realism unit.',
                   'https://uploads.29th.org/personnel/award/cib1/presentation_image/35971fb4aa4f89a8c02d6ec52ae4c231.gif',
                   None], ['Combat Infantry Badge, 2nd Award',
                           'Awarded to a soldier after their 3rd scrimmage with another realism unit.',
                           'https://uploads.29th.org/personnel/award/cib2/presentation_image/44275ec2f10d8353031161a198a5e884.gif',
                           None], ['Combat Infantry Badge, 3rd Award',
                                   'Awarded to a soldier after their 5th scrimmage with another realism unit',
                                   'https://uploads.29th.org/personnel/award/cib3/presentation_image/4bb0a8d720f38672e4d2a599457f9574.gif',
                                   None], ['Expert Infantry Badge',
                                           'Awarded to men who prove themselves experts in all aspects of Infantry and is required for soldiers to participate in combat.',
                                           'https://uploads.29th.org/personnel/award/eib/presentation_image/74ad8dd7e146315f542907a7f5102a3a.gif',
                                           None],
          ['The Trenches Unit Participation', 'Participated in The Trenches Unit campaign',
           'https://uploads.29th.org/personnel/award/trenches/ribbon_image/2365cd2841ddacc41a7e91eeeb383a00.gif', None],
          ['Battlegrounds Unit Participation', 'Participated in the Battlegrounds Unit campaign',
           'https://uploads.29th.org/personnel/award/battlegrounds/ribbon_image/2698f8984db5412b99ca4b89f41c9cbf.gif',
           None], ['Day of Defeat Unit Participation', 'Participated in the Day of Defeat Unit campaign',
                   'https://uploads.29th.org/personnel/award/dod/ribbon_image/94fa4a04a992d975d1f562d220adf645.gif',
                   None],
          ['Meritorious Unit Citation', 'Most exemplary and skilled squad in the company (Transfers every month)',
           'https://uploads.29th.org/personnel/award/muc/presentation_image/a1a9ea329d49c828ab9b6ac31b33216b.png',
           'https://uploads.29th.org/personnel/award/muc/ribbon_image/c8bceed827620532c1d0701ffd7e1631.gif'],
          ['American Campaign Medal', 'Awarded for exemplary leadership on or off the battlefield.',
           'https://uploads.29th.org/personnel/award/acamp/presentation_image/08751d795dbceea3f536b6fbf0055648.gif',
           'https://uploads.29th.org/personnel/award/acamp/ribbon_image/4151401c517ef53f7fe7fce20a689858.gif'],
          ['Combat Action Badge, 1st Award',
           "This will be awarded by the Recruitment Officer, to a member of the 29th Infantry Division who has successfully recruited 2 recruits for that week's Training Platoon.",
           'https://uploads.29th.org/personnel/award/cab1/presentation_image/e07b1af33f54c225477867f39c0eb645.gif',
           None], ['Combat Action Badge, 2nd Award',
                   "This will be awarded by the Recruitment Officer, to a member of the 29th Infantry Division who has successfully recruited 5 recruits for that week's Training Platoon.",
                   'https://uploads.29th.org/personnel/award/cab2/presentation_image/96a737c214cb1f6a70178ab89a57049e.gif',
                   None], ['Combat Action Badge, 3rd Award',
                           "This will be awarded by the Recruitment Officer, to a member of the 29th Infantry Division who has successfully recruited 10 recruits for that week's Training Platoon.",
                           'https://uploads.29th.org/personnel/award/cab3/presentation_image/d0dd9c33f5fbf16b4e6cdebfdc6ff7ef.gif',
                           None], ['Combat Action Badge, 4th Award',
                                   "This will be awarded by the Recruitment Officer, to a member of the 29th Infantry Division who has successfully recruited 20 recruits for that week's Training Platoon.",
                                   'https://uploads.29th.org/personnel/award/cab4/presentation_image/2b33fadf807b8bf15e7d787171ecf233.gif',
                                   None], ['Recruiter Badge',
                                           'This will be awarded by the Commanding Officer, based upon reports from the Recruitment Officer, to a member of the 29th Infantry Division who has successfully shown consitency as being one of the top recruiters for over a month.',
                                           'https://uploads.29th.org/personnel/award/recruiter/presentation_image/c3e8af5ca91bc2915ec28dd86f17fbfe.gif',
                                           None],
          ['Darkest Hour Unit Participation', 'Participated in the Darkest Hour Unit campaign',
           'https://uploads.29th.org/personnel/award/dh/ribbon_image/9a335f070d02f05fe64c193b73c3bb10.gif', None],
          ['World War I Victory Medal',
           'This is to be awarded to members who have served for two years, and for each consecutive two years thereafter.',
           'https://uploads.29th.org/personnel/award/ww1v/presentation_image/c61966f829d7d9a8df564dcac411a045.gif',
           None], ['Army Achievement Award',
                   'This soldier has consistently performed his duties in a staff position to the highest calibre and demonstrated the best of non-combat 29th values.',
                   'https://uploads.29th.org/personnel/award/aach/presentation_image/2e479cd47a290772b94debf1c5a37144.gif',
                   'https://uploads.29th.org/personnel/award/aach/ribbon_image/3497c468a947325dbc371f69c747518d.gif'],
          ['Military Police Badge', 'Awarded to Military Police Officers',
           'https://uploads.29th.org/personnel/award/mp/presentation_image/95322923a767bb4f50d8eacb23a856db.gif', None],
          ['Defense Meritorious Service Medal',
           'Only awarded to the participants that win a defence round of an official scrimmage.',
           'https://uploads.29th.org/personnel/award/dms/presentation_image/122b5c52fb04f5b0c465c459c3e12915.gif',
           None], ['World War II (WWII) Victory Medal',
                   'Only awarded to the participants that win every round of a multi-round official scrimmage. Awarding of this medal supercedes the awarding of the African European Middle-Eastern Campaign Medal and the Defence Meritorious Service Medal Ribbon.',
                   'https://uploads.29th.org/personnel/award/ww2v/presentation_image/d31815bb4f41eb23730f3ddcac19efe7.gif',
                   'https://uploads.29th.org/personnel/award/ww2v/ribbon_image/d0d8d086db01de658ee57869bec5722c.gif'],
          ['Rising Storm Unit Participation', 'Participated in the Rising Storm Unit campaign',
           'https://uploads.29th.org/personnel/award/rs/ribbon_image/3c1869e83bcf45de24b7a9b8087c6b21.gif', None],
          ['ARMA Unit Participation', 'Participated in the ARMA Unit campaign',
           'https://uploads.29th.org/personnel/award/arma/ribbon_image/02a81a86c87365ddbcf86790dc7b8799.gif', None],
          ['Army NCO Professional Development Ribbon',
           'This soldier has passed through a Squad Leader Training Program.', None, None],
          ['Military Outstanding Volunteer Service Medal',
           'This soldier has been a major contributor to a large, important and successfully project in a staff office.',
           'https://uploads.29th.org/personnel/award/movsm/presentation_image/e90adda0beb63abe5a6a2269b7fcbf9d.gif',
           'https://uploads.29th.org/personnel/award/movsm/ribbon_image/c7aa468c0e23d36c3723e92bd2513e3b.gif'],
          ['Armed Forces Expeditionary Medal',
           'Awarded for participation in a non-official scrimmage event. Does not apply to public scrimmages. Must be private events that are organized and have a limited, selected roster of participants from 29th.',
           'https://uploads.29th.org/personnel/award/afem/presentation_image/5ad8b569fb55469fed3107fc518f4c29.png',
           None], ['Armed Forces Service Medal',
                   'For Soldiers whom perform staff related duties above and beyond what is required in a staff position.',
                   None, None], ['Meritorious Service Medal',
                                 'Awarded for Service in the 29th that is exemplary as a solid soldier whom has aided and put forth the time and effort to the 29th when asked and not asked.',
                                 'https://uploads.29th.org/personnel/award/msm/presentation_image/77753f54d2eefed572fa66a3929ba894.png',
                                 None], ['Superior Unit Citation',
                                         'Squad excels among all squads at a platoon level. Platoon HQ can award two Superior Citations a year (reviewed every six months).',
                                         'https://uploads.29th.org/personnel/award/suc/presentation_image/a90f0d3f5ee6556a7d45e6f686181085.png',
                                         None], ['Meritorious Public Service Medal',
                                                 'Awarded in recognition of dedication through recurring financial contributions to the upkeep of the unit. Requires minimum contribution for recurring donation system. This medal remains on a members jacket only during active periods of contribution.',
                                                 'https://uploads.29th.org/personnel/award/mpsm/presentation_image/99a494e3eb42936d029ab376d8021947.gif',
                                                 None],
          ['Rising Storm 2 Unit Participation', 'Participated in the Rising Storm 2: Vietnam Unit campaign',
           'https://uploads.29th.org/personnel/award/rs2/ribbon_image/ab1fef4effea5cc31bdbfaa7344e5aaa.gif', None],
          ['Squad Unit Participation', 'Participated in the Squad Unit campaign',
           'https://uploads.29th.org/personnel/award/sq/ribbon_image/abe20ea562874945cb1817ffa4166948.gif', None],
          ['Blue Infantry Cord', 'Awarded for a $10 Recurring Donation', None, None]]

# Generate the hierarchy
battalion_names = ["1st Battalion", "2nd Battalion"]
company_names = ["Easy", "Charlie", "Fox", "Dog"]
image = "https://placehold.co/600x400"
inc = 0

"""
for award in awards:
    db.create_award(awards[inc][0], awards[inc][1], awards[inc][2], awards[inc][3])
    inc += 1
print("Awards added to database")

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
