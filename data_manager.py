import sqlite3

class DataManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients
                            (name TEXT PRIMARY KEY,
                            age INTEGER NOT NULL,
                            sickness TEXT NOT NULL,
                            UNIQUE(name))''')
        self.conn.commit()

    def add_patient(self, name, age, sickness):
        try:
            self.cursor.execute("INSERT INTO patients (name, age, sickness) VALUES (?, ?, ?)", (name, age, sickness))
            self.conn.commit()
            print("Patient added successfully.")
            return True
        except sqlite3.IntegrityError:
            print("Patient with the same name already exists.")
            return False
        
    def find_patient_by_name(self, name):
        self.cursor.execute("SELECT * FROM patients WHERE name=?", (name,))
        return self.cursor.fetchall()

    def delete_patient_by_name(self, name):
        self.cursor.execute("DELETE FROM patients WHERE name=?", (name,))
        self.conn.commit()
        print("Patient deleted successfully.")
    
    def show_all_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        patients = self.cursor.fetchall()
        for patient in patients:
            print(patient) 
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    data_manger = DataManager("patients.db")
    data_manger.show_all_patients()
    #print(data_manger.find_patient_by_name('Mir'))
