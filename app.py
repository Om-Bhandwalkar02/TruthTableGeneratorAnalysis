from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import advanced_truth_table

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogicExpression(BaseModel):
    expression: str

@app.get("/")
def home():
    return {"message": "Truth Table Generator API is running!"}

@app.post("/generate-truth-table")
def generate_truth_table(data: LogicExpression):
    result = advanced_truth_table(data.expression)

    if result["error"]:
        raise HTTPException(status_code=400, detail=result["error"])

    result["truth_table"] = result["truth_table"].astype(str).to_dict(orient='records')

    return result

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
