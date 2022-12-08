from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from json import dumps, loads
from flask import session
from time import time
from os import getcwd, path
from pathlib import Path
from base64 import (
  b64encode, 
  b64decode, 
  urlsafe_b64encode, 
  urlsafe_b64decode
)

def open_private_key_file(location):
  file_path = path.join(getcwd(), location)
  location = Path(file_path)
  assert location.is_file(), f"{file_path} does not exist"
  with open(file_path, 'rb') as key_file:
    return serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

class UrlDataSigner:

  def __init__(self, private_key=None):
    if private_key:
      self.private_key = open_private_key_file(private_key)
    else:
      self.private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
      )
    self.public_key = self.private_key.public_key()

  def encode_data(self, data):
    encoded_data = b64encode(
      dumps(data, default=str).encode()
    )

    signature = self.private_key.sign(
      encoded_data,
      padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
      ),
      hashes.SHA256()
    )

    return {
      "signature": urlsafe_b64encode(signature).decode(),
      "data": urlsafe_b64encode(encoded_data).decode()
    }

  def decode_data(self, encoded_data, encoded_signature):
    """takes in url encoded args"""
    signature = urlsafe_b64decode(encoded_signature)
    data = urlsafe_b64decode(encoded_data)
    try:
      self.public_key.verify(
        signature,
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
      )
      return loads(b64decode(data))
    except InvalidSignature:
      raise Exception('Invalid Signature')


class PolicyEncoder:
  

  def __init__(self, private_key=None):
    self.signer = UrlDataSigner(private_key)

  def encode(self, resource, action, expires_in, conditions={}):

    assert isinstance(expires_in, int), \
      "expires should be a unix timestamp"
    assert isinstance(conditions, dict), \
      f"conditions should be a dictionary, got {type(conditions)}"
    assert isinstance(resource, str), \
      "resource should be a string"
    assert isinstance(action, str), \
      "action should be a string"

    policy = {
      "action": action,
      "expires": int(time()) + expires_in,
      "resource": resource,
      "session": session['id'],
      "conditions": conditions
    }

    result = self.signer.encode_data(policy)

    return {
      "policy": result['data'],
      "signature": result['signature']
    }


  def decode(self, action, policy, signature, conditions=False):

    assert policy is not None, "Missing policy"
    assert isinstance(policy, str), "Policy should be a string"
    assert signature is not None, "Missing a policy signature"
    assert isinstance(signature, str), "Signature should be a string"

    # decode policy and verify against signature

    policy = self.signer.decode_data(policy, signature)

    assert policy is not None, "Invalid policy"

    # match policy session with request session

    assert 'session' in policy, "Policy is missing 'session'"
    assert isinstance(policy['session'], str), \
      "Policy session should be a string"
    assert policy['session'] == session['id'], \
        "Url sharing is not allowed"

    # check policy expiration
    
    assert 'expires' in policy, "Policy is missing 'expires'"
    assert int(policy['expires']) >= time(), \
      f"Link expired {int(time() - int(policy['expires']))} second(s) ago)"

    # validate policy action
    
    assert 'action' in policy, "Policy is missing action"
    assert policy['action'] == action, \
      f"Policy action does not match '{action}' got {policy['action']}"

    if conditions:
      assert "conditions" in policy, \
          "Missing policy conditions list"
      assert isinstance(policy['conditions'], dict), \
        "Policy conditions should be a object"

    return policy

policy_encoder = PolicyEncoder()