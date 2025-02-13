from typing import Dict, List
from fastapi import FastAPI
import uvicorn

from app.entrypoints.router import routeur_pipelines, routeur_search



app = FastAPI(
	title='Job Market',
	description="""""",
)

app.include_router(routeur_search)
app.include_router(routeur_pipelines)


# Endpoint pour afficher toutes les routes existantes
@app.get("/routes/", response_model=List[Dict])
async def get_routes():
	routes_info = []
	
	for route in app.routes:
		# On filtre les routes de type 'HTTPRoute' pour éviter les WebSocket ou autres types de routes
		if hasattr(route, "methods"):
			routes_info.append({
				"path": route.path,
				"methods": list(route.methods),
				"name": route.name,
			})
	return routes_info


if __name__ == '__main__':
	uvicorn.run('main:app', host='127.0.0.1', reload=True, port=8080)
