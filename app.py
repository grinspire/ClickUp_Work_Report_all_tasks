from flask import Flask, jsonify
import requests

app = Flask(__name__)

api_key = "pk_67411195_OHENSAG9JM2PBQB2A2JWGH8VEJ5A1EOK"

def get_all_tasks_assigned_to_member(member_name):
  team_url = "https://api.clickup.com/api/v2/team"
  payload = {}
  headers = {
    'Content-Type': 'application/json',
    'Authorization': api_key
  }

  response = requests.request("GET", team_url, headers=headers, data=payload)

  # Parse JSON
  data = response.json()
  team_id = data["teams"][0]["id"]

  all_tasks = []

  space_url = f"https://api.clickup.com/api/v2/team/{team_id}/space"
  space_response = requests.request("GET", space_url, headers=headers, data=payload)
  space_response.raise_for_status()
  space_data = space_response.json()
  # Print DataFrame
  for space in space_data['spaces']:
    space_id = space["id"]
    folder_response = requests.get(f"https://api.clickup.com/api/v2/space/{space_id}/folder", headers=headers)
    folder_response.raise_for_status()
    folder_data = folder_response.json()
    for folder in folder_data['folders']:
      folder_id = folder["id"]
      print(folder_id)
      list_response = requests.get(f"https://api.clickup.com/api/v2/folder/{folder_id}/list", headers=headers)
      list_response.raise_for_status()
      list_data = list_response.json()
      for list in list_data['lists']:
        list_id = list["id"]
        print(list_id)
        task_response = requests.get(f"https://api.clickup.com/api/v2/list/{list_id}/task", headers=headers)
        task_response.raise_for_status()
        task_data = task_response.json()
        for task in task_data['tasks']:
          assignees = task.get('assignees', [])
          for assignee in assignees:
            if member_name in assignee.get('username', ''):
          # if ( len(task['assignees']) > 0 and member_name in task['assignees'][0]['username'] ):
              all_tasks.append({'id': task['id'], 'name': task['name'], 'url': task['url']})
              print({'id': task['id'], 'name': task['name'], 'url': task['url']})

  return all_tasks

@app.route('/', methods=['GET'])
def get_welcome():
  # Logic to retrieve and return users
  return 'Welcome to visit api!'

@app.route('/api/tasks/<member_name>', methods = ["POST"])  # Define an API route
def get_tasks_by_member(member_name):
  print(member_name)
  """
  This function retrieves tasks assigned to a member and returns them as JSON.
  """
  tasks_assigned_to_member = get_all_tasks_assigned_to_member(member_name)
  return jsonify(tasks_assigned_to_member)

# if __name__ == '__main__':
#   app.run(debug=True)  # Run the Flask app in debug mode (optional)

# member_name = "Arunima"
# tasks_assigned_to_member = get_all_tasks_assigned_to_member(member_name)
# print(tasks_assigned_to_member)