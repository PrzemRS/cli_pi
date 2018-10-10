module counter(
	input clk,											// Async 10MHz clock
	input nRst,											// Active low rst button
	input cnt,											// Counter button, active low
	input backward,									// Backwart direction counter indicator, active low
	output [3:0] led,								// led outputs
	output [7:0] segments,					// 7 segment outputs
	output [3:0] active_segment,		// Active segment selector
	input fi_en												// Fault injection trigger
);
	
	wire clk2_o, cnt_btn_state, backward_btn_state;

	reg [15:0] counter = 16'd0;

	// Fast clock for multiplexing 7segment displays
	clock_divider #(10_000) clock_divider_inst2 (.clk_i(clk), .rst_i(nRst), .clk_o(clk2_o));
	
	// Debouncers
	PushButton_Debouncer cnt_btn (.clk(clk), .PB(cnt), .PB_state(cnt_btn_state));
	PushButton_Debouncer backward_btn (.clk(clk), .PB(backward), .PB_state(backward_btn_state));

	// Segment selector instance for 4 7segment displays
	segment_selector segment_selector_inst (.value(counter), .clk(clk2_o) ,.nRst(nRst), .segments(segments), .active_segment(active_segment));

	// Counter
	always @(negedge cnt_btn_state or negedge nRst)
	begin
		if(!nRst)
		begin
			counter = 16'd0;
		end
		else 	begin
			if (!backward_btn_state)
			begin
				counter = counter - 1;
				if (counter == 16'b1111111111111111)
					counter = 16'b0010011100001111; // 9999
			end
			else
			begin
				counter = counter + 1;
				if (counter == 16'b0010011100010000) // 10000
					counter = 16'd0;
			end
		end
	end

	// Assign inverted bits because leds are active low.
	assign led = ~counter[3:0];

endmodule