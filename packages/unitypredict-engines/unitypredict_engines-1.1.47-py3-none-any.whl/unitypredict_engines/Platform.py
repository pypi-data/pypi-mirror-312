from abc import ABCMeta, abstractmethod
from io import BufferedReader, IOBase

class OutcomeValue:
    Probability = 0.0
    Value = None

    def __init__(self, value: any = '', probability: float = 0.0):
        self.Probability = probability
        self.Value = value

class InferenceContextData:
    StoredMeta: dict = {}

    def __init__(self):
        self.StoredMeta = {}

class InferenceRequest:
    InputValues: dict
    DesiredOutcomes: list
    Context: InferenceContextData = None 
    def __init__(self):
        self.Context = InferenceContextData()
        self.InputValues = {}
        self.DesiredOutcomes = []
    
class InferenceResponse:
    ErrorMessages: str = ''
    AdditionalInferenceCosts: float = 0.0
    ReInvokeInSeconds: int = -1
    Context: InferenceContextData = None
    OutcomeValues: dict = {}
    Outcomes: dict = {}

    def __init__(self):
        self.ErrorMessages = ''
        self.AdditionalInferenceCosts = 0.0
        self.ReInvokeInSeconds = -1
        self.Context = InferenceContextData()
        self.OutcomeValues = {}
        self.Outcomes = {}

class ChainedInferenceRequest:
    ContextId: str = ''
    InputValues: dict
    DesiredOutcomes: list

    def __init__(self, contextId='', inputValues={}, desiredOutcomes=[]):
        self.ContextId = contextId
        self.InputValues = inputValues
        self.DesiredOutcomes = desiredOutcomes

    
class ChainedInferenceResponse:
    ContextId: str = ''
    RequestId: str = ''
    ErrorMessages: str = ''
    ComputeCost: float = 0.0
    OutcomeValues: dict = {}
    Outcomes: dict = {}

    def __init__(self):
        self.ContextId = ''
        self.RequestId = ''
        self.ErrorMessages = ''
        self.ComputeCost = 0.0
        self.OutcomeValues = {}
        self.Outcomes = {}

    def getOutputValue(self, outputName: str, index = 0):
        if self.Outcomes == None:
            return None
        
        if outputName not in self.Outcomes:
            return None
        
        if len(self.Outcomes.get(outputName)) > index:
            if isinstance(self.Outcomes.get(outputName)[index], dict):
                return self.Outcomes.get(outputName)[index].get('value')
            elif isinstance(self.Outcomes.get(outputName)[index], OutcomeValue):
                return self.Outcomes.get(outputName)[index].Value
        else:
            return None

class FileTransmissionObj:
    FileName: str = ''
    FileHandle: IOBase = None

    def __init__(self, fileName, fileHandle):
        self.FileName = fileName
        self.FileHandle = fileHandle

class FileReceivedObj:
    FileName: str = ''
    LocalFilePath: str = ''

    def __init__(self, fileName, localFilePath):
        self.FileName = fileName
        self.LocalFilePath = localFilePath

class IPlatform:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def getModelsFolderPath(self) -> str: raise NotImplementedError

    @abstractmethod
    def getModelFile(self, modelFileName: str, mode: str = 'rb') -> IOBase: raise NotImplementedError

    @abstractmethod
    def getRequestFile(self, requestFileName: str, mode: str = 'rb') -> IOBase: raise NotImplementedError

    @abstractmethod
    def saveRequestFile(self, requestFileName: str, mode: str = 'wb') -> IOBase: raise NotImplementedError

    @abstractmethod
    def getRequestFilePublicUrl(self, requestFileName: str) -> str: raise NotImplementedError

    @abstractmethod
    def getLocalTempFolderPath(self) -> str: raise NotImplementedError

    @abstractmethod
    def logMsg(self, msg: str): raise NotImplementedError

    @abstractmethod
    def invokeUnityPredictModel(self, modelId: str, request: ChainedInferenceRequest) -> ChainedInferenceResponse: raise NotImplementedError


test = ChainedInferenceResponse()
test.Outcomes = {
    'outcome': [OutcomeValue('hello', 0)]
}

print(test.getOutputValue('outcome'))