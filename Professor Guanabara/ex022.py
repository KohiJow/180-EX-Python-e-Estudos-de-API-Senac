#Create a program who read the complete name of someone and show:
#Name with all your letter in capital
#Name with all your letter in lower case
#How many letters at all (without consider spaces)
#How many letters have the first name

Name = str(input('Insert your name: ')) #Ask's whats is your name to proceed
NoSpace = Name.replace(' ', '') #Replace spaces with nothing :D
NameD = Name.split() #Divide the string, kit kat?
print(Name.upper()) #Scream your name, rude.
print(Name.lower()) #whispers in your ear, naughty.
print(len(NoSpace)) #tell how many letters your name has without counting your existential void
print(len(NameD[0])) #divide the string, Portgas D.Ace
