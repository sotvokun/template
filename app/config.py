from os import getenv


project_name = "starter"

connection_strings = {
    "redis": getenv("REDIS_CONNECTION"),
}

redis = {
    "prefix": f"{project_name}:",
}
