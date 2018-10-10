module segment_selector (
	input [15:0] value,
	input clk,
	input nRst,
	output [7:0] segments,
	output [3:0] active_segment
	);

	wire [3:0] thousands, hundreds, tens, ones;
	wire [7:0] ones_segments, tens_segments, hundreds_segments, thousands_segments;
  reg [7:0] temp_segments;
	reg [3:0] temp_active_segment = 4'b0001;
	wire [3:0] thousands_value, hundreds_value, tens_value, ones_value;

	// Binary to BCD converter
	bintobcd bintobcd_inst (.binary(value), .tensOfThousands(), .thousands(thousands), .hundreds(hundreds), .tens(tens), .ones(ones));

	// binary to 7 segment display converter modules
	digit_converter thousands_digit_converter_inst (.value(thousands_value), .segments(thousands_segments));
	digit_converter hundreds_digit_converter_inst (.value(hundreds_value), .segments(hundreds_segments));
	digit_converter tens_digit_converter_inst (.value(tens_value), .segments(tens_segments));
	digit_converter ones_digit_converter_inst (.value(ones), .segments(ones_segments));

	// Tuen off led displays when not used
	assign thousands_value = (thousands == 4'b0) ? 4'b1111 : thousands;
	assign hundreds_value = (hundreds != 4'b0) ? hundreds : ((thousands != 4'b0) ? hundreds : 4'b1111);
	assign tens_value = (tens != 4'b0) ? tens : ((hundreds != 4'b0) ? tens : ((thousands != 4'b0) ? tens : 4'b1111));

	// segment selector
	always @ (posedge clk or negedge nRst)
	if(!nRst)
	  begin
	   	temp_active_segment = 4'b0001;
			temp_segments = ones_segments;
		end
	else
	begin
		temp_active_segment = {temp_active_segment[2:0], temp_active_segment[3]};
		case (temp_active_segment)
			4'b0001 : temp_segments = ones_segments;
			4'b0010 : temp_segments = tens_segments;
			4'b0100 : temp_segments = hundreds_segments;
			4'b1000 : temp_segments = thousands_segments;
		endcase
	end

	assign segments = temp_segments;
	assign active_segment = temp_active_segment;

endmodule