from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

class DocumentHandler:
    def __init__(self, options):
        self.keyLength = options.keyLength or 10;
        self.maxLength = options.maxLength # none by default
        self.store = options.store
        self.keyGenerator = options.keyGenerator


    def handleGet(self, request, response, config):
        key = request.path_params['id'].split('.')[0]
        skipExpire = bool(eval(f"config.documents.{key}"))

        ret = self.store.get(key, skipExpire)
        headers = {'content-type': 'application/json'}
        if ret:
            if str(request.method) == 'HEAD':
                return JSONResponse(status_code=200, headers=headers)
            else:
                content = {"data": ret, "key": key}
                return JSONResponse(status_code=200, content=content, headers=headers)
        else:
            if str(request.method) == 'HEAD':
                return JSONResponse(status_code=404, headers=headers)
            else:
                content = {"message": 'Document not found.'}
                return JSONResponse(status_code=404, content=content, headers=headers)


    def handleRawGet(self, request, response, config):
        key = request.path_params['id'].split('.')[0]
        skipExpire = bool(eval(f"config.documents.{key}"))

        ret = self.store.get(key, skipExpire)
        if ret:
            headers = {'content-type': 'text/plain; charset=UTF-8'}
            if str(request.method) == 'HEAD':
                response.status_code = status.HTTP_200_OK
            else:
                return ret
        else:
            headers = {'content-type': 'application/json'}
            if str(request.method) == 'HEAD':
                return JSONResponse(status_code=404, headers=headers)
            else:
                content = {"message": 'Document not found.'}
                return JSONResponse(status_code=404, content=content, headers=headers)


    def handlePost(self, request, response, buffer):
        buffer = buffer.decode("utf-8") 
        adding = lambda key: self.store.set(key, buffer)

        try:
            if self.maxLength and len(buffer) > self.maxLength:
                cancelled = True
                headers = {'content-type': 'application/json'}
                content = {"message": 'Document exceeds maximum length.'}
                return JSONResponse(status_code=400, content=content, headers=headers)
            elif len(buffer) == 0:
                cancelled = True
                headers = {'content-type': 'application/json'}
                content = {"message": 'Document must contain at least one letter of content.'}
                return JSONResponse(status_code=400, content=content, headers=headers)

            ret, key = self.chooseKey(adding)
            headers = {'content-type': 'application/json'}
            if ret:
                content = {'key': key}
                return JSONResponse(status_code=200, content=content, headers=headers)
            else:
                content = {'message': 'Error adding document.'}
                return JSONResponse(status_code=500, content=content, headers=headers)
        except Exception:
            headers = {'content-type': 'application/json'}
            content = {"message": 'Connection error.'}
            return JSONResponse(status_code=500, content=content, headers=headers)



    def chooseKey(self, callback):
        key = self.acceptableKey()

        ret = self.store.get(key, True)
        if ret:
            self.chooseKey(callback)
        else:
            return callback(key), key


    def acceptableKey(self):
          return self.keyGenerator.createKey(self.keyLength)
