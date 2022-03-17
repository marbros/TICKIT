import uvicorn
from fastapi import FastAPI

# ML Pkg
# import sklearn.external.joblib as extjoblib
import joblib as joblib
import os,sys

sys.modules['sklearn.externals.joblib'] = joblib

# Models
sell_model = open("models/tickit.pkl", "rb")
sell_clf = joblib.load(sell_model)

#init app
app = FastAPI()

#Routes
@app.get('/')
async def index():
  return {'Text':"Hello API Builder"}

@app.get('/items/{date}')
async def items(date):
  return {"text":date}

#ML Aspect

@app.get('/predict/{date}')
async def predict(date):
  prediction = sell_clf.predict(date)
  if prediction[0] == 0:
    result = "something"
  else:
    result = "F"

  return  {"orig_date": date, "prediction": result}

if __name__ == '__main__':
  uvicorn.run(app,host="127.0.0.1", port=8000)