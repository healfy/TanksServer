

.PHONY: proto

proto:
	python3 -m grpc_tools.protoc -I. --python_out=rpc/. --grpclib_python_out=rpc/. ./proto/tanks.proto