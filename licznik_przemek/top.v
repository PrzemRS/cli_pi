module top(	input clk,
				input nRst,
				input cnt,
				input backward,
				output [3:0] led,
				output [7:0] segments,
				output [3:0] active_segment
				);

counter counter_inst(.clk(clk), .nRst(nRst), .cnt(cnt), .backward(backward), .led(led), .segments(segments), .active_segment(active_segment), .fi_en());
endmodule