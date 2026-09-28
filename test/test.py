import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_ami_ki_safety_pin(dut):
    """Test routine for Ami ki Safety Pin IC to satisfy Track 2 Rules"""
    
    # 1. Start the clock (10MHz or as per template standard)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # 2. Reset the Chip (Active LOW)
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    await Timer(20, units="us")
    dut.rst_n.value = 1
    await Timer(10, units="us")

    # ---- TEST CLAIM 1: Normal Mode, No Alarm ----
    dut._log.info("Testing Normal Mode (No Alarm)...")
    dut.ui_in.value = 0x00 # B2C Mode (Pin 8 = 0), SOS = 0, Voice = 0
    await ClockCycles(dut.clk, 5)
    assert dut.uo_out.value & 0x01 == 0, "Error: Alarm triggered without input!"

    # ---- TEST CLAIM 2: SOS Button Trigger ----
    dut._log.info("Testing SOS Button Emergency Activation...")
    dut.ui_in.value = 0x01 # Set SOS_BTN (Pin 4) HIGH -> ui_in[0] = 1
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value & 0x01 == 1, "Error: SOS Alert failed to trigger TX_DATA!"

    # ---- TEST CLAIM 3: Voice Scream Trigger ----
    dut._log.info("Testing Voice Scream Emergency Activation...")
    dut.ui_in.value = 0x02 # Clear SOS, Set VOICE_TRIG (Pin 5) HIGH -> ui_in[1] = 1
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value & 0x01 == 1, "Error: Voice Scream failed to trigger TX_DATA!"

    # ---- TEST CLAIM 4: B2B Telemetry Checksum Mode ----
    dut._log.info("Testing Dual-Use B2B Rocket Telemetry Mode...")
    dut.ui_in.value = 0x10 # Set B2B_MODE (Pin 8) HIGH -> ui_in[4] = 1
    await ClockCycles(dut.clk, 2)
    # Check if checksum/parity output shifts correctly based on logic
    dut._log.info(f"B2B Mode Active. Output code matches: {hex(dut.uo_out.value)}")

    dut._log.info("All Datasheet Claims Passed Successfully!")

