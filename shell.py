import sys
import os
import subprocess

def main():

    bultin_commands = ["echo", "type", "exit", "pwd", "cd"]
    
    # Custom PATH env variable
    paths = os.getenv("PATH").split(":")
    
    # REPL (read–eval–print loop)
    while True:
        try:
            
            sys.stdout.write("$ ")
            sys.stdout.flush()

            # Wait for user input
            args = input().split(" ")
            command = args[0]
            
            # Check if it's a builtin command
            if command in bultin_commands:
                # Handles exist command
                if command == "exit":
                    sys.exit()
                
                # Handles echo command
                elif command == "echo":
                    print(" ".join(args[1:]))
                
                # Handles type command
                elif command == "type":
                    # Check if the command is a shell builtin
                    if args[1] in bultin_commands:
                        print(f"{args[1]} is a shell builtin")
                    else:
                        found = False
                        # Search for the command in the PATH env variable
                        for path in paths:
                            command_path = os.path.join(path, args[1])
                            if os.path.exists(command_path):
                                print(f"{args[1]} is {command_path}")
                                found = True
                                break 

                        if not found:
                            print(f"{args[1]} not found")
                            
                # Print current directory
                elif command == "pwd":
                    print(os.getcwd())
                
                # Change directory
                elif command == "cd":
                    # Absolute and relative paths
                    if os.path.exists(args[1]):
                        os.chdir(args[1])
                    # User home directory specified by ~ character
                    # User home directory is present inside HOME env variable
                    elif args[1] == "~":
                        user_dir = os.getenv("HOME")
                        os.chdir(user_dir)
                    else:
                        print(f"{args[1]}: No such file or directory")
                         
            # Check if it's an external program - given as absolute paths
            elif os.path.exists(command):
                out = subprocess.run(
                    args=args, 
                    capture_output=True
                    )
                # output in bytes, decode
                out_decoded = out.stdout.decode()
                print(out_decoded, end="")
            
            # Handles invalid commands
            else:
                print(f"{command}: command not found")     
                    
        except (Exception, EOFError, OSError) as e:
            print("\nExiting the program.")
            break  # Exit the loop
        
if __name__ == "__main__":
    main()
