from flask import Flask,request,render_template, Response
from AIlesson1 import model_input_streaming

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "AIStreamResponse.html"
    )
@app.route("/chat",methods=['POST'])
def chat():
    input_text = request.form['input_text']
    def generate():
        for chunk in model_input_streaming(input_text):
            # 直接返回原始markdown，由前端渲染
            yield chunk
    return Response(
        generate(),
        content_type="text/plain; charset=utf-8"
    )
if __name__ =='__main__':
    app.run(debug=True)