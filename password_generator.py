import random as rd

#usable characters
characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!"#$%&/()=*~^[]{}'

print('Welcome to the password generator program!')

while True:
    password_len = input('Enter desire password length: ')
    try:
        password_len = int(password_len)
        password_number = input('Enter desire number of passwords: ')
        try:
            password_number = int(password_number)
            for i in range(password_number):
                password = ''
                for x in range(password_len):
                    password_string = rd.choice(characters)
                    password = password + password_string
                print('Here is your password: ', password)
            answer = input('Are you satisfied with the password given? (Y/N) ')
            if answer.lower() == 'no' or answer.lower() =='n':
                continue
            else: 
                break
        except:
            print('Please type a number!')
    except:
        print('Please type a number!')
        
    
