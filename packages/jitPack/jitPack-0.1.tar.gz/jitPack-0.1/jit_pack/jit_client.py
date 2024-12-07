from jit_pack.jit_message import MessageServer
from jit_pack.jit_auth import JitAuth 
from jit_pack.jit_orders import JitOrders  




class JitApp:
    instance = None
    def __init__(self, auth:JitAuth, messaging:MessageServer, orders: JitOrders):
        if JitApp.instance is not None:
            raise Exception("Use Jitapp.initialize() to create an instance.")
       
        self.auth = auth
        self.messaging= messaging
        self.orders= orders
        self._setup_auth_listener()

    @staticmethod
    def initialize():
        """
        Initialize the JitApp with its components.

        Returns:
            JitApp: Initialized JitApp instance
        """
        if JitApp.instance is None:
            JitApp.instance = JitApp(auth= JitAuth(), messaging= MessageServer(),orders= JitOrders())
        return JitApp.instance




    def _setup_auth_listener(self) -> None:
        def treat_user(user: dict) -> None:
            if user:
                self.messaging.start_server()
            else:
                self.messaging.dispose()

        self.auth.user_subject.subscribe(on_next= treat_user, 
                                                    on_completed= self.messaging.dispose, 
                                                    on_error= self.messaging.dispose)


    @staticmethod
    def dispose():
        """
        Disposes of resources, stopping all threads and servers.
        This includes:
            - Auth service disposal
            - Messaging server shutdown
        """
        if JitApp.instance:
            try:
                JitApp.instance.auth.dispose()
                JitApp.instance.messaging.dispose()
            finally:
                JitApp.instance = None