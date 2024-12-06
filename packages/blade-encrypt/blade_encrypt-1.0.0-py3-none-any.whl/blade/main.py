import os
import ctypes
from blade.core import Blade
import fade  # For colorful text
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def print_logo():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    ctypes.windll.kernel32.SetConsoleTitleW("BLADE Encryption Tool | Dev: DARKTRON")

    logo = '''        
                                   ██████╗ ██╗      █████╗ ██████╗ ███████╗
                                   ██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝
                                   ██████╔╝██║     ███████║██║  ██║█████╗  
                                   ██╔══██╗██║     ██╔══██║██║  ██║██╔══╝  
                                   ██████╔╝███████╗██║  ██║██████╔╝███████╗
                                   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝                                 
    '''
    menu = '''
                                         ╔═════════════════════════╗
                                      ╔═══════════════════════════════╗
                                      ║ [1] Encrypt a File            ║  
                                      ║ [2] Decrypt a File            ║
                                      ║ [3] Encrypt a Folder          ║
                                      ║ [4] Decrypt a Folder          ║
                                      ║ [5] Generate a New Key        ║
                                      ╚═══════════════════════════════╝ 
                                                  ║ [X] EXIT ║
                                                  ╚══════════╝                      
    '''
    logo_color = fade.brazil(logo)
    menu_color = fade.brazil(menu)
    print(logo_color)
    print(menu_color)

def colorful_input(prompt, options):
    """Colorful selection input for options"""
    choice = input(f"{Fore.YELLOW}> ").strip()
    
    if choice not in options:
        print(f"{Fore.RED}Invalid choice, please try again.")
        return colorful_input(prompt, options)
    return choice

def main():
    blade = Blade()
    print_logo()
    # print(f"Encryption Key: {blade.key.decode()} (Save this securely!)")

    while True:
        # Menu with colorful options
        options = {
            "1": Fore.CYAN,
            "2": Fore.YELLOW,
            "3": Fore.MAGENTA,
            "4": Fore.GREEN,
            "5": Fore.RED,
            "6": Fore.BLUE,
        }
        
        choice = colorful_input("\nSelect an option", options)
        
        if choice == "1":
            file_path = input("Enter the file path to encrypt: ").strip()
            if os.path.exists(file_path):
                blade.encrypt_file(file_path)
                print(f"{Fore.CYAN}File encrypted: {file_path}.BLADE-777")
            else:
                print(f"{Fore.RED}File not found.")

        elif choice == "2":
            file_path = input("Enter the encrypted file path to decrypt: ").strip()
            if os.path.exists(file_path):
                blade.decrypt_file(file_path)
                print(f"{Fore.YELLOW}File decrypted: {file_path.replace('.BLADE-777', '')}")
            else:
                print(f"{Fore.RED}Encrypted file not found.")

        elif choice == "3":
            folder_path = input("Enter the folder path to encrypt: ").strip()
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                blade.encrypt_folder(folder_path)
                print(f"{Fore.MAGENTA}Folder encrypted: {folder_path}.zip.BLADE-777")
            else:
                print(f"{Fore.RED}Folder not found.")

        elif choice == "4":
            encrypted_zip = input("Enter the encrypted zip file path: ").strip()
            output_folder = input("Enter the output folder path: ").strip()
            if os.path.exists(encrypted_zip):
                blade.decrypt_folder(encrypted_zip, output_folder)
                print(f"{Fore.GREEN}Folder decrypted to: {output_folder}")
            else:
                print(f"{Fore.RED}Encrypted zip file not found.")

        elif choice == "5":
            blade = Blade()  # Generate a new key
            print(f"{Fore.RED}New Encryption Key: {blade.key.decode()} (Save this securely!)")

        elif choice == "X":
            print(f"{Fore.BLUE}Exiting BLADE. Goodbye!")
            break

        else:
            print(f"{Fore.RED}Invalid option. Please try again.")

if __name__ == "__main__":
    main()
