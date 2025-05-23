<h2>Command client for MMDok used to store documents and metadata.</h2>
TinyDS is a modern, minimal, simple and scalable DMS that is designed to be able to handle hundreds of millions of documents. 
It can run serverless, in a container or locally with the same code base. MMCli is a command line client to TinyDS. For more info see <a href="https://tinyds.com">TinyDS</a><br><br>
<h2>Getting started with the cli</h2>

With Python3 installed run the following command on the command prompt:

$ <b> python -c "from mmcli import mmcli; mmcli.run()" </b><br><br>

(Cmd) help<br><br>
Commands:<br>
   <table>
   <tr><td><b>audit</b></td><td><i>print audit logs for a document</i></td></tr>
   <tr><td><b>count</b></td><td><i>count documents</i></td></tr>
   <tr><td><b>download</b></td><td><i>download a document to file</i></td></tr>
   <tr><td><b>delete</b></td><td><i>deletes a document</i></td></tr>
   <tr><td><b>login</b></td><td><i>used to log in to the server</i></td></tr>
   <tr><td><b>metadata</b></td><td><i>prints metadata for a document</i></td></tr>
   <tr><td><b>register</b></td><td><i>register a user</i></td></tr>
   <tr><td><b>search</b></td><td><i>search documents</i></td></tr>
   <tr><td><b>server</b></td><td><i>change target server from the default</i></td></tr>
   <tr><td><b>types</b></td><td><i>lists available document types</i></td></tr>
   <tr><td><b>update</b></td><td><i>updates a document's metadata</i></td></tr>
   <tr><td><b>upload</b></td><td><i>upload either a new document or a new version</i></td></tr>
   <tr><td><b>view</b></td><td><i>download and show a document in the webbrowser</i></td></tr>
</table>

For detailed help for a command type: 'help <command>'<br><br>

<h3>Example session</h3>
Note that if you at registration below answer that you don't belong to a group, you will be able to login
and use the system immediately. You will be able to use a set of predefined document types and attributes,
and you will only handle your own documents.<br>
However, if you belong to a group, your group administrator has to give you permissions before you can start.
You will then be able to share documents within the group.
<pre>

$ python3 -c "from mmcli import mmcli; mmcli.run()"

(Cmd) register
   Email:magnus@foo.bar
Password:
Do you belong to a group[Y|N]:Y
<i>
Registration succeded. 
An email will be sent to you for confirmation.
Please ask your group administration to give you permissions.
</i>

(Cmd) login
   Email:magnus@foo.bar
Password:
<i>
 Login succeded
 Group: edok
</i>

(Cmd) types 
<i>{'Faktura': {'_id': '611c18862271d9e4a5dae511',
             'customer': 'edok',
             'fields': {'Fakturanr': {'displayname': 'Invoice number',
                                      'displayname_sv': 'Fakturanummer',
                                      'format': '\\d+',
                                      'general': False,
                                      'index': True,
                                      'mandatory': True,
                                      'name': 'Fakturanr',
                                      'order': 1,
                                      'placeholder': '123456',
                                      'search': True,
                                      'type': 'text',
                                      'update': True,
                                      'values': None}},
             'id': 1,
             'name': 'Faktura',
             'order': 1}}
</i>
(Cmd) search
Filter: {"Fakturanr":123459}
Sort: 
From: 
Number: 
<i>[{'_id': '611c2032d444ac00094333b5',
  'creator': 'gustav@foo.bar',
  'metadata': {'Fakturanr': '123459', 'type': 'Faktura'},
  'ts': '2021-08-17T20:46:42.853Z',
  'type': 'Faktura',
  'updated_by': 'gustav@foo.bar'}]
</i>

(Cmd) metadata
Documentid: 611c2032d444ac00094333b5
<i>{'Fakturanr': '123459', 'type': 'Faktura'}
</i>

(Cmd) count
<i>
{'count': 14}
</i>

(Cmd) audit
Documentid: 611c2032d444ac00094333b5
[{'op': 'create', 'ts': '2021-08-17T20:46:42.853Z', 'user': 'gustav@foo.bar'},
 {'op': 'view', 'ts': '2021-08-17T21:24:33.977Z', 'user': 'gustav@foo.bar'},
 {'op': 'view', 'ts': '2021-08-19T21:27:01.185Z', 'user': 'sture@foo.bar'}]

 (Cmd) upload
Provide a document id if it is a new version, leave empty for new document
Docid: 
Chose document type: Faktura
Metadata: {"Fakturanr":123}
Path to files: /tmp/dummy.pdf
<i>
True
612404f1c0c7380008f019ad
</i>

(Cmd) count
<i>
{'count': 15}
</i>
</pre>

<h3>Permissions</h3>
All commands except register and login need permissions. One can either register as a standalone
user or as belonging to a group. In the first case the user has full permission but only
the documents created by the user. In the latter case permissions have to be set up by a
group administrator.

<h3>Document types</h3>
For standalone users available document types and attributes are a set of standand and common for all.
For group users those are defined in an admin gui. See below. In a future release
admin operations will be available via an api and cli.

<h3>Notifications</h3>
Notifications can be received upon document creation or deletion. For an example this can be look at 
this link: <a href="https://mmdok.se/notification.html">notification client</a>
The client takes the url parameter ?group=<i>group_name</i>, where the <i>group_name</i> is the name of your group. 

<h3>Server side</h3>
The default server is a serverless lambda located on AWS, which also is the default server for this CLI.
However, the client can be set to connect to a server anywhere, for example locally while testing, or 
againt a server running in a Docker container.

<h3>Other clients</h3>
MMDok can be accessed via a REST API. MMCli contains a Python client using this api.<br>
There is a gui client available at <a href="https://mmdok.se/">gui client</a>. The same login will work.

<h3>Administration</h3>
Administrations of documenttypes, users and their permissions can be done via an admin gui (a proper api will come). Two screens
from the gui is show below. Please contact us if you want to create a group.
<h4>The main screen</h4>
<img src="https://mmdok.se/images/admin_main.png" alt="Bilden hittades inte" width="800" height="450">
<h4>Screen for defining fields</h4>
<img src="https://mmdok.se/images/admin_field.png" alt="Bilden hittades inte" width="800" height="450">

