from dataclasses import dataclass


@dataclass
class PageParams:
    page: int = 1
    page_size: int = 10
