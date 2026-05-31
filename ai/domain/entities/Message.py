from dataclasses import dataclass


@dataclass
class Message:
    role: str #promt
    content: str #user task


@dataclass
class Qwest:
    id: str #promt
    qwest: str



@dataclass
class mass_qwest:
    qwest: Qwest
