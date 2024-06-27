from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from supabase import create_client, Client
import pickle
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import sklearn

load_dotenv()

SUPABASE_URL = 'https://yupyjsyxagknjnzwgiyj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1cHlqc3l4YWdrbmpuendnaXlqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTk0Mzk2NjIsImV4cCI6MjAzNTAxNTY2Mn0.jTYt966Y2gsLSkMVGxrVI9UnZaAbXCbVmyqoYYYEbkQ'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
# Allow requests from all origins
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


model = pickle.load(open('my_model.pickle', "rb"))
# Load the CSV file for feature columns (X_columns assumed to be available globally)
data8 = pd.read_csv('data8_processed.csv')  # Adjust filename as per your saved CSV

# Extract feature columns from data8 (assuming 'price' column is the target)
X_columns = data8.drop('price', axis=1).columns.tolist()


class UserSignup(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class HouseDetails(BaseModel):
    location: str
    sqft: int
    bath: int
    bhk: int

@app.post("/signup/")
async def signup(user:UserSignup):

    try:

        data = {
            "email": user.email,
            "password": user.password,
        }
        print(data)
        response = supabase.table('users').insert(data).execute()

        
        return {"message":"signup successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@app.post("/login/")
async def login(user: UserLogin):
    
    response = supabase.table('users').select('*').eq('email', f'{user.email}').execute()
    print(response)

    user_data = response.data[0]
    if user.password != user_data['password']:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    

    return {"user":"login successfully"}



@app.post("/predict/")
async def predict_price(details: HouseDetails):
    def price_predict(location, sqft, bath, BHK):
        try:
            loc_index = np.where(np.array(X_columns) == location)[0][0]  # Ensure X_columns is treated as an array
            x = np.zeros(len(X_columns))
            x[0] = sqft
            x[1] = bath
            x[2] = BHK
            if loc_index >= 0:
                x[loc_index] = 1
            return model.predict([x])[0]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    try:
        prediction = price_predict(details.location, details.sqft, details.bath, details.bhk)
        return {"predicted_price": f"""₹ {prediction} thousands"""}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
