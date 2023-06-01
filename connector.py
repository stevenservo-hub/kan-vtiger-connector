import kanboard
from vtiger import Vtiger

kanboard_url = 'https://kan.example.com/jsonrpc.php'
kanboard_username = ' '
kanboard_password = ' '

vtiger_url = 'https://vtiger.example.net/webservice.php'
vtiger_username = ' '
vtiger_accesskey = ' '

# Kanboard API
kb = kanboard.Client(kanboard_url)
kb.login(kanboard_username, kanboard_password)

# Vtiger API
vt = Vtiger(url=vtiger_url, username=vtiger_username, accesskey=vtiger_accesskey)

# Retrieve Kanboard projects
projects = kb.get_all_projects()

# Retrieve Vtiger accounts
accounts = vt.list_entities(module='Accounts')

# Map Kanboard project IDs to Vtiger account IDs
project_account_mapping = {
    'Kanboard_Project_ID_1': 'Vtiger_Account_ID_1',
    'Kanboard_Project_ID_2': 'Vtiger_Account_ID_2',
    # idk :(
}

def open_vtiger_ticket(task):
    # Get project ID and map it to Vtiger account ID
    project_id = task['project_id']
    if project_id in project_account_mapping:
        account_id = project_account_mapping[project_id]
        # Create ticket in Vtiger
        ticket_data = {
            'ticket_title': task['title'],
            'ticket_desc': task['description'],
            'ticket_status': 'Open',
            'parent_id': account_id
        }
        vt.create_entity(module='HelpDesk', data=ticket_data)
        print(f"Opened Vtiger ticket for Kanboard task '{task['title']}'")

def close_vtiger_ticket(task):
    # Get project ID and map it to Vtiger account ID
    project_id = task['project_id']
    if project_id in project_account_mapping:
        account_id = project_account_mapping[project_id]
        # Find corresponding ticket in Vtiger and close it
        query = f"(subject = '{task['title']}' OR ticket_title = '{task['title']}') AND parent_id = '{account_id}'"
        tickets = vt.query_entities(module='HelpDesk', query=query)
        if len(tickets) > 0:
            ticket_id = tickets[0]['id']
            vt.update_entity(module='HelpDesk', entity_id=ticket_id, data={'ticket_status': 'Closed'})
            print(f"Closed Vtiger ticket for Kanboard task '{task['title']}'")

# Monitor Kanboard tasks
while True:
    tasks = kb.get_all_tasks()
    for task in tasks:
        if task['is_active'] == 1:
            # Task is open
            open_vtiger_ticket(task)
        else:
            # Task is closed
            close_vtiger_ticket(task)
    # Add a delay between checks (e.g., every 5 minutes)
    time.sleep(300)
