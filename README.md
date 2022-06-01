# Reverse Shell Server

A very small and consise reverse shell server.  
It's mainly used in order to simplify the concurrency of multiple connections.

## Usage

- Launch the server with `ipython -i server.py`
```py
Server started on port 8080.

Received new agent connection from ('127.0.0.1', 60446)

In [1]: server.agents
Out[1]: [Agent @ 127.0.0.1]

In [2]: agent = server.agents[0]

In [3]: agent.run_shell_cmd('whoami')
Out[3]: 'elon'
```
