
from dataclasses import dataclass
from datetime import date
import inspect
from typing import Any, Dict, Type, get_type_hints

from app.domain.common.errors.errors import MissingValueException


@dataclass
class Entity:
    @classmethod
    def create(cls: Type["Entity"], **kwargs) -> "Entity":
        required_attributs = list(cls.__dataclass_fields__.keys())
        
        try:
            hints = get_type_hints(cls)
            none_keys: Dict[str, Any] = {}

            for attribut in required_attributs[:]:
                if attribut not in kwargs:
                    # Vérifie si l'attribut peut être None
                    if 'None' in str(hints[attribut]):
                        none_keys[attribut] = None
                        required_attributs.remove(attribut)
                    else:
                        raise MissingValueException(entity=cls.__qualname__, message=attribut)

            # Instancier automatiquement les sous-dataclasses
            for attr, attr_type in hints.items():
                if attr in kwargs and inspect.isclass(attr_type) and hasattr(attr_type, "__dataclass_fields__"):
                    # Si l'attribut est une dataclass et qu'on a un dictionnaire → instanciation automatique
                    if isinstance(kwargs[attr], dict):
                        kwargs[attr] = attr_type.create(**kwargs[attr])

            keys = {attribut: kwargs[attribut] for attribut in required_attributs}
            keys.update(none_keys)

            return cls(**keys)

        except MissingValueException as mexc:
            raise Exception(mexc)

        except Exception as exc:
            print('Erreur dans creation Entité:', exc)
            raise Exception(exc)

	
# @dataclass 
# class Entity:
# 	# created_on: date

# 	@classmethod
# 	def create(cls, **kwargs):
# 		required_attributs = list(cls.__dataclass_fields__.keys())
		
# 		try:
# 			# identification de tous les champs de la dataclass
# 			hints = get_type_hints(cls)
# 			none_keys: Dict = {}
# 			for attribut in required_attributs[:]:
# 				if attribut not in list(kwargs.keys()):
# 					# s'il manque un champs mais qu'il accepte None, on le met à None, sinon Raise
# 					if 'None' in str(hints[attribut]):
# 						none_keys.update(**{f'{attribut}':None})
# 						required_attributs.remove(attribut)
# 					else:
# 						raise ValueError(f"il manque une valeur pour l'attribut : {attribut}")
					
# 			keys: Dict = {attribut: kwargs[attribut] for attribut in required_attributs}
# 			keys.update(none_keys)
# 			return cls(**keys)
# 		except ValueError as vex:
# 			raise Exception(vex)

# 		except Exception as exc:
# 			print(' error in Importations.create:', exc)
# 			raise Exception(exc)
	