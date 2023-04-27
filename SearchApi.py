from typing import List
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch.exceptions import ConnectionError, TransportError
from requests.exceptions import ConnectionError as RequestsConnectionError
from time import sleep

app = FastAPI()

es = Elasticsearch(
    [os.environ.get("host")],
    http_auth=(os.environ.get("userName"), os.environ.get("password")),
)

circuit_breaker_policy = None

try:
    circuit_breaker_policy = CircuitBreakerPolicy(3, 30)
except Exception as ex:
    print(f"Failed to create CircuitBreakerPolicy: {ex}")


class CircuitBreakerPolicy:
    def __init__(self, max_failures: int, reset_timeout_seconds: int):
        self.breaker = None
        try:
            self.breaker = Polly.CircuitBreaker.CircuitBreakerPolicy(
                exceptions=[Exception()],
                max_failures=max_failures,
                duration_of_break=reset_timeout_seconds,
            )
        except Exception as ex:
            print(f"Failed to create CircuitBreakerPolicy: {ex}")

    async def execute_async(self, action):
        if self.breaker is not None:
            return await self.breaker.execute_async(action)
        else:
            return await action()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, content={"message": exc.detail}
    )


@app.get("/search")
async def search(city: str = None, rating: int = 1):
    try:
        result = await circuit_breaker_policy.execute_async(
            lambda: search_hotels(city, rating)
        )
        return result
    except Polly.CircuitBreaker.BrokenCircuitException as ex:
        raise HTTPException(status_code=406, detail="Circuit is OPEN.")
    except (ConnectionError, TransportError, RequestsConnectionError) as ex:
        raise HTTPException(status_code=503, detail="Elasticsearch service is not available")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Internal server error")


async def search_hotels(city: str, rating: int) -> List[dict]:
    rating = rating or 1

    s = Search(using=es, index=os.environ.get("indexName"))

    if city is None:
        s = s.query(Q("match_all") & Q("range", Rating={"gte": rating}))
    else:
        s = s.query(
            Q("prefix", CityName={"value": city.lower()})
            & Q("range", Rating={"gte": rating})
        )

    response = await s.execute()
    hotels = [hit.to_dict() for hit in response.hits.hits]
    return hotels
