from dataclasses import dataclass
import json
from typing import Dict, Type, Union
from fastapi import Body, Form, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel



async def format_to_json(request: Request):
	content_type = request.headers.get("Content-Type", "")
	
	if content_type.startswith("application/json"):
		json_data = json.loads(await request.body())
		if not json_data:
			raise HTTPException(status_code=400, detail="Données JSON manquantes")
	
	elif content_type.startswith("multipart/form-data"):
		form_data = await request.form()
		return form_data
		# json_data = jsonable_encoder(form_data)
	
	else:
		raise HTTPException(status_code=400, detail="Content-Type non supporté")
	
	return json_data
	
