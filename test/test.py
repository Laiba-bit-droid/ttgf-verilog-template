# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start: Ami ki Safety Pin 🧷")

    # 100 kHz clock (10 us period)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # Smoke test: outputs resolved hone chahiye (no X/Z)
    dut._log.info("Smoke test")
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value.is_resolvable, "uo_out has X/Z after reset"

    # Input toggle test
    dut.ui_in.value = 0b00000000
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value.is_resolvable, "uo_out has X/Z after input toggle"

    dut._log.info("All checks passed ✅")

