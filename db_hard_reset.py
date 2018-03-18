import os
import shutil

info = """
Hard reset of the database.
Deletes:
    > \db.sqlite3
    > \pawpals\__pycache__\*
    > \pawpals\migrations\* except _init_.py
    > \pawpals\migrations\__pycache__\* 
"""

def delete_tree(path):
    try:
        shutil.rmtree(path)
        print("> Deleted: " + path)
    except:
        print(">>> Could not delete: " + path)
        
def reset():
    print("Reseting database...")
    # \db.sqlite3
    try:
        os.remove("db.sqlite3")
        print("> Deleted: db.sqlite3")
    except:
        print(">>> Could not delete: db.sqlite3")
        
    # \pawpals\__pycache__\*
    delete_tree("pawpals\__pycache__")
    
    # \pawpals\migrations\__pycache__\* 
    delete_tree("pawpals\migrations\__pycache__")
    
    # \pawpals\migrations\* except _init_.py
    try:
        all_files = []
        for root, dirs, files in os.walk("pawpals\migrations"):
            for name in files:
                all_files.append(os.path.join(root, name))
        
        to_omit = "pawpals\migrations\__init__.py"
        
        for file in all_files:
            if not(file == to_omit):
                os.remove(file)
                print("> Deleted migration: " + file)
    except:
        print(">>> Could not delete: migrations")
        
if __name__ == "__main__":
    
    print(info)
    
    proceed = input("Proceed? Y/N ").lower()
    if proceed == "y":
        print()
        reset()        
        print("\nMake migrations, migrate, populate, enjoy.")
        
    