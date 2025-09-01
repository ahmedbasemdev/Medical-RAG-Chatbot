from flask import Flask,request,render_template,jsonify, session, redirect, url_for
from app.components.retriever import create_qa_chain
from dotenv import load_dotenv
from makeupsafe import Makeup
load_dotenv()
import os

app = Flask(__name__)
app.secret_key =  os.urandom(24)
load_dotenv()

def nl2br(value):
      return Makeup(value.replace("\n","<br>"))

app.jinja_env.filters['nl2br'] = nl2br

@app.route("/",methods=["GET","POST"])
def index():
      if "messages" not in session:
            session["messages"] = []
            
      if request.method == "POST":
            user_input = request.form["prompt"]

            if user_input:
                  messages = session["messages"]
                  messages.append({"role":"user","content":user_input})
                  session["messages"] = messages

                  try:
                        qa_chain = create_qa_chain()
                        if qa_chain is None:
                              raise Exception("QA chain could not be created (LLM or VectorStore issue)")
                        
                        response = qa_chain.invoke({"query":user_input})
                        result = response.get("result", "No Response from the model")

                        messages.append({"role":"assistant","content":result})
                        session["messages"] = messages
                  except Exception as e:
                        error_msg = f"Error : {str(e)}"
                        return render_template("index.html" , messages = session["messages"] , error = error_msg)

                        
            return redirect(url_for("index"))
      return render_template("index.html",messages=session.get("messages",[]))

@app.route("/clear",methods=["GET"])
def clear():
      session.pop("messages",None)
      return redirect(url_for("index"))

if __name__ == "__main__":
      app.run(host="0.0.0.0",port=5000, debug=False, use_reloader=False)
