module clock(
    input clk,
    output reg [3:0] h2,h1,m2,m1,s2,s1 // The actual output
);
    reg temp;
    reg [3:0] e = 4'd0;
    reg [3:0] f = 4'd0;
    reg [3:0] d = 4'd0;
    reg [3:0] c = 4'd0;
    reg [3:0] a = 4'd0;
    reg [3:0] b = 4'd0;
    always @(posedge clk) begin
        s1 = {(~f[0]&f[3])|(f[0]&f[1]&f[2]), (~f[1]&f[2])|(~f[0]&f[2])|(f[0]&f[1]&~f[2]), (f[0]&~f[1]&~f[3])|(~f[0]&f[1]), (~f[0])};
        temp = f[0] & ~f[1] & ~f[2] & f[3];
        s2 = {1'd0, (~e[0]&e[2])|(e[1] & e[0]), (~e[2]&~e[1] & e[0])|(~e[0] & e[1]), (~e[0])};
        s2 = ({4{temp}} & s2) | ({4{~temp}} & e); 
        temp = temp & e[0] & ~e[1] & e[2] & ~e[3];

        m1 = {(~d[0]&d[3])|(d[0]&d[1]&d[2]) , (~d[1]&d[2])|(~d[0]&d[2])|(d[0]&d[1]&~d[2]), (d[0]&~d[1]&~d[3])|(~d[0]&d[1]), (~d[0])};
        m1 = ({4{temp}} & m1) | ({4{~temp}} & d); 
        temp = temp & d[0] & ~d[1] & ~d[2] & d[3];

        m2 = {1'd0, (~c[0]&c[2])|(c[1] & c[0]), (~c[2]&~c[1] & c[0])|(~c[0] & c[1]), (~c[0])};
        m2 = ({4{temp}} & m2) | ({4{~temp}} & c); 
        temp = temp & c[0] & ~c[1] & c[2] & ~c[3];

        h1 = {(~b[0]&b[3])|(b[0]&b[1]&b[2]), (~b[1]&b[2])|(~b[0]&b[2])|(b[0]&b[1]&~b[2]), (b[0]&~b[1]&~b[3])|(~b[0]&b[1]), (~b[0])};
        h1 = ({4{temp}} & h1) | ({4{~temp}} & b);         
        temp = temp & b[0] & ~b[1] & ~b[2] & b[3];

        h2 = {(~a[0]&a[3])|(a[0]&a[1]&a[2]) , (~a[1]&a[2])|(~a[0]&a[2])|(a[0]&a[1]&~a[2]), (a[0]&~a[1]&~a[3])|(~a[0]&a[1]), (~a[0])};
        h2 = ({4{temp}} & h2) | ({4{~temp}} & a);         
        temp = ~s1[0] & ~s1[1] & ~s1[2] & ~s1[3] &~s2[0] & ~s2[1] & ~s2[3] & ~s2[2] & ~a[0] & a[1] & ~a[2] & ~a[3] & b[0] & b[1] & ~b[2] & ~b[3] & c[0] & ~c[1] & c[2] & ~c[3] & d[0] & ~d[1] & ~d[2] & d[3];

        s1 = {4{~temp}} & s1;
        s2 = {4{~temp}} & s2;
        m1 = {4{~temp}} & m1;
        m2 = {4{~temp}} & m2;
        h1 = {4{~temp}} & h1;
        h2 = {4{~temp}} & h2;


        f = s1;
        e = s2;
        d = m1;
        c = m2;
        b = h1;
        a = h2;
    end


endmodule

module main(
    input b1, b2, b3, b4,
    output reg [5:0] power,
    output reg [3:0] disp
);

    wire clk;
    qlal4s3b_cell_macro u_qlal4s3b_cell_macro (
        .Sys_Clk0 (clk),
    );

    localparam integer Freq = 20000000;             // For easier simulation
    localparam integer MUX_DIV = Freq/6;

    // --- Outputs from clock core ---
    wire [3:0] h2, h1, m2, m1, s2, s1;

    reg [22:0] mux_counter = 0;
    reg [2:0] mux_index = 0;

    // --- Pause and Button Edge Logic ---
    reg paused = 0;
    reg b1_prev = 0, b2_prev = 0, b3_prev = 0, b4_prev = 0;
    wire b2_fall = b2_prev && !b2;
    wire b3_fall = b3_prev && !b3;
    wire b4_fall = b4_prev && !b4;

    // --- Clock Pulse Generation ---
    reg [15:0] pulse_remain = 0;    // Number of manual advance pulses left
    reg pulse_active = 0;
    reg aclk = 0;

    // --- The clock core ---
    clock mainclock(
        .clk(aclk),
        .h2(h2), .h1(h1), .m2(m2), .m1(m1), .s2(s2), .s1(s1)
    );

    // --- Edge Sampling ---
    always @(posedge clk) begin
        b1_prev <= b1;     // Pause toggle
        b2_prev <= b2;     // +1 sec
        b3_prev <= b3;     // +1 min
        b4_prev <= b4;     // +1 hour
        if (b1_prev && ~b1)
            paused <= ~paused;
    end

    // --- Multiplexer (DISPLAY ALWAYS RUNS) ---
    always @(posedge clk) begin
        // MUX always cycles for display purposes
        if (mux_counter == MUX_DIV-1) begin
            mux_counter <= 0;
            mux_index <= (mux_index == 5) ? 0 : mux_index + 1;
        end else begin
            mux_counter <= mux_counter + 1;
        end

        case(mux_index)
            0: begin disp <= s1; power <= 6'b000001; end
            1: begin disp <= s2; power <= 6'b000010; end
            2: begin disp <= m1; power <= 6'b000100; end
            3: begin disp <= m2; power <= 6'b001000; end
            4: begin disp <= h1; power <= 6'b010000; end
            5: begin disp <= h2; power <= 6'b100000; end
            default: begin disp <= 4'd0; power <= 6'b000000; end
        endcase
    end

    // --- aclk Pulse Logic ---
    // Exactly one pulse at each MUX cycle in run mode,
    // or N pulses in paused mode after button press
    always @(posedge clk) begin
        // Default: No pulse
        aclk <= 0;

        if (!paused) begin
            // One tick at each mux roll-over (simulate real-time stepping)
            if (mux_counter == MUX_DIV-1 && mux_index == 5) aclk <= 1;
            // No manual-advance activity in run
            pulse_active <= 0;
            pulse_remain <= 0;
        end else begin
            // Button (falling-edge) detection to arm multi-pulse generator
            if (!pulse_active) begin
                if (b2_fall) begin
                    pulse_remain <= 1; pulse_active <= 1;
                end else if (b3_fall) begin
                    pulse_remain <= 60; pulse_active <= 1;
                end else if (b4_fall) begin
                    pulse_remain <= 3600; pulse_active <= 1;
                end
            end else if (pulse_remain > 0) begin
                aclk <= 1;
                pulse_remain <= pulse_remain - 1;
                if (pulse_remain == 1)
                    pulse_active <= 0;
            end
        end
    end

endmodule
