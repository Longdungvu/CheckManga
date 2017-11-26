import checkmanga
from flask import Flask, request, jsonify
app = Flask(__name__)

checkmangautil = checkmanga.CheckMangaUtil('mycheckmanga.db')

def validate_input_json_keys(request_json, required_keys):
	for key in required_keys:
		if key not in request_json.keys():
			return key
	return True

def process_json_wrapper(request, func, route_name, required_keys):	
	req_json = request.get_json()
	if not req_json: 
		return {"Failed": "Request JSON was empty."}
	validate = validate_input_json_keys(req_json, required_keys)
	if validate != True:
		return {"Failed": "Failed JSON request had missing key: {0}".format(validate)}
	function_result=func(req_json)
	if function_result: 
		return {"Success": "Successful call to {0} with parameters: {1}".format(route_name, str(req_json))}
	else:
		return {"Failed": "API call failed because request JSON had invalid value."}
	
@app.route("/")
def hello():
	return "Welcome to the CheckManga API!"

@app.route('/api/addmanga/', methods=['POST'])
def pass_to_add_manga():
	req_keys = ["Title", "Site", "Status", "Url", "CoverImageUrl"]
	status_msg = process_json_wrapper(request, checkmangautil.add_manga, "add_manga", req_keys)
	return jsonify(status_msg)

@app.route('/api/deletemanga/', methods=['POST'])
def pass_to_delete_manga():
	req_keys=["Title"]
	status_msg = process_json_wrapper(request, checkmangautil.delete_manga, "delete_manga", req_keys)
	return jsonify(status_msg)

@app.route('/api/addsite/', methods=['POST'])
def pass_to_add_site():
	req_keys=["SiteName", "SitePath"]
	status_msg = process_json_wrapper(request, checkmangautil.add_site, "add_site", req_keys)
	return jsonify(status_msg)

@app.route('/api/deletesite/', methods=['POST'])
def pass_to_delete_site():
	req_keys=["SiteName"]
	status_msg = process_json_wrapper(request, checkmangautil.delete_site, "delete_site", req_keys)
	return jsonify(status_msg)

@app.route('/api/changemangastatus/', methods=['POST']) #changes from ongoing to bookmarked
def pass_to_change_manga_status():
	req_keys = ["Title", "Status"]
	status_msg = process_json_wrapper(request, checkmangautil.change_manga_status, "change_manga_status", req_keys)
	return jsonify(status_msg)

@app.route('/api/updatelastchapterread/', methods=['POST'])
def pass_update_last_chapter_read():
	req_keys = ["Title", "LastChapterRead"]
	status_msg=process_json_wrapper(request, checkmangautil.update_last_chapter_read, "update_last_chapter_read", req_keys)
	return jsonify(status_msg)

@app.route('/api/getallongoingmanga/', methods=['GET'])
def pass_to_get_all_ongoing_manga():
	all_ongoing = checkmangautil.get_all_ongoing_manga()
	return jsonify({"result": all_ongoing})

@app.route('/api/getallbookmarkedmanga/', methods=['GET'])
def pass_to_get_all_bookmarked_manga():
	all_bookmarked= checkmangautil.get_all_bookmarked_manga()
	return jsonify({"result": all_bookmarked})

@app.route('/api/getallsupportedsites/', methods=['GET'])
def pass_to_get_all_supported_sites():
	sites = checkmangautil.get_all_supported_sites()
	return jsonify({"result": sites})

@app.route('/api/checkmanga/', methods=['POST'])
def pass_to_check_manga():
	checked_manga = checkmangautil.check_manga()
	return jsonify({"result": checked_manga})

