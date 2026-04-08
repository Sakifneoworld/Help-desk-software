from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Planet API", version="1.0.0")

# Planet data
planets = {
    0: "Sun",
    1: "Mercury",
    2: "Venus",
    3: "Earth",
    4: "Mars",
    5: "Jupiter",
    6: "Saturn",
    7: "Uranus",
    8: "Neptune",
}


class PlanetResponse(BaseModel):
    id: int
    name: str


@app.get("/planet/{id}", response_model=PlanetResponse)
def get_planet(id: int):
    """Get planet name by index (0=Sun, 1-8=planets)"""
    if id not in planets:
        raise HTTPException(status_code=404, detail=f"Planet with id {id} not found")
    return PlanetResponse(id=id, name=planets[id])


@app.get("/planets")
def list_planets():
    """List all planets"""
    return [PlanetResponse(id=id, name=name) for id, name in planets.items()]


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
