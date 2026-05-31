from dependency.openai import Openaiclient


def getclient(client:str):
    def _getclient():
        if client == 'openai':
            return Openaiclient()

    return _getclient