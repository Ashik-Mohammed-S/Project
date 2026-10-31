from flask import Flask,jsonify,request,send_from_directory
from copilot import Copilot
from finance import ROOT,REPORTS

def create_app():
    app=Flask(__name__,static_folder=str(ROOT/'web'),static_url_path='/assets')
    app.config['MAX_CONTENT_LENGTH']=8192;copilot=Copilot()
    @app.get('/')
    def index():return send_from_directory(ROOT/'web','index.html')
    @app.get('/health')
    def health():return jsonify(status='ok',evidence_documents=len(copilot.retriever.docs),data='synthetic',default_mode='extractive')
    @app.get('/api/reports/<name>')
    def report(name):
        if name not in REPORTS:return jsonify(error='Unknown report'),404
        return jsonify(report=name,rows=copilot.finance.report(name),data='synthetic',source='sql/'+name+'.sql')
    @app.post('/api/ask')
    def ask():
        if not request.is_json:return jsonify(error='Send application/json'),415
        body=request.get_json(silent=True)
        if not isinstance(body,dict):return jsonify(error='Expected JSON object'),400
        try:return jsonify(copilot.ask(body.get('question'),body.get('mode','extractive')))
        except ValueError as error:return jsonify(error=str(error)),400
    @app.after_request
    def headers(response):
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'"
        response.headers['X-Content-Type-Options']='nosniff';return response
    return app

app=create_app()
