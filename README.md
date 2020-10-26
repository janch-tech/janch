# janch
A YAML config centric tool to act on your service status

# Functional requirements
1. Able to check if there are any errors
2. Able to check if output is valid
    1. Equals specified value
    2. Matches a regular expression
3. Utility types
    1. http(s) response using curl
    2. matches of linux grep
    3. output of any linux command
    4. ..

# Non functional requirements

1. Simple YAML
2. Less time taken for someone new to be able to use it
3. Pretty CLI
4. Greppable CLI output
5. Uses Async where possible
6. Self Documentated 
7. Extendable
8. Pluggable
9. Documented code
10. Unit tested code



# Todos

- [x] Write a utility to gather and inspect any resource
- [x] The utility should configurable via yaml
- [x] Basic Curl check
- [x] Grep command check
- [x] Read dotenv files
- [x] Create CLI loggers
- [x] Regex Inspector
- [x] Write Gatherer (command type)
- [x] Expected vs Actual comparison
- [ ] Make Regex group printable
- [ ] Regex Groups
- [ ] Write Gatherer (permission type)
- [ ] Write Gatherer (disk space type)
- [ ] Write Gatherer (memory usage type)
- [ ] Write Gatherer (cpu usage type)
- [ ] Write Gatherer (database type)
- [ ] Use Queue
- [ ] Default gatherer should be simple url
- [ ] Default inspector should check if error occured
- [ ] CLI option to run only one item
- [ ] CLI option to get info about a gatherer type
- [ ] abstract base class for gatherers
- [ ] abstract base class for inspectors
- [ ] abstract base class for actors
- [ ] abstract based class for loggers
- [ ] Doc blocks
- [ ] Research readthedocs
- [ ] Create file loggers
- [ ] Expression Parser
- [ ] Alternate layout
- [ ] Write unit tests
- [ ] Explore Integration with Graphite
- [ ] Explore webserver mode
- [ ] Plugin by reading plugin location
- [ ] Set up proper logging
- [ ] Log formatters
