import MySQLdb
import datetime
from datetime import timedelta 

############################    Global variables    ##############################################
Current_id = "empty"

##############################      DB connection   ################################################
db = MySQLdb.connect("localhost","username","password","databaseName")  #replace username with your localhost username, password with password, and databaseName with the name of a database

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
          return results

    except:
       print ("Error: unable to fecth data")

def loginOwner(username, password):
    sql = "SELECT username, l_id FROM OWNERS WHERE username ='" + username + "' AND password='" + password + "'"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchone()
       if(results == None):
          print("invalid login")
          closeClient()
       else:
          return results

    except:
       print ("Error: unable to fecth data")
       
def CheckoutBook(r_id):
    isbn = raw_input("Enter the book's isbn: ")
    sql = "UPDATE BOOKS B SET B.quantity = B.quantity - 1 WHERE B.isbn = " + isbn + " AND B.quantity > 0"
    sql2 = "SELECT isbn, book_location_id FROM BOOKS A WHERE A.isbn =" + isbn  + " AND A.quantity > 0"
    sql3 = "INSERT INTO LOANER(r_id, l_id, b_id, return_date, checkout_date) VALUES (%s, %s, %s, %s, %s)"
    
    try:
       # Execute the SQL command
       cursor.execute(sql)
       #db.commit()
       
       cursor.execute(sql2)
       results = cursor.fetchone()
       if(results == None):
          print("invalid login")
          closeClient()
       else:
          #Current_id = results[1]
          val = (r_id, results[1], results[0], setCheckoutDate(), setReturnDate())
          cursor.execute(sql3, val)
          db.commit()
       # Fetch all the rows in a list of lists.
       #results = cursor.fetchone()

    except:
       print ("Error: unable to fecth data")

def ReturnBook(l_id):
    r_id = raw_input("Enter the Reader's id: ")
    isbn = raw_input("Enter the Book's id: ")
    
    sql = "DELETE FROM LOANER WHERE r_id=" + str(r_id) + " AND b_id =" + str(isbn) + " AND l_id=" + str(l_id) 
    sql1 = "UPDATE BOOKS B SET B.quantity = B.quantity + 1 WHERE B.isbn = " + str(isbn)
    try:
       # Execute the SQL command
       cursor.execute(sql)
       #db.commit()
       
       cursor.execute(sql1)
       results = cursor.fetchone()
       db.commit()
       # Fetch all the rows in a list of lists.
       #results = cursor.fetchone()

    except:
       print ("Error: unable to fecth data")
       
def AddBook(l_id):
    title = raw_input("Enter book title: ")
    author = raw_input("Enter book author: ")
    published_date = raw_input("Enter published_date: ")
    quantity = raw_input("Enter quantity: ")
    
    sql = "INSERT INTO BOOKS(title, author, published_date, book_location_id, quantity) VALUES (%s, %s, %s, %s, %s)"
    val = (title, author, published_date, l_id, quantity)
    
    try:
       # Execute the SQL command
       cursor.execute(sql, val)
       db.commit()

    except:
       print ("Error: unable to fecth data")

def ShowInventory(l_id):
    sql = "SELECT * FROM BOOKS WHERE book_location_id= " + str(l_id)
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("Inventory:")
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
       
def currentCheckedOut(l_id):
    sql = "SELECT * FROM LOANER WHERE l_id =" + str(l_id)
    
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("| Reader ID | Book ID | Checkout Date | Return Date |")
       for row in results:
          r_id = row[0]
          b_id = row[2]
          checkout = row[3]
          returnD = row[4]
          
          # Now print fetched result
          print(int(r_id), int(b_id), checkout, returnD)
    except:
       print ("Error: unable to fecth data")
    
def BooksCheckedOutReader(r_id):
    sql = "SELECT * FROM LOANER WHERE r_id =" + str(r_id)
    
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       print("| Reader ID | Book ID | Checkout Date | Return Date |")
       for row in results:
          r_id = row[0]
          b_id = row[2]
          checkout = row[3]
          returnD = row[4]
          
          # Now print fetched result
          print(int(r_id), int(b_id), checkout, returnD)
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
def Logged_In_Menu(cUser, r_id):
    print("\n\n\n")
    print("*******************************************************************************************")
    print("*                        The Amazing Library System Main Menu                             *")
    print("*******************************************************************************************")
    print("1. Search for Book")
    print("2. Search by Store")
    print("3. Currently Logged in as: " + cUser)
    print("4. Exit")
    print("5. Checkout Book")
    print("6. Show Checked out Books")
    
    choice = input("Enter the number of the choice you want: ")
    switchLoggedIn(choice, r_id)

    
#switch statement for selecting which option to run
def switchLoggedIn(num, r_id):
    switched = {
        1: lambda : OptionOne(),
        2: lambda : OptionTwo(),
        4: lambda : closeClient(),
        5: lambda : CheckoutBook(r_id),
        6: lambda : BooksCheckedOutReader(r_id),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()

##################################################  Close Database  ##############################################
#Closes database connection and exits
def closeClient():
    db.close()
    print("Closing...")
    exit()
    
###############################################     Owner Menu  #################################################

def Owner_Menu(cUser, l_id):
    print("\n\n\n")
    print("*******************************************************************************************")
    print("*                        The Amazing Library System Owner Menu                            *")
    print("*******************************************************************************************")
    print("1. Show Inventory")
    print("2. Currently Logged in as: " + cUser)
    print("3. Exit")
    print("4. Return Book")
    print("5. Add Book")
    print("6. Books Currently Checked Out")
    
    choice = input("Enter the number of the choice you want: ")
    switchOwner(choice, l_id)

    
#switch statement for selecting which option to run
def switchOwner(num, l_id):
    switched = {
        1: lambda : ShowInventory(l_id),
        3: lambda : closeClient(),
        4: lambda : ReturnBook(l_id),
        5: lambda : AddBook(l_id),
        6: lambda : currentCheckedOut(l_id),
    }
    func = switched.get(num, lambda :'Invalid')
    return func()
    
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
###################################################     First Menu   #########################################
    
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
    

#################################################  Set Date Functions  ##############################################
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
    if(currentUser[0] == None):
        closeClient()
    else:
        while(1):
            Logged_In_Menu(currentUser[0], currentUser[1])
elif(userChoice == 4):
    createReaderAccount()
    closeClient()  
elif(userChoice == 2):
    username = raw_input("Enter username: ")
    password = raw_input("Enter password: ")
    currentUser = loginOwner(username, password)
    if(currentUser[0] == None):
        closeClient()
    else:
        while(1):
            Owner_Menu(currentUser[0], currentUser[1])
else:
    closeClient()
    
