from abc import ABC,abstractmethod
from src.models import Classification
class LLMProvider(ABC):
 @abstractmethod
 def classify(self,text:str)->Classification: ...
