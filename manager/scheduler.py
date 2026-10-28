from generator import GenerateSystem

"""
repository.py -> creates table and api for writing, updating and reading rows (uses the sqlite wrapper)
protocol.py -> converts the python object to json and converts the responses
worker_pool.py -> starts/manages the pool of workers and handles io streams to through protocol.py
"""