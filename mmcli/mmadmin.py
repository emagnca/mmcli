import cmd2
import json
from mmcli.mmclient import MMClient
import pprint

mmclient = MMClient('http://localhost:3001', 'http://localhost:3008')

class MMAdmin(cmd2.Cmd):
    """
    Admin CLI for managing resources via REST API.
    """
    def do_create(self, line):
        """Create a new admin resource. Usage: create <resource> <json_file_path>"""
        import os
        try:
            parts = line.split(' ', 1)
            if len(parts) < 2:
                print('Usage: create <resource> <json_file_path>')
                return
            resource, file_path = parts
            file_path = file_path.strip()
            if not os.path.isfile(file_path):
                print(f'File not found: {file_path}')
                return
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            rsp = mmclient.admin_create(resource, data)
            print(f'Status: {rsp.status_code}')
        except Exception as e:
            print(f'Error: {e}')


    def do_read(self, line):
        """Read an admin resource. Usage: read <resource> [name]"""
        parts = line.split()
        if not parts:
            print('Usage: read <resource> [name]')
            return
        resource = parts[0]
        name = parts[1] if len(parts) > 1 else None
        rsp = mmclient.admin_read(resource, name)
        pprint.pprint(rsp.json())

    def do_update(self, line):
        """Update an admin resource. Usage: update <resource> <id> <json_file_path>"""
        import os
        try:
            parts = line.split(' ', 2)
            if len(parts) < 3:
                print('Usage: update <resource> <id> <json_file_path>')
                return
            resource, id, file_path = parts
            file_path = file_path.strip()
            if not os.path.isfile(file_path):
                print(f'File not found: {file_path}')
                return
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            rsp = mmclient.admin_update(resource, id, data)
            print(f'Status: {rsp.status_code}')
        except Exception as e:
            print(f'Error: {e}')


    def do_delete(self, line):
        """Delete an admin resource. Usage: delete <resource> <id>"""
        parts = line.split()
        if len(parts) < 2:
            print('Usage: delete <resource> <id>')
            return
        resource, id = parts
        rsp = mmclient.admin_delete(resource, id)
        print(f'Status: {rsp.status_code}')

    def do_exit(self, line):
        """Exit the admin CLI."""
        return True

    def do_login(self, line):
        """Authenticate user via bankid, freja, apikey, or user-password."""
        import getpass
        tried_login = False
        success = False
        while (not tried_login):
            type = input('bankid|freja|apikey|user-password: ')
            tried_login = type in 'bfau'
            if (type.startswith('b')):
                ssn = input('     Ssn: ')
                success = mmclient.login_bankid(ssn)
            elif (type.startswith('f')):
                ssn = input('     Email: ')
                success = mmclient.login_freja(ssn)
            elif (type.startswith('a')):
                email = input('     Email: ')
                key = input('    Apikey: ')
                success = mmclient.login_apikey(email, key)
            elif (type.startswith('u')):
                user = input('   Email: ')
                pwd = getpass.getpass('Password: ')
                code = input('    Code: ')
                success = mmclient.login_usrpwd(user, pwd, code)
        if success: print('Login succeded')
        else: print('Login failed')

    def do_quit(self, line):
        """Exit the admin CLI."""
        return True



def run():
    MMAdmin().cmdloop()

if __name__ == '__main__':
    MMAdmin().cmdloop()
