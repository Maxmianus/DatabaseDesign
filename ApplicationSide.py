import MySQLdb
import datetime
from datetime import timedelta 

############################    Global variables    ###############################################
Reader_id = "empty"

##############################      DB connection   ################################################
db = MySQLdb.connect("localhost","chris","2765593cD","LibraryTables")  #replace username with your localhost username, password with password, and databaseName with the name of a database

cursor = db.cursor()

#testing connection
cursor.execute("SELECT VERSION()")
info = cursor.fetchone()
print ("Database Version : %s " % info)

###############################     Queries     ###################################################

def printAll():
    sql = "SELECT * FROM BOOKS WHERE quantity > 0"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("List of Books:")
       print("| title | author | isbn | published date | quantity |")
       for row in results:
          title  = row[0]
          author = row[1]
          isbn = int(row[2])
          date = int(row[3])
          quantity = int(row[5])
          # Now print fetched result
          print(title, author, isbn, date, quantity)
    except:
       print ("Error: unable to fecth data")
           
def printTitle():
    titleInput = raw_input("Enter the book's title: ")
    
    sql = "SELECT * FROM BOOKS WHERE quantity > 0 AND title='" + titleInput + "'"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("List of Books:")
       print("| title | author | isbn | published date | quantity |")
       for row in results:
          title  = row[0]
          author = row[1]
          isbn = int(row[2])
          date = int(row[3])
          quantity = int(row[5])
          # Now print fetched result
          print(title, author, isbn, date, quantity)
    except:
       print ("Error: unable to fecth data")
   
def printAuthor():
    authorInput = raw_input("Enter the book's title: ")
    
    sql = "SELECT * FROM BOOKS WHERE quantity > 0 AND author='" + authorInput + "'"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("List of Books:")
       print("| title | author | isbn | published date | quantity |")
       for row in results:
          title  = row[0]
          author = row[1]
          isbn = int(row[2])
          date = int(row[3])
          quantity = int(row[5])
          # Now print fetched result
          print(title, author, isbn, date, quantity)
    except:
       print ("Error: unable to fecth data")

def printOwners():
    sql = "SELECT * FROM OWNERS"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("List of Stores:")
       print("| Name | ID |")
       for row in results:
          name  = row[0]
          store_id = int(row[1])
          # Now print fetched result
          print(name, store_id)
    except:
       print ("Error: unable to fecth data")
       
def printStoreBooks():
    storeInput = raw_input("Enter the store's id: ")
    
    sql = "SELECT * FROM BOOKS WHERE quantity > 0 AND book_location_id='" + storeInput + "'"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("List of Books:")
       print("| title | author | isbn | published date | quantity |")
       for row in results:
          title  = row[0]
          author = row[1]
          isbn = int(row[2])
          date = int(row[3])
          quantity = int(row[5])
          # Now print fetched result
          print(title, author, isbn, date, quantity)
    except:
       print ("Error: unable to fecth data")

#working on       
def loginReader(username, password):
    sql = "SELECT username, r_id FROM READERS WHERE username ='" + username + "' AND password='" + password + "'"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchone()
       if(results == None):
          print("invalid login")
          closeClient()
       else:
          Reader_id = results[1]
          return results[0]

    except:
       print ("Error: unable to fecth data")
       
def CheckoutBook():
    isbn = raw_input("Enter the book's isbn: ")
    sql = "UPDATE BOOKS B SET B.quantity = B.quantity - 1 WHERE B.isbn = " + isbn + " AND B.quantity > 0"
    sql2 = "SELECT isbn, book_location_id FROM BOOKS A WHERE A.isbn = isbn AND A.quantity > 0"
    sql3 = "INSERT INTO LOANER(r_id, l_id, b_id, return_date, checkout_date) VALUES (%s, %s, %s, %s, %s)"
    
    try:
       # Execute the SQL command
       cursor.execute(sql)
       db.commit()
       
       cursor.execute(sql2)
       results = cursor.fetchone()
       if(results == None):
          print("invalid login")
          closeClient()
       else:
          Reader_id = results[1]
          val = (Reader_id, results[1], results[0], setCheckoutDate(), setReturnDate())
          cursor.execute(sql3, val)
          db.commit()
       # Fetch all the rows in a list of lists.
       #results = cursor.fetchone()

    except:
       print ("Error: unable to fecth data")

def ReturnBook():
    print("nothing now..")
    
        
def createReaderAccount():
    fname = raw_input("Enter first name: ")
    lname = raw_input("Enter last name: ")
    phone_number = raw_input("Enter phone number: ")
    email = raw_input("Enter email: ")
    username = raw_input("Enter username: ")
    password = raw_input("Enter password: ")
    
    sql = "INSERT INTO READERS(fname, lname, phone_number, email, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (fname, lname, phone_number, email, username, password)
    
    try:
       # Execute the SQL command
          cursor.execute(sql, val)
          db.commit()
       # Fetch all the rows in a list of lists.
       #results = cursor.fetchone()

    except:
       print ("Error: unable to fecth data")
    
###############################     Main Menu       ###############################################
def MenuOne():
    print("\n\n\n")
    print("*******************************************************************************************")
    print("*                        The Amazing Library System Main Menu                             *")
    print("*******************************************************************************************")
    print("1. Search for Book")
    print("2. Search by Store")
    print("3. Exit")

#switch statement for selecting which option to run
def switch(num):
    switched = {
        1: lambda : OptionOne(),
        2: lambda : OptionTwo(),
        3: lambda : closeClient(),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()

#Closes database connection and exits
def closeClient():
    db.close()
    print("Closing...")
    exit()
    
#################################   Logged In Menu      #########################################################
def Logged_In_Menu(cUser):
    print("\n\n\n")
    print("*******************************************************************************************")
    print("*                        The Amazing Library System Main Menu                             *")
    print("*******************************************************************************************")
    print("1. Search for Book")
    print("2. Search by Store")
    print("3. Currently Logged in as: " + cUser)
    print("4. Exit")
    print("5. Checkout Book")
    
    choice = input("Enter the number of the choice you want: ")
    switchLoggedIn(choice)

    
#switch statement for selecting which option to run
def switchLoggedIn(num):
    switched = {
        1: lambda : OptionOne(),
        2: lambda : OptionTwo(),
        4: lambda : closeClient(),
        5: lambda : CheckoutBook(),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()

#Closes database connection and exits
def closeClient():
    db.close()
    print("Closing...")
    exit()
    
    
##################################################   Option One   ###############################################
def OptionOne():
    print("\n\n\n")
    print("*******************************************************************************************")
    print("*                 The Amazing Library System Book Search Menu                             *")
    print("*******************************************************************************************")
    print("1. Show all books")
    print("2. Search by title")
    print("3. Search by Author")
    
    choice = input("Enter the number of the choice you want: ")
    switchOne(choice)
    raw_input("Press enter to continue")

#switch statement for book searching
def switchOne(num):
    switched = {
        1: lambda : printAll(),
        2: lambda : printTitle(),
        3: lambda : printAuthor(),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()
###################################################   Option Two   ########################################
def OptionTwo():
    print("\n\n\n")
    print("*******************************************************************************************")
    print("*                 The Amazing Library System Store Search Menu                            *")
    print("*******************************************************************************************")
    print("1. Show all stores")
    print("2. Show Books at specific store")

    choice = input("Enter the number of the choice you want: ")
    switchTwo(choice)
    raw_input("Press enter to continue")

#switch statement for book searching
def switchTwo(num):
    switched = {
        1: lambda : printOwners(),
        2: lambda : printStoreBooks(),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()
###################################################     Other Options   #########################################
def CreateAccount():
    print("Nothing so far")

def Login():
    print("Nothing right now")
    
#Login menu to see if the user is anonymous, a reader, or an owner
def UserType():
    print("*******************************************************************************************")
    print("*                        The Amazing Library System Login Menu                            *")
    print("*******************************************************************************************")
    print("1. Log in as a Reader")
    print("2. Log in as a Owner")
    print("3. Veiw anonymously")
    print("4. Create Reader account")   #Only allowing reader accounts to be publicly made
    
    choice = input("Enter the number of the choice you want: ")
    return(choice)

#################################################   Date Functions  ##############################################
def setCheckoutDate():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y")

def setReturnDate():
    now = datetime.datetime.now()
    returnDate = timedelta(days=14) #return date is 14 days
    newDate = (now + returnDate)
    return newDate.strftime("%d-%m-%Y")
    
###################################################     Client side   ###########################################
#switch statement for menus, unsure will use
def switchMain(num):
    switched = {
        1: lambda : MenuOne(),
        2: lambda : Logged_In_Menu(),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()   
    
#Let user choose login
userChoice = UserType()

#For readers and anonymous users, owners will get a different menu once logged in
if(userChoice == 3):
    while(1):
        MenuOne()
        choice = input("Enter the number of the choice you want: ")
        switch(choice)
elif(userChoice == 1):
    username = raw_input("Enter username: ")
    password = raw_input("Enter password: ")
    currentUser = loginReader(username, password)
    if(currentUser == None):
        closeClient()
    else:
        while(1):
            Logged_In_Menu(currentUser)
elif(userChoice == 4):
    createReaderAccount()
    closeClient()    
else:
    closeClient()
    
