# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest

class ExecuteOperationSyncRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'BPStudio', '2021-09-31', 'ExecuteOperationSync','bpstudio')
		self.set_method('POST')

	def get_ClientToken(self): # String
		return self.get_body_params().get('ClientToken')

	def set_ClientToken(self, ClientToken):  # String
		self.add_body_params('ClientToken', ClientToken)
	def get_ResourceGroupId(self): # String
		return self.get_body_params().get('ResourceGroupId')

	def set_ResourceGroupId(self, ResourceGroupId):  # String
		self.add_body_params('ResourceGroupId', ResourceGroupId)
	def get_ServiceType(self): # String
		return self.get_body_params().get('ServiceType')

	def set_ServiceType(self, ServiceType):  # String
		self.add_body_params('ServiceType', ServiceType)
	def get_Attributes(self): # String
		return self.get_body_params().get('Attributes')

	def set_Attributes(self, Attributes):  # String
		self.add_body_params('Attributes', Attributes)
	def get_ApplicationId(self): # String
		return self.get_body_params().get('ApplicationId')

	def set_ApplicationId(self, ApplicationId):  # String
		self.add_body_params('ApplicationId', ApplicationId)
	def get_Operation(self): # String
		return self.get_body_params().get('Operation')

	def set_Operation(self, Operation):  # String
		self.add_body_params('Operation', Operation)
