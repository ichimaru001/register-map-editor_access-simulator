# TITLE   :     MEMORY-MAPPED REGISTER MAP EDITOR AND ACCESS SIMULATOR
# AUTHOR  :     ichimaru001
# DATE    :     05/07/25

print("Hello, World!\nWelcome to the memory-mapped register-map editor and access simulator!\n")

registerTable = {}
userChoice:int = -1

while userChoice != 8:
  print("*** MEMORY-MAPPED REGISTER-MAP EDITOR AND ACCESS SIMULATOR ***")
  print("   1. Load register map file")
  print("   2. View register table")
  print("   3. Read Register value")
  print("   4. Write register value")
  print("   5. Search registers by description")
  print("   6. Reset all registers")
  print("   7. Save register map to file")
  print("   8. Exit")
  userChoice = int(input("Enter your choice (1-8): "))
  if userChoice == 1:
    # stuff = []
    with open("./register-map.txt", "r") as file:
      headerLine = file.readline()
      headerKeys = headerLine.split() # line split into elements
      headerKeys = [key.lower() for key in headerKeys] # elements are converted into lowercase
      for line in file:
        stuffInside = line.split()
        # parsing of description of register
        lengthOfRegister = 4
        # ! "desc" is short for "description"
        descRegister = []
        descRegister = stuffInside[lengthOfRegister - 1:]
        descString = ' '.join(word for word in descRegister)
        stuffInside[lengthOfRegister - 1] = descString
        stuffInside = stuffInside[:lengthOfRegister]
        # print(stuffInside)
        # print(f"This is the description of a register: {descString}")
        # registerTable[stuffInside[0]] = {
        #   headerKeys[2]:stuffInside[1],
        #   headerKeys[3]:stuffInside[2],
        #   headerKeys[4]:stuffInside[3]
        # }
        registerTable[stuffInside[0]] = {
          headerKeys[i+2]:stuffInside[i+1]
          for i in range(lengthOfRegister - 1)
        }
        # stuff.append(stuffInside)
      # print(stuff)
      # print(headerKeys)
      print(registerTable)
  if userChoice == 2:
    print("\n** REGISTER TABLE **")
    print(f"{'# ADDR':<7} {'NAME':<10} {'VALUE':<7} {'DESCRIPTION':<20}")
    for registerAddress, registerItems in registerTable.items():
      registerName = registerItems["name"]
      registerValue = registerItems["value"]
      registerDesc = registerItems["description"]
      print(f"{registerAddress:<7} {registerName:<10} {registerValue:<7} {registerDesc:<20}")
    print("\n")
  if userChoice == 3:
    userRegisterAddress = -1 
    userRegisterAddress = input("Enter register address to read: ")
    userRegisterAddress = userRegisterAddress.strip()
    # print(userRegisterAddress)
    print("\n")
    if userRegisterAddress in registerTable:
      register = registerTable[userRegisterAddress]
      # print(f"{register}")
      for key, value in register.items():
        print(f"{key.capitalize():<12} : {value}")
    else:
      print("No register found!")
    print("\n")
  if userChoice == 4:
    userRegisterAddress = -1 
    userRegisterAddress = input("Enter register address to write to: ")
    userRegisterAddress = userRegisterAddress.strip()
    print("\n")
    if userRegisterAddress in registerTable:
      userRegisterValue = -1
      register = registerTable[userRegisterAddress]
      errorFlag = 1
      while errorFlag:
        userRegisterValue = input("Enter a new value for this register (e.g. 0x3251): ")
        # check format
        checkRegisterValue = list(userRegisterValue.strip())
        if (checkRegisterValue[0] != '0' and checkRegisterValue[1] != 'x') or (len(checkRegisterValue) != 6):
          print("error occurred!")
          errorFlag = 1
        else:
          errorFlag = 0
      register.update({"value":userRegisterValue})
    else:
      print("No register found!")
    print("\n")
  if userChoice == 5:
    userDescSearch = "" # user search by phrase or keyword
    userDescSearch = input("Enter a search term: ")
    userDescSearch = userDescSearch.strip()
    matchingRegisters = {}
    for key, values in registerTable.items():
      descRegisterArray = values["description"].split()
      descRegisterArray = [term.lower() for term in descRegisterArray]
      print(f"This is the descRegisterArray: {descRegisterArray}")
      if userDescSearch in descRegisterArray:
        matchingRegisters[key] = values
        # print("Found a register!")
    if len(matchingRegisters) > 0:
      print(f"\nFound {len(matchingRegisters)} register(s)")
      print("\n** REGISTERS FOUND **")
      print(f"{'# ADDR':<7} {'NAME':<10} {'VALUE':<7} {'DESCRIPTION':<20}")
      for registerAddress, registerItems in matchingRegisters.items():
        registerName = registerItems["name"]
        registerValue = registerItems["value"]
        registerDesc = registerItems["description"]
        print(f"{registerAddress:<7} {registerName:<10} {registerValue:<7} {registerDesc:<20}")
      print("\n")
    else:
      print(f"No registers found with description containing {userDescSearch}.")
  if userChoice == 6:
    # reset all registers -> reset all values of registers to 0x0000
    for key, values in registerTable.items():
      registerTable[key].update({"value":"0x0000"})
    print("All registers have their value changed to 0x0000!")
  if userChoice == 7:
    # save register table to file
    with open("./register-map.txt", "w") as file:
      file.writelines(f"{'# ADDR':<7} {'NAME':<10} {'VALUE':<7} {'DESCRIPTION':<20}\n")
      for registerAddress, registerItems in registerTable.items():
        registerName = registerItems["name"]
        registerValue = registerItems["value"]
        registerDesc = registerItems["description"]
        file.writelines(f"{registerAddress:<7} {registerName:<10} {registerValue:<7} {registerDesc:<20}\n")