from tkinter import *
import sys, os, json

sys.path.insert(0,'/Users/BramanthaPatra/A2Git/smartofficeA2/smartoffice/smartoffice')
import api_caller

class mainWindow(object):
    # shows the main GUI
    def __init__(self,master):
        """Initialize window"""
        self.master=master
        self.l=Label(master,text="Welcome to our clinic check in system! Have you ever used this machine before?")
        self.l.pack()
        self.b=Button(master,text="Yes",command=self.have_used)
        self.b.pack()
        self.b2=Button(master,text="No",command=self.have_not_used)


        self.b2.pack()

    # if the patient has previously used the machine, it'll automatically run the recognisation code
    def have_used(self):
        """Delete everythings from the window and run recognise code"""
        self.b.destroy()
        self.b2.destroy()
        os.system("python3 03_recognise.py")

    # otherwise, it'll prompt the user to enter their name
    def have_not_used(self):
        """Prompt user to input their name"""
        self.l.configure(text="Please enter your Name")
        self.b.destroy()
        self.b2.destroy()
        self.l2=Label(text="Name:")
        self.l2.pack()
        self.e=Entry()
        self.e.pack()
        self.b3=Button(text='Ok',command=self.cleanup)
        self.b3.pack()

    # loops through the patient object,
    # if the input name matches the one in database,
    # it'll automatically run capture and recognise code
    def cleanup(self):
        """Check if the name is existed in the system"""
        self.value=self.e.get()

        patients = api_caller.get_patients()
        patients_dumps = json.dumps(patients, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        patients_loads = json.loads(patients_dumps)

        for patient in patients_loads:
            if patient['name'] == self.value:
                os.system("python3 01_capture.py -n {}".format(self.value))
                os.system("python3 03_recognise.py")
            else:
                self.l2.destroy()
                self.e.destroy()
                self.b3.destroy()
                self.l.configure(text="You have not been registered in the database")

    def entryValue(self):
        """Get the Value"""
        return self.w.value



if __name__ == "__main__":
    root=Tk()
    m=mainWindow(root)
    root.mainloop()