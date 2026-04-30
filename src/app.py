from flask import Flask,request,render_template
import markdown
from AIlesson1 import model_input

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    response_html = ""
    if request.method =='POST':
        input_text = request.form['input_text']
        response = model_input(input_text)
        response_html = markdown.markdown(
            response,
            extensions=[
                "fenced_code"
            ]
        )

    return render_template(
        "response.html",
        response=response_html
    )

def custom_model_response(input_text):
    return "这是自定义模型回复：" + input_text

if __name__ =='__main__':
    app.run(debug=True)