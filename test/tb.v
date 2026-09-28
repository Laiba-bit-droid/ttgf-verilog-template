`default_nettype none
`timescale 1ns / 1ps

/* This testbench is an electronic wrapper that connects the cocotb test scripts 
   directly to our custom Ami ki Safety Pin silicon module layout. */

module tb ();

  // Dump the signals for simulation waveform viewing
  initial begin
    \$dumpfile("tb.vcd");
    \$dumpvars(0, tb);
    #1;
  end

  // Wire connections mapping the template variables to our chip pins
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

  // Instantiation of our actual hardware brain module (Fixes the unknown module error)
  tt_um_ami_ki_safety_pin user_project (
      .ui_in   (ui_in),    // Dedicated inputs
      .uo_out  (uo_out),   // Dedicated outputs
      .uio_in  (uio_in),   // IOs: Input path
      .uio_out (uio_out),  // IOs: Output path
      .uio_oe  (uio_oe),   // IOs: Enable path
      .ena     (ena),      // logic high enable
      .clk     (clk),      // master system clock
      .rst_n   (rst_n)     // global power-on reset
  );

endmodule

