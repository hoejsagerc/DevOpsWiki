import logging
from fastapi import FastAPI
import azure.functions as func


app = FastAPI()

def main(req: func.HttpRequest, context:func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req)

