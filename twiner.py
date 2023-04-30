import cmd
import colorama
from src.network_interface import *


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
   
   
[+] Welcome to Twiner, a evil-twin attack bot.
[clear] Clear the screen.
[quit] Quit the program.
[ifaces] Get list of available network interfaces.
[iface <interface>] Set the network interface to use.
{colorama.Style.RESET_ALL}"""
    prompt = f"{colorama.Fore.BLUE}> {colorama.Style.RESET_ALL}"

    def do_clear(self, arg=None):
        print(self.intro)
    
    def do_quit(self, arg=None):
        print(f"{colorama.Fore.RED}Quitting...{colorama.Style.RESET_ALL}")
        return True
    
    def do_ifaces(self, arg=None):
        network_interfaces: List[NetworkInterface] = get_wifi_interfaces()
        for interface in network_interfaces:
            print(f"{colorama.Fore.GREEN}{interface.to_string()}", end="\n\n")

    def do_iface(self, arg=None):
        if arg is None:
            print(f"{colorama.Fore.RED}Please specify an interface.{colorama.Style.RESET_ALL}")
            return
        
   
if __name__ == '__main__':
    TwinerCmd().cmdloop()
