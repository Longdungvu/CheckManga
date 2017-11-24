import checkmanga
from flask import Flask, request, jsonify
app = Flask(__name__)

checkmangautil = checkmanga.CheckMangaUtil('mycheckmanga.db')

@app.route("/")
def hello():
	return "Welcome to the CheckManga API!"

@app.route('/api/checkmanga/', methods=['POST'])
def pass_to_checkmanga():
	 return jsonify(checkmangautil.check_manga())

@app.route('/api/addmanga/', methods=['POST'])
def pass_to_addmanga():
	print request.get_json()
	status_msg = checkmangautil.add_new_manga(request.get_json())
	return jsonify(status_msg)

@app.route('/api/changemangastatus/', methods=['POST']) #changes from ongoing to bookmarked
def pass_to_changemangastatus():
	status_msg = checkmangautil.change_manga_status(request.get_json())
	return jsonify(status_msg)

@app.route('/api/deletemanga/', methods=['POST'])
def pass_to_delete_manga():
	status_msg = checkmangautil.delete_manga(request.get_json())
	return jsonify(status_msg)

@app.route('/api/addnewsite/', methods=['POST'])
def pass_to_add_new_site():
	status_msg = checkmangautil.add_new_site(request.get_json())
	return jsonify(status_msg)

@app.route('/api/getbookmarkedmanga/', methods=['GET'])
def pass_to_get_bookmarked_manga():
	status_msg = checkmangautil.get_all_bookmarked()
	return jsonify({"result":[dict(entry) for entry in status_msg]})

@app.route('/api/getlastreadongoing/', methods=['GET'])
def pass_to_get_last_readongoing():
	status_msg = checkmangautil.get_all_ongoing()
	print status_msg
	return jsonify({"result":[dict(entry) for entry in status_msg]})

@app.route('/api/getsupportedsites/', methods=['GET'])
def pass_to_get_supported_sites():
	status_msg = checkmangautil.get_supported_sites()
	return jsonify({"result":status_msg})



