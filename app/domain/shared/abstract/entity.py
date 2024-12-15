
from dataclasses import dataclass
from datetime import date
from typing import Dict, get_type_hints



@dataclass 
class Entity:
	# created_on: date

	@classmethod
	def create(cls, **kwargs):
		required_attributs = list(cls.__dataclass_fields__.keys())
		
		try:
			# identification de tous les champs de la dataclass
			hints = get_type_hints(cls)
			none_keys: Dict = {}
			for attribut in required_attributs[:]:
				if attribut not in list(kwargs.keys()):
					# s'il manque un champs mais qu'il accepte None, on le met à None, sinon Raise
					if 'None' in str(hints[attribut]):
						none_keys.update(**{f'{attribut}':None})
						required_attributs.remove(attribut)
					else:
						raise ValueError(f"il manque une valeur pour l'attribut : {attribut}")
					
			keys: Dict = {attribut: kwargs[attribut] for attribut in required_attributs}
			keys.update(none_keys)
			return cls(**keys)
		except ValueError as vex:
			raise Exception(vex)

		except Exception as exc:
			print(' error in Importations.create:', exc)
			raise Exception(exc)
	