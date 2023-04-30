import cmd
import colorama
from src.network_interface import get_wifi_interfaces


colorama.init()

class TwinerCmd(cmd.Cmd):
    intro = f"""{colorama.Fore.GREEN}
__________       _____________     __________________
\__   __/|\     /|\__   __/( (    /|(  ____ \(  ____ )
   ) (   | )   ( |   ) (   |  \  ( || (    \/| (    )|
   | |   | | _ | |   | |   |   \ | || (__    | (____)|
   | |   | |( )| |   | |   | (\ \) ||  __)   |     __)
   | |   | || || |   | |   | | \   || (      | (\ (   
   | |   | () () |___) (___| )  \  || (____/\| ) \ \__
   )_(   (_______)\_______/|/    )_)(_______/|/   \__/
   
   
[+] Welcome to Twiner, a evil-twin attack tool.
[clear] Clear the screen.
[quit] Quit the program.
[ifaces] Get list of available network interfaces.
{colorama.Style.RESET_ALL}"""
    prompt = f"{colorama.Fore.BLUE}> {colorama.Style.RESET_ALL}"

    def do_clear(self, arg=None):
        print(self.intro)
    
    def do_quit(self, arg=None):
        print(f"{colorama.Fore.RED}Quitting...{colorama.Style.RESET_ALL}")
        return True
    
    def do_ifaces(self, arg=None):
        print(get_wifi_interfaces())


if __name__ == '__main__':
    TwinerCmd().cmdloop()
