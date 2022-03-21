import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ML Pkg
import joblib as joblib
from statsmodels.tsa.ar_model import AutoReg

# Models
sell_model = open("models/tickit.pkl", "rb")
sell_clf = joblib.load(sell_model)

#init app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

#Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "prediction_text": "..."})

#ML Aspect

@app.get("/predict/{date}")
async def get_sell_date(date: str):
  day = 342 + int(date.split('-')[2])
  prediction = sell_clf.predict(day,day)
  output = int(prediction[0]) / 100000000 #10*^-8
  output = round(output,1)
  return {"prediccion":output}

@app.post("/predict", response_class=HTMLResponse)
async def handle_form(request: Request, Day_p:str = Form(...)):
  day = 342 + int(Day_p.split('-')[2])
  prediction = sell_clf.predict(day,day)
  output = int(prediction[0]) / 100000000 #10*^-8
  output = round(output,1)
  msg = "El pronostico de ventas es {} ".format(output)
  return templates.TemplateResponse("home.html", {"request": request, "prediction_text": msg})

if __name__ == '__main__':
  uvicorn.run(app,host="127.0.0.1", port=8000)