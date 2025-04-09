"""?"""
from app import webserver
from flask import request, jsonify

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """POST request to post_endpoint"""
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """GET request to get_results/<job_id>"""
    print(f"JobID is {job_id}")

    job_id_int = int(job_id)

    if job_id_int >= webserver.job_counter or job_id_int < 0:
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})

    job_result = webserver.tasks_runner.job_dict.get(job_id_int)

    if job_result is None:
        return jsonify({'status': 'running'})

    return jsonify({'status': 'done', 'data': job_result})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """POST request to states_mean"""

    payload = request.json
    
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/states_mean', None)
    
    return jsonify({"job_id": new_job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """POST request to state_mean"""

    payload = request.json
    target_state = payload.get('state')
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/state_mean', target_state)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """POST request to best5"""

    payload = request.json
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/best5', None)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """POST request to worst5"""

    payload = request.json
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/worst5', None)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """POST request to global_mean"""

    payload = request.json
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/global_mean', None)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """POST request to diff_from_mean"""

    payload = request.json
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/diff_from_mean', None)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """POST request to state_diff_from_mean"""

    payload = request.json
    target_state = payload.get('state')
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/state_diff_from_mean', target_state)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """POST request to mean_by_category"""

    payload = request.json
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/mean_by_category', None)

    return jsonify({"job_id": new_job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """POST request to state_mean_by_category"""

    payload = request.json
    target_state = payload.get('state')
    new_job_id = webserver.job_counter
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(new_job_id, payload, '/api/state_mean_by_category', target_state)

    return jsonify({"job_id": new_job_id})

@webserver.route('/')
@webserver.route('/index')
def index():
    """root - /index endpoints requests"""
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs =""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """defined routes for webserver"""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
