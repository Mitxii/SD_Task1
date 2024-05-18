# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import chat_pb2 as proto_dot_chat__pb2


class ChatServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterClient = channel.unary_unary(
                '/ChatServer/RegisterClient',
                request_serializer=proto_dot_chat__pb2.Client.SerializeToString,
                response_deserializer=proto_dot_chat__pb2.Boolean.FromString,
                )
        self.SendMessage = channel.unary_unary(
                '/ChatServer/SendMessage',
                request_serializer=proto_dot_chat__pb2.Message.SerializeToString,
                response_deserializer=proto_dot_chat__pb2.Empty.FromString,
                )
        self.ReceiveMessage = channel.unary_unary(
                '/ChatServer/ReceiveMessage',
                request_serializer=proto_dot_chat__pb2.Client.SerializeToString,
                response_deserializer=proto_dot_chat__pb2.Message.FromString,
                )


class ChatServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReceiveMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterClient': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterClient,
                    request_deserializer=proto_dot_chat__pb2.Client.FromString,
                    response_serializer=proto_dot_chat__pb2.Boolean.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=proto_dot_chat__pb2.Message.FromString,
                    response_serializer=proto_dot_chat__pb2.Empty.SerializeToString,
            ),
            'ReceiveMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveMessage,
                    request_deserializer=proto_dot_chat__pb2.Client.FromString,
                    response_serializer=proto_dot_chat__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatServer/RegisterClient',
            proto_dot_chat__pb2.Client.SerializeToString,
            proto_dot_chat__pb2.Boolean.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatServer/SendMessage',
            proto_dot_chat__pb2.Message.SerializeToString,
            proto_dot_chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReceiveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatServer/ReceiveMessage',
            proto_dot_chat__pb2.Client.SerializeToString,
            proto_dot_chat__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)