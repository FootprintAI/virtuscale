from virtuscale.backend.base import Base

def compile(builder: Base, output_path: str):
    builder.compile(output_path)
