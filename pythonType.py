def add(firstName: str | list, lastName:str):
    a=firstName.capitalize()
    b=lastName.capitalize()
    return a+" "+b

fname="bill"
lname ="ate"

name=add(fname,lname)
print(name)