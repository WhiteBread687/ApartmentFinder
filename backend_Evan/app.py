"""Run from backend_Evan: python -m flask --app app run --debug"""
from flask import Flask,request,jsonify
from werkzeug.exceptions import HTTPException
from validation import validate,InvalidSearch
from matching import search
from serializers import response
from config import DATA_MODE
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=65536

@app.get('/api/health')
def health():
    return jsonify(status='ok',data_mode=DATA_MODE)

@app.post('/api/apartments/search')
def apartments():
    criteria=validate(request.get_json())
    return jsonify(response(criteria,search(criteria)))

@app.errorhandler(InvalidSearch)
def invalid(exc):
    return jsonify(error=dict(code='INVALID_SEARCH',message=str(exc),field=exc.field)),400

@app.errorhandler(HTTPException)
def http_error(exc):
    return jsonify(error=dict(code=exc.name.upper().replace(' ','_'),message=exc.description)),exc.code

@app.errorhandler(Exception)
def unexpected(exc):
    app.logger.exception('Search failed')
    return jsonify(error=dict(code='SERVER_ERROR',message='Unable to complete the request. Check the backend logs.')),500
