# Example file

# from uuid import UUID

# from fastapi import Depends, FastAPI

# from trace_logger.config import configure_logging, get_logger
# from trace_logger.deps import get_trace_id
# from trace_logger.middleware import TraceIDMiddleware

# # User explicitly configures logging
# configure_logging(level="debug")

# app = FastAPI()
# app.add_middleware(TraceIDMiddleware)

# Keep this in a common file from where you can access through out the project
# logger = get_logger(__name__,)
# logger = get_logger(__name__, sensitive_patterns=['This', 'log'])
# logger = get_logger(__name__, sensitive_patterns=['This', 'log'],show_last=1)


# # Configure sensitive value filter
# sensitive_patterns = [
#     r"\d{16}",  # Example: credit card numbers
#     r"(?:\d{3}-\d{2}-\d{4})",  # Example: SSNs
#     "User", # Example: any text
#     "level",
#     "log",
#     r"(?<=Bearer\s)[a-zA-Z0-9]+" # Example: token
# ]
# logger = get_logger(
#     __name__,
#     sensitive_patterns=sensitive_patterns,
#     show_last=2
# )


# @app.get("/")
# def say_hello(name: str = "Dev", trace_id: UUID = Depends(get_trace_id)):
#     logger.debug("This is debug level log.")
#     logger.info("This is info level log.")
#     logger.error("This is error level log.")
#     logger.warning("This is warning level log.")
#     return {"Message": f"Hello {name}"}


# @app.get("/userinfo")
# def get_user_info(
#     trace_id: UUID = Depends(get_trace_id)
# ):
#     logger.info("User credit card: 1234567812345678.")
#     logger.info("User SSN: 123-45-6789.")
#     logger.info("Token authorization: Bearer abc123DEF456")
#     return {"user": "Dev"}
