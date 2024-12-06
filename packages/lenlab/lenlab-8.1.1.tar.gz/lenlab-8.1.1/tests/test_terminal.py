import numpy as np
import pytest

from lenlab.launchpad.protocol import check_memory_28k, make_memory_28k, pack
from lenlab.launchpad.terminal import Terminal
from lenlab.spy import Spy


def test_knock(firmware, terminal: Terminal):
    spy = Spy(terminal.reply)
    terminal.write(packet := pack(b"knock"))
    reply = spy.run_until_single_arg()
    assert reply == packet


def test_hitchhiker(firmware, terminal: Terminal):
    spy = Spy(terminal.reply)
    terminal.write(pack(b"knock") + b"knock")
    reply = spy.run_until_single_arg()
    assert reply == pack(b"knock")

    spy = Spy(terminal.reply)
    assert not spy.run_until()

    spy = Spy(terminal.reply)
    terminal.write(packet := pack(b"knock"))
    reply = spy.run_until_single_arg()
    assert reply == packet


def test_command_too_short(firmware, terminal: Terminal):
    spy = Spy(terminal.reply)
    terminal.write(b"Lk\x05\x00")
    assert not spy.run_until()

    spy = Spy(terminal.reply)
    terminal.write(packet := pack(b"knock"))
    reply = spy.run_until_single_arg()
    assert reply == packet


@pytest.fixture(scope="module")
def memory_28k(terminal: Terminal) -> np.ndarray:
    spy = Spy(terminal.reply)
    terminal.write(packet := pack(b"mi28K"))  # init 28K
    reply = spy.run_until_single_arg()
    assert reply == packet

    return make_memory_28k()


# @pytest.mark.repeat(4000)  # 100 MB, 21 minutes
def test_28k(firmware, terminal: Terminal, memory_28k: np.ndarray):
    spy = Spy(terminal.reply)
    terminal.write(pack(b"mg28K"))  # get 28K
    reply = spy.run_until_single_arg()
    assert reply is not None
    check_memory_28k(reply, memory_28k)
