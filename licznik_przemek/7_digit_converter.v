module digit_converter ( value, segments );

	input [3:0] value;
	output [7:0] segments;
	reg [7:0] temp_segments;

	// 7 segment conversion
	always @ (value)
		case (value)
			4'b0000 : temp_segments <= 8'b00111111 ; // 0
			4'b0001 : temp_segments <= 8'b00000110 ; // 1
			4'b0010 : temp_segments <= 8'b01011011 ; // 2
			4'b0011 : temp_segments <= 8'b01001111 ; // 3
			4'b0100 : temp_segments <= 8'b01100110 ; // 4
			4'b0101 : temp_segments <= 8'b01101101 ; // 5
		  4'b0110 : temp_segments <= 8'b01111101 ; // 6
			4'b0111 : temp_segments <= 8'b00000111 ; // 7
			4'b1000 : temp_segments <= 8'b01111111 ; // 8
			4'b1001 : temp_segments <= 8'b01101111 ; // 9
			4'b1010 : temp_segments <= 8'b01110111 ; // A
			4'b1011 : temp_segments <= 8'b01111100 ; // b
			4'b1100 : temp_segments <= 8'b01011000 ; // c
			4'b1101 : temp_segments <= 8'b01011110 ; // d
			4'b1110 : temp_segments <= 8'b01111001 ; // E
			4'b1111 : temp_segments <= 8'b00000000 ; // All off
	  endcase
		 
	assign segments = temp_segments;

endmodule