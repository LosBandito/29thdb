import random


class MilitaryUnit:
    def __init__(self, name):
        self.name = name
        self.soldiers = []

    def add_soldier(self, profile):
        if profile is None:
            print("Profile not found!")
            return
        self.soldiers.append(profile)

    def delete_soldier(self, name, age):
        for soldier in self.soldiers:
            if soldier.name == name and soldier.age == age:
                self.soldiers.remove(soldier)
                break

    def get_soldiers(self):
        print(f"Unit: {self.name}")
        for soldier in self.soldiers:
            print(soldier)


class Battalion(MilitaryUnit):
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


class Company(MilitaryUnit):
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

    def add_soldier(self, profile):
        super().add_soldier(profile)
        profile.platoon = self.name

    def delete_soldier(self, profile, name, age):
        super().delete_soldier(name, age)

        if profile.squad is not None:
            profile.squad = None
            profile.platoon = None


class Squad(MilitaryUnit):
    def add_soldier(self, profile):
        super().add_soldier(profile)
        profile.squad = self.name

    def delete_soldier(self, profile, name, age):
        super().delete_soldier(name, age)

        profile.squad = None


class Profile:
    def __init__(self, name, age, address, id=random.randint(0, 100000), rank="Private", ait="Rifle", company=None,
                 platoon=None, squad=None, battalion=None):
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


names = ["John", "Sam", "Jack", "Jill", "Mike", "Anna", "Chris", "Ella", "David", "Sophia", "Ryan", "Grace", "Brian",
         "Chloe", "Dylan", "Ava", "Ethan", "Emma", "Mason", "Olivia"]

soldiers = [Profile(id=i, name=names[i], age=random.randint(20, 40), address="USA") for i in range(20)]

# Creating Units
first_battalion = Battalion("1st Battalion")
easy_company = Company("Easy Company")
fox_company = Company("Fox Company")
first_platoon = Platoon("1st Platoon")
second_platoon = Platoon("2nd Platoon")
first_squad = Squad("First Squad")
second_squad = Squad("Second Squad")

# Assigning Soldiers to Units
for soldier in soldiers[:5]:
    first_battalion.add_soldier(soldier)
    easy_company.add_soldier(soldier)
    first_platoon.add_soldier(soldier)
    first_squad.add_soldier(soldier)

for soldier in soldiers[5:10]:
    first_battalion.add_soldier(soldier)
    fox_company.add_soldier(soldier)
    second_platoon.add_soldier(soldier)
    first_squad.add_soldier(soldier)

for soldier in soldiers[10:15]:
    first_battalion.add_soldier(soldier)
    easy_company.add_soldier(soldier)
    first_platoon.add_soldier(soldier)
    second_squad.add_soldier(soldier)

# Displaying Soldiers in the Battalion for verification
first_battalion.get_soldiers()
