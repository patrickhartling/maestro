import Pyro.core

# you have to change the URI below to match your own host/port.
#cs = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/cluster_server")
cs = Pyro.core.getProxyForURI("PYROLOC://infiscape3:7766/cluster_server")
cs.test()
