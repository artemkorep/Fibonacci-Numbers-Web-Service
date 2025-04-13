from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.functional import fibonacci

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    field = error["loc"][-1]

    if field == "n":
        msg = "n must be a non-negative integer"
        if error["type"] == "missing":
            msg = "Parameter 'n' is required"
        return JSONResponse(
            status_code=400,
            content={"error": msg}
        )

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.get("/fibonacci")
def get_fibonacci(n: int = Query(..., ge=0)):
    return {"n": n, "result": fibonacci(n)}