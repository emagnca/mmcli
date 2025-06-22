import cmd2
import json
from mmcli.mmclient import MMClient
import pprint

mmclient = MMClient('http://localhost:3001', 'http://localhost:3008')

class MMAdmin(cmd2.Cmd):
    """
    Admin CLI for managing resources via REST API.
    """
    def do_create_field(self, line):
        """Interactively create a new field by entering all attributes."""
        print("Enter the attributes for the new field. Leave blank to skip an attribute.")
        customer = input('customer: ')
        name = input('name: ')
        displayname = input('displayname: ')
        displayname_sv = input('displayname_sv: ')
        type_ = input('type: ')
        placeholder = input('placeholder: ')
        order_input = input('order (integer): ')
        try:
            order = int(order_input) if order_input else None
        except ValueError:
            print('Invalid order, setting to None.')
            order = None
        format_ = input('format (regex): ')
        
        def ask_bool(prompt):
            val = input(f'{prompt} (y/n): ')
            return val.lower() in ['y', 'yes', 'true', '1'] if val else False

        search = ask_bool('search')
        index = ask_bool('index')
        update = ask_bool('update')
        general = ask_bool('general')
        mandatory = ask_bool('mandatory')

        data = {}
        if customer: data['customer'] = customer
        if name: data['name'] = name
        if displayname: data['displayname'] = displayname
        if displayname_sv: data['displayname_sv'] = displayname_sv
        if type_: data['type'] = type_
        if placeholder: data['placeholder'] = placeholder
        if order is not None: data['order'] = order
        if format_: data['format'] = format_
        data['search'] = search
        data['index'] = index
        data['update'] = update
        data['general'] = general
        data['mandatory'] = mandatory

        pprint.pprint(data)
        confirm = input('Proceed? (y/n): ')
        if confirm.lower() not in ['y', 'yes']:
            print('Cancelled.')
            return
        rsp = mmclient.admin_create('field', data)
        try:
            pprint.pprint(rsp.json())
        except Exception:
            print(rsp.text)

    def do_create(self, line):
        """Create a new admin resource. Usage: create <resource> <json_data>"""
        try:
            parts = line.split(' ', 1)
            if len(parts) < 2:
                print('Usage: create <resource> <json_data>')
                return
            resource, data_str = parts
            data = json.loads(data_str)
            rsp = mmclient.admin_create(resource, data)
            pprint.pprint(rsp.json())
        except Exception as e:
            print(f'Error: {e}')

    def do_read(self, line):
        """Read an admin resource. Usage: read <resource> [id]"""
        parts = line.split()
        if not parts:
            print('Usage: read <resource> [id]')
            return
        resource = parts[0]
        id = parts[1] if len(parts) > 1 else None
        rsp = mmclient.admin_read(resource, id)
        pprint.pprint(rsp.json())

    def do_update(self, line):
        """Update an admin resource. Usage: update <resource> <id> <json_data>"""
        try:
            parts = line.split(' ', 2)
            if len(parts) < 3:
                print('Usage: update <resource> <id> <json_data>')
                return
            resource, id, data_str = parts
            data = json.loads(data_str)
            rsp = mmclient.admin_update(resource, id, data)
            pprint.pprint(rsp.json())
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
        try:
            pprint.pprint(rsp.json())
        except Exception:
            print(rsp.text)

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
