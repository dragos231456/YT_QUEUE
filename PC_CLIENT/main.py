from GUI import GUI_Client
from used_materials import Network_Extractor

extractor = Network_Extractor()           
client = GUI_Client(extractor)
client._run()
