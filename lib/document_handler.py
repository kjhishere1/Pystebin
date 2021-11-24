from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

class DocumentHandler:
    def __init__(self, options):
        self.keyLength = options['keyLength'] or 10;
        self.maxLength = options['maxLength'] # none by default
        self.store = options['store']
        self.keyGenerator = options['keyGenerator']


    async def handleGet(self, request, response, config):
        key = request.path_params['id'].split('.')[0]
        skipExpire = bool(eval(f"config.documents.{key}"))

        ret = self.store.get(key, skipExpire)
        headers = {'content-type': 'application/json'}
        if ret:
            if str(request.method) == 'HEAD':
                return await JSONResponse(status_code=200, headers=headers)
            else:
                content = {"data": ret, "key": key}
                return await JSONResponse(status_code=200, content=content, headers=headers)
        else:
            if str(request.method) == 'HEAD':
                return await JSONResponse(status_code=404, headers=headers)
            else:
                content = {"message": 'Document not found.'}
                return await JSONResponse(status_code=404, content=content, headers=headers)


    async def handleRawGet(self, request, response, config):
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
                return await JSONResponse(status_code=404, headers=headers)
            else:
                content = {"message": 'Document not found.'}
                return await JSONResponse(status_code=404, content=content, headers=headers)


    async def handlePost(self, request, response):
        buffer = ''
        cancelled = False

        async def onSuccess():
            if self.maxLength and len(buffer) > self.maxLength:
                cancelled = True
                headers = {'content-type': 'application/json'}
                content = {"message": 'Document exceeds maximum length.'}
                return await JSONResponse(status_code=400, content=content, headers=headers)

            async def adding(key):
                ret = self.store.set(key, buffer)
                headers = {'content-type': 'application/json'}
                if ret:
                    content = {'key': key}
                    return await JSONResponse(status_code=200, content=content, headers=headers)
                else:
                    content = {'message': 'Error adding document.'}
                    return await JSONResponse(status_code=500, content=content, headers=headers)
            self.chooseKey(adding)

        print('TEST')

        ct = request.headers['content-type']
        if ct and ct.split(';')[0] == 'multipart/form-data':
            pass
        else:
            data = await request.json()
            print(data)



    def chooseKey(callback):
        key = self.acceptableKey()

        ret = self.store.get(key, True)
        if ret:
            self.chooseKey(callback)
        else:
            callback(key)

    def acceptableKey(self):
          return self.keyGenerator.createKey(self.keyLength)