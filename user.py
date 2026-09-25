class User:
    def __init__(self, Name, PhoneNumber, Email, Gender, Governorate, Password, Age, National_ID):
        self.name = Name
        self.phone_number = PhoneNumber
        self.email = Email
        self.gender = Gender
        self.governorate = Governorate
        self.password = Password
        self.age = Age
        self.national_id = National_ID
        self.role = 'user'
        self.learning_plan = []

