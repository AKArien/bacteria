import grpc

import bacteria_pb2
import bacteria_pb2_grpc
from concurrent import futures

from state import Bacteria, State

def protobuf_state(state: State):
    return {
        State.STABLE: bacteria_pb2.BacteriaInfo.STABLE,
        State.GROWING: bacteria_pb2.BacteriaInfo.GROWING,
        State.SHRINKING: bacteria_pb2.BacteriaInfo.SHRINKING,
        State.DEAD: bacteria_pb2.BacteriaInfo.DEAD,
    }[state]

class BacteriaService(bacteria_pb2_grpc.BacteriaServiceServicer):

	def __init__(self):
		self.bacteria = Bacteria()

	def GetInfo(self, request, context):
		return bacteria_pb2.BacteriaInfo(
			volume=self.bacteria.volume,
			current_state=protobuf_state(self.bacteria.state),
			can_switch_to=[
				protobuf_state(s)
				for s in self.bacteria.can_switch_to
			],
		)

	def ChangeState(self, request, context):
		try:
			new_state = {
				bacteria_pb2.BacteriaInfo.STABLE: State.STABLE,
				bacteria_pb2.BacteriaInfo.GROWING: State.GROWING,
				bacteria_pb2.BacteriaInfo.SHRINKING: State.SHRINKING,
				bacteria_pb2.BacteriaInfo.DEAD: State.DEAD,
			}[request.new_state]

			self.bacteria.change_state(new_state)

			return self.GetInfo(None, context)

		except ValueError as e:
			context.abort(
				grpc.StatusCode.INVALID_ARGUMENT,
				str(e)
			)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

bacteria_pb2_grpc.add_BacteriaServiceServicer_to_server(
    BacteriaService(),
    server,
)

server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
