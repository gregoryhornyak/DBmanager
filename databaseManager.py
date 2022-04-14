from os import stat, system as sys
from os.path import exists
import json
import datetime

class Database:
    def __init__(self, filename, **kwarg):
        self.db = {}  # database
        #! outsource to function
        if exists(filename):
            with open(filename) as db_file:
                self.db = json.load(db_file)
        #!
        self.attributes = []
        self.filename = filename
        self.name = "name"
        if "lang" in kwarg and kwarg["lang"] == "hun":
            self.name = "név"
            input("language set to hungarian")
            print("language set to hungarian")
        self._newline_in_logs()
        self._logger("database created")
        self._logger("save into file: "+filename)
            
    def _logger(self,message:str):
        """
        input: message
        output: txt file
        """
        message = message.replace("á", "a")
        message = message.replace("í", "i")
        message = message.replace("é", "e")
        message = message.replace("ó", "o")
        message = message.replace("ö", "o")
        message = message.replace("ő", "o")
        message = message.replace("ü", "u")
        message = message.replace("ű", "u")
        message = message.replace("ú", "u")
        
        f1 = open("logs.txt", "a")
        today = datetime.datetime.now()
        log = str(today.strftime("%d/%m/%Y %H:%M:%S")) + " | " + message + "\n"
        try:
            f1.write(log)
        except Exception as e:
            t_msg = " ".join(str(e).split()[2:6])
            temp_str = str(today.strftime("%d/%m/%Y %H:%M:%S")) + " | " + t_msg + "\n"
            f1.write(temp_str)
        finally:
            f1.close()
            
    def _newline_in_logs(self):
        f1 = open("logs.txt", "a")
        f1.write("\n")
        f1.close()
        
    def _get_max_id(self):
        maxx=-1
        for id,val in self.db.items():
            if int(id) > maxx:
                maxx = int(id)
        return maxx+1
        
    def menu_loop(self): # menu
        id=self._get_max_id()  # id of each item
        loop = True
        self._logger("started loop")
        while loop:
            sys("cls")
            if self.name == "név":
                print("HUN")
            # list attributes  
            self._check_n_print_attributes()
            # get user input of list of attributes and values
            ui,choice = self._analyse_user_input()
            if choice == 1: # store input
                if self._store_input(ui,id):
                    id += 1 # increase id
            elif choice == 2: # print out dictionary
                self._print_db()
            elif choice == 3: # undo last insertion
                self._undo_item(id)
            elif choice == 4: #quit
                #loop = False
                loop = self._end_process()
            elif choice == 5: # import db from file
                self._import_db()
            elif choice == 6: #help
                self._print_help()
            elif choice == 7: # delete item
                self._delete_item()
            else:
                print("NO INPUT")
            self._save_db()
        self._logger("loop ended")
        self._logger("quit for program")

    def _delete_item(self):
        #! or self._print_db()
        print("Items in db:")
        for id,val in self.db.items():
            print(id,":",val[self.name])
        #! 
        ui = self._get_user_input(msg="Type in idx of item",int=True)
        pop_item = self.db.pop(ui,None)
        self._logger("deleted: "+str(pop_item))

    def _check_n_print_attributes(self):
        # collect attributes
        self.attributes = []
        for v in self.db.values():
            for k in v.keys():
                if k not in self.attributes:
                    self.attributes.append(k)
        self._logger("attributes: "+str(self.attributes))
        # print out existing attributes
        for a in self.attributes:
            print(a,end=", ")
        print()
        
    def _print_db(self):
        self._logger("printed db")
        print(self.filename,"\n")
        # enumerate is good for style, bad for order
        for e,dicto in enumerate(self.db.items()):
            print("Item",e,end="'s ")
            for k,v in dicto[1].items():
                print(k,":",v,end=" | ")
            print()
        self._wait()
    
    def _wait(self):
        input("\n\npress any key to continue...")

    def _save_db(self):
        try:
            with open(self.filename, "w") as outfile:
                json.dump(self.db, outfile)
            print("Successfully saved db")
            self._logger("saved db")
        except Exception as e:
            print(e)
    
    def _end_process(self):
        self._logger("about to end process")
        ui = input("\nAre you sure you want to quit?\n< ").lower()
        return not self._ans_is_yes(ui)
    
    def _get_user_input(self,**kwargs:str):
        """
        msg: is to be printed out
        int: return int
        """
        is_int = False
        msg = ""
        if kwargs:
            if "msg" in kwargs:
                msg = kwargs["msg"]
            if "int" in kwargs:
                is_int = True
        if is_int:
            ui = int(input(msg+"\n< "))
        else:     
            ui = input(msg+"< ").lower()
        return ui
    
    def _undo_item(self,id):
        pop_item = self.db.pop(id-1,None)
        print("Popped item:",pop_item)
        self._logger("popped item: "+str(pop_item))
        self._wait()
        
    def _analyse_user_input(self):
        #ui = input("< ").lower()
        ui = self._get_user_input()
        choice = 0
        if ui in ["database","db","listhem","list","print"]:
            choice = 2
        elif ui in ["undo"]:
            choice = 3
        elif ui in ["delete","erase","pop"]:
            choice = 7
        elif ui in ["exit","end","quit","escape"]:
            choice = 4
        elif ui in ["import","imp","load db"]:
            choice = 5
        elif ui == "":
            pass
        elif ui == "help":
            choice = 6
        elif "=" in ui:
            choice = 1
        else:
            pass
        self._logger(ui+" -> choice: "+str(choice))
        return ui,choice 

    def _ans_is_yes(self,ui):
        """
        binary check user input
        return: true if yes
                false if not yes 
        """
        #! question could be also included here
        #!   and passed as parameter
        if ui in ["yes", "y", "aha", "si"]:
            self._logger("answer is yes")
            return True
        return False

    def _check_item_existence(self,in_dict):
        item_name = in_dict[self.name]
        occurances = {}
        for id, val in self.db.items():
            if val == in_dict:
                print("already in db")
                self._logger(item_name + "is already in db with same details")
                self._wait()
                return "upd", id  # same items, typed in twice
            for k,v in val.items():
                if v == item_name and k == "name":
                    occurances[id] = val
        if occurances: # if not empty
            for id, val in occurances.items():
                for k,v in val.items():
                    if k == "name":                
                        print("\n",id,"Item with name",v,
                                "already exists in db.")
                        print("Details:",val)
                        self._logger(v+" name is already existing")
            # leave or not
            ui = self._get_user_input(msg="Would you like to update?")
            #ui = input("Would you like to update?\n< ").lower()
            if self._ans_is_yes(ui): # yes
                # ask which one
                ui_id = self._get_user_input(msg="Which one?",int=True)
                #ui_id = int(input("Which one?\n< "))
                self._logger("updated "+ui_id)
                return "upd",ui_id # update request
        return "leave", 0 # leave request
    
    def _store_input(self,ui,id):
        stored = False
        ui = ui.split(",") # split input to words
        temp_dict = {} # create temporary dictionary
        try:
            for statement in ui:
                equal_sign_idx = statement.find("=")
                key = statement[:equal_sign_idx].strip()
                value = statement[equal_sign_idx+1:].strip()
                self._logger(key+" : "+value)
                if key == value:
                    input("key and value are the same")
                    self._logger("key and value are the same")
                    return stored
                else:
                    temp_dict[key] = value
                    stored = True
        except Exception as e:
            input(e)

        # check if item exists
        try:
            command, id_old = self._check_item_existence(temp_dict)
        except KeyError:
            input("Name must be and comes first")
            command = "dont"
            id_old = 0
            
        if command == "upd":
            self.db[id_old] = temp_dict # add new item to database
        elif command == "leave":
            self.db[id] = temp_dict # add new item to database
        elif command == "dont":
            pass
        return stored
    
    def _import_db(self):
        filename = self._get_user_input(msg="Type in filename(.json)") + ".json"
        #! check if .json is at end
        if exists(filename):
            print("File exists")
            self.filename = filename
            with open(filename) as db_file:
                in_dictionary = json.load(db_file)
            self.db = in_dictionary
            print("Database imported")
            self._logger("Database imported from "+filename)
        else:
            print("file doesnt exists")
        self._wait()
        
    def _print_help(self):
        self._logger("help was asked")
        text = """
        \n
    type in item details: e.g.: name, colour, weight, size, title, brand, made, year, etc...
    print database: [database, db, listhem, list , print]
    delete previous item: [delete, undo]
    exit from program: [exit, end, quit]
    import database from file: [import, imp, load db]
        \n
        """
        print(text)
        self._wait()
        
if __name__ == "__main__":
    dbManager01 = Database("basement_db02.json")#,lang="hun")
    #dbManager01.db = {"0": {"name": "kalap\u00e1cs", "made": "bosch", "material": "wood", "weight": "0.2kg"}, "1": {"name": "asztal", "brand": "ikea", "material": "wood", "size": "2x2x1.3m", "weight": "12kg"}, "2": {"name": "book", "title": "vil\u00e1g k\u00f6r\u00fcl 80 nap alatt", "colour": "white"}, "3": {"name": "sz\u00e1m\u00edt\u00f3g\u00e9p", "brand": "hp", "colour": "black", "size": "0.4x0.5x0.2m", "working": "no"}, "5": {"name": "kisaut\u00f3", "colour": "red", "memory": "true"}}
    dbManager01.menu_loop()
    
    
    
    