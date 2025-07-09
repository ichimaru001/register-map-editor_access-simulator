# TITLE   :     MEMORY-MAPPED REGISTER MAP EDITOR AND ACCESS SIMULATOR
# AUTHOR  :     ichimaru001
# DATE    :     05/07/25

import re # regex 

print("Hello, World!\nWelcome to the memory-mapped register-map editor and access simulator!\n")

registerTable: dict[str, dict[str, str]] = {}
userChoice: int = -1

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
    with open("./register-map.txt", "r") as file:
      headerLine: str = file.readline()
      headerKeys: list[str] = headerLine.split() # line split into elements
      headerKeys = [key.lower() for key in headerKeys] # elements are converted into lowercase
      for line in file:
        contentsLine: list[str] = line.split()
        # parsing of description of register
        lengthOfRegister: int = 4
        # ! "desc" is short for "description"
        descRegister: list[str] = []
        descRegister = contentsLine[lengthOfRegister - 1:]
        descString: str = ' '.join(word for word in descRegister)
        contentsLine[lengthOfRegister - 1] = descString
        contentsLine = contentsLine[:lengthOfRegister]
        
        registerTable[contentsLine[0]] = {
          headerKeys[i+2]:contentsLine[i+1]
          for i in range(lengthOfRegister - 1)
        }
      print(registerTable)
  if userChoice == 2:
    print("\n** REGISTER TABLE **")
    print(f"{'# ADDR':<7} {'NAME':<10} {'VALUE':<7} {'DESCRIPTION':<20}")
    for registerAddress, registerItems in registerTable.items():
      registerName: str = registerItems["name"]
      registerValue: str = registerItems["value"]
      registerDesc: str = registerItems["description"]
      print(f"{registerAddress:<7} {registerName:<10} {registerValue:<7} {registerDesc:<20}")
    print("\n")
  if userChoice == 3:
    userRegisterAddress: str = "" 
    userRegisterAddress = input("Enter register address to read: ")
    userRegisterAddress = userRegisterAddress.strip()
    # print(userRegisterAddress)
    print("\n")
    if userRegisterAddress in registerTable:
      register: dict[str, str] = registerTable[userRegisterAddress]
      # print(f"{register}")
      for registerKey, registerValue in register.items():
        print(f"{registerKey.capitalize():<12} : {registerValue}")
    else:
      print("No register found!")
    print("\n")
  if userChoice == 4:
    userRegisterAddress: str = "" 
    userRegisterAddress = input("Enter register address to write to: ")
    userRegisterAddress = userRegisterAddress.strip()
    print("\n")
    if userRegisterAddress in registerTable:
      userRegisterValue: str = ""
      register: dict[str, str] = registerTable[userRegisterAddress]
      errorFlag: int = 1
      while errorFlag:
        userRegisterValue = input("Enter a new value for this register (e.g. 0x3251): ")
        # check format
        checkRegisterValue = userRegisterValue.strip()
        regexPattern = r"0x[0-9A-Fa-f]{4}"
        # if (checkRegisterValue[0] != '0' and checkRegisterValue[1] != 'x') or (len(checkRegisterValue) != 6):
        if re.fullmatch(regexPattern,checkRegisterValue):
          errorFlag = 0
        else:
          print("error occurred!")
          errorFlag = 1
      register.update({"value":userRegisterValue})
    else:
      print("No register found!")
    print("\n")
  if userChoice == 5:
    userDescSearch: str = "" # user search by phrase or keyword
    userDescSearch = input("Enter a search term: ")
    userDescSearch = userDescSearch.strip().lower()
    matchingRegisters: dict[str, dict[str, str]] = {}
    for key, values in registerTable.items():
      if userDescSearch in values["description"].lower():
        matchingRegisters[key] = values
        # print("Found a register!")
    if len(matchingRegisters) > 0:
      print(f"\nFound {len(matchingRegisters)} register(s)")
      print("\n** REGISTERS FOUND **")
      print(f"{'# ADDR':<7} {'NAME':<10} {'VALUE':<7} {'DESCRIPTION':<20}")
      for registerAddress, registerItems in matchingRegisters.items():
        registerName: str = registerItems["name"]
        registerValue: str = registerItems["value"]
        registerDesc: str = registerItems["description"]
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
        registerName: str = registerItems["name"]
        registerValue: str = registerItems["value"]
        registerDesc: str = registerItems["description"]
        file.writelines(f"{registerAddress:<7} {registerName:<10} {registerValue:<7} {registerDesc:<20}\n")