import json
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        return {"nik":"mok"}  

print(json.dumps(2 + 1j, cls=ComplexEncoder))