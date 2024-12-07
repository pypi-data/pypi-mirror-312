import time

import requests
import base64
import os

RIVALZ_API_URL = "https://be.rivalz.ai"

RAG_API_URL = "https://rivalz-rag-be.vinhomes.co.uk"


class RivalzClient:
    def __init__(self, secret: str = ''):
        self.secret = secret or os.getenv('SECRET_TOKEN')

    def __uload_to_r2(self, file_path: str):
        file_name = os.path.basename(file_path)

        presigned_url_resp = requests.post(f"{RIVALZ_API_URL}/api-v2/ipfs-v2/make-r2-presigned-url", json={
            "fileName": file_name,
            "fileSize": os.path.getsize(file_path)
        }, headers={
            'Authorization': f'Bearer {self.secret}'
        })

        presigned_url_resp.raise_for_status()  # Raise an error for bad status codes
        presigned_url = presigned_url_resp.json()['data']['url']
        upload_hash = presigned_url_resp.json()['data']['uploadHash']
        with open(file_path, 'rb') as file:
            upload_res = requests.put(presigned_url, data=file)
            upload_res.raise_for_status()  # Raise an error for bad status codes
            return upload_hash

    def upload_file(self, file_path: str):
        return self.__uload_to_r2(file_path)

    def upload_passport(self, file_path: str):
        return self.__uload_to_r2(file_path)

    def download(self, upload_hash: str, save_path: str):
        headers = {
            'Authorization': f'Bearer {self.secret}'
        }
        res = requests.get(f"{RIVALZ_API_URL}/api-v2/ipfs-v2/r2-download-url/{upload_hash}", headers=headers)
        res.raise_for_status()  # Raise an error for bad status codes        
        data = res.json()['data']
        url = data['url']
        res = requests.get(url)
        res.raise_for_status()  # Raise an error for bad status codes
        # Save the file
        with open(save_path, 'wb') as file:
            file.write(res.content)
        return save_path

    def get_upload_history(self, page: int = 0, size: int = 10):
        headers = {
            'Authorization': f'Bearer {self.secret}'
        }
        res = requests.get(f"{RIVALZ_API_URL}/api-v1/upload-history", headers=headers, params={
            'page': page,
            'size': size
        })
        res.raise_for_status()  # Raise an error for bad status codes
        total_files_uploaded = res.json()['data']['totalFilesUploaded']
        upload_histories = res.json()['data']['uploadHistories']
        return total_files_uploaded, upload_histories

    def delete_file(self, upload_hash: str):
        headers = {
            'Authorization': f'Bearer {self.secret}'
        }
        res = requests.post(f"{RIVALZ_API_URL}/api-v2/ipfs-v2/r2-delete-file/{upload_hash}", headers=headers)
        res.raise_for_status()  # Raise an error for bad status codes
        return res.json()

    def __upload_file(self, file_path: str):
        request_presigned_url = RAG_API_URL + "/presigned-url"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        file_key = str(round(time.time() * 1000)) + "_" + os.path.basename(file_path)
        params = {
            'file_name': file_key
        }
        res = requests.get(request_presigned_url, headers=headers, params=params)
        res.raise_for_status()
        pre_signed_url = res.json()['url']
        # upload file
        with open(file_path, 'rb') as file:
            res = requests.put(pre_signed_url, data=file)
            res.raise_for_status()  # Raise an error for bad status codes
        return file_key

    def create_rag_knowledge_base(self, file_path: str, knowledge_base_name: str):
        file_key = self.__upload_file(file_path)
        create_knowledge_base_url = RAG_API_URL + "/knowledge-bases"
        payload = {
            'name': knowledge_base_name,
            'fileKey': file_key
        }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(create_knowledge_base_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def add_document_to_knowledge_base(self, file_path: str, knowledge_base_id: str):
        file_key = self.__upload_file(file_path)
        add_document_url = RAG_API_URL + "/knowledge-bases/add-file"
        payload = {
            'id': knowledge_base_id,
            'fileKey': file_key
        }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(add_document_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def delete_document_from_knowledge_base(self, file: str, knowledge_base_id: str):
        delete_document_url = RAG_API_URL + "/knowledge-bases/del-file"
        payload = {
            'id': knowledge_base_id,
            'fileKey': file
        }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(delete_document_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def get_knowledge_bases(self):
        get_knowledge_base_url = RAG_API_URL + "/knowledge-bases"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_knowledge_base_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_knowledge_base(self, knowledge_base_id: str):
        get_knowledge_base_url = RAG_API_URL + f"/knowledge-bases/{knowledge_base_id}"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_knowledge_base_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def create_chat_session(self, knowledge_base_id: str, message: str, session_id=None):
        create_chat_session_url = RAG_API_URL + "/chats"
        if session_id is None:
            payload = {
                'knowledge_id': knowledge_base_id,
                'message': message
            }
        else:
            payload = {
                'knowledge_id': knowledge_base_id,
                'message': message,
                'sessionID': session_id
            }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(create_chat_session_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def get_chat_session(self, session_id: str):
        get_chat_session_url = RAG_API_URL + f"/chats/detail/{session_id}"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_chat_session_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_chat_sessions(self):
        get_chat_sessions_url = RAG_API_URL + "/chat-sessions"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_chat_sessions_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_uploaded_documents(self):
        get_uploaded_documents_url = RAG_API_URL + "/files"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_uploaded_documents_url, headers=headers)
        res.raise_for_status()
        return res.json()
