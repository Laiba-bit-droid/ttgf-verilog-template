`default_nettype none

module tt_um_ami_ki_safety_pin (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock signal
    input  wire       rst_n     // reset (active LOW)
);

    // Assigning inputs from ui_in vector based on our datasheet
    wire sos_btn    = ui_in[0];   // Pin 4 equivalent
    wire voice_trig = ui_in[1];   // Pin 5 equivalent
    wire b2b_mode   = ui_in[2];   // Pin 8 equivalent

    // Internal logic registers
    reg tx_data_reg;
    reg status_led_reg;
    reg [7:0] checksum_reg;

    // Output assignment
    assign uo_out[0] = tx_data_reg;    // Pin 6 equivalent
    assign uo_out[1] = status_led_reg;  // Pin 7 equivalent
    assign uo_out[7:2] = 6'b000000;    // Unused pins grounded

    // IO pins configuration (Setting all to inputs/disabled for simplicity)
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Core Sequential Logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_data_reg    <= 1'b0;
            status_led_reg <= 1'b0;
            checksum_reg   <= 8'b0;
        end else begin
            // Heartbeat/Status LED
            status_led_reg <= ~status_led_reg; 

            if (b2b_mode == 1'b0) begin
                // B2C Child Safety Mode Logic
                if (sos_btn == 1'b1 || voice_trig == 1'b1) begin
                    tx_data_reg <= 1'b1; // Trigger Emergency Alarm State
                end else begin
                    tx_data_reg <= 1'b0;
                end
            end else begin
                // B2B Aerospace Mode (Telemetry Checksum Logic)
                checksum_reg <= ui_in + 8'hA5; // Simple custom checksum generation
                tx_data_reg  <= ^checksum_reg;  // Parity bit output
            end
        end
    end
endmodule


