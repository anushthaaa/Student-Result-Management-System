class User:
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def authentication(self, email, password):
        return self.email == email and self.password == password
    
    def display_info(self):
        return f"{self.name} | ID: {self.student_id}"

class Student(User):
    def __init__(self, email, password, name, student_id, semester=None):
        super().__init__(email, password, name)
        self.student_id = student_id
        self.semester = semester

class Admin(User):
    def __init__(self, email, password, name, employe_id):
        super().__init__(email, password, name)
        self.employe_id = employe_id 