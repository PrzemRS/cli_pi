module licznik(
	input clk,
	input nRst,
	output [3:0] led,
	output [7:0] segments,
	output [3:0] active_segment
);
	
	wire clk_o;
	reg update = 0;
	reg [3:0] counter = 4'b1111;
	reg [3:0] value = 4'b0000;
	reg [1:0] iter = 2'b00 ;
	
	
   reg [7:0] temp_segments = 7'b1111100;
	reg [3:0] temp_active_segment = 2'b00;

	clock_divider clock_divider_inst (.clk_i(clk), .rst_i(nRst), .clk_o(clk_o));
	//digit_converter digit_converter_inst (.clk(clk), .rst(nRst), .segments(segments), .value(value)  );


	always @(posedge clk_o or negedge nRst)
		if(nRst == 1'b0)
		begin
			counter = 4'b1111;
		end
		else if (iter > 0)
		    update <= 1'b0;
		else 	begin
			counter = counter - 1;
			update <= 1'b1;
			end
		
	assign led = counter;
	
	always @ (posedge clk or negedge nRst) 
	  if(nRst == 1'b0)
	   	iter = 2'd4;	 	
	  else if (update)
			iter = 2'd4;			
     else if (iter > 0) 
	      begin
			value = ((counter*(-1)) / 10^(iter-1)) % 10;
			temp_active_segment <= (4-iter);
			iter = iter -1;
			end
			
			
	always @ (posedge clk or negedge nRst)
		if(nRst == 1'b0)
		    temp_segments = 7'b1111100;
		else case (value)
	    	4'b0000 : temp_segments = 7'b0000001 ; // 0
	    	4'b0001 : temp_segments = 7'b1001111 ; // 1
	    	4'b0010 : temp_segments = 7'b0010010 ; // 2
	    	4'b0011 : temp_segments = 7'b0000110 ; // 3
	    	4'b0100 : temp_segments = 7'b1001100 ; // 4
	    	4'b0101 : temp_segments = 7'b0100100 ; // 5
	      4'b0110 : temp_segments = 7'b0100000 ; // 6
	    	4'b0111 : temp_segments = 7'b0001111 ; // 7
	    	4'b1000 : temp_segments = 7'b0000000 ; // 8
	    	4'b1001 : temp_segments = 7'b0000100 ; // 9
	    endcase
			
	assign segments = temp_segments;
	assign active_segment = temp_active_segment;
			
			
	//always @(posedge clk)
			
			//segments = (counter*(-1)) / 1 % 10;
			//segments = (counter*(-1)) / 10 % 10;
			//segments = (counter*(-1)) / 100 % 10;
			//segments = (counter*(-1)) / 1000 % 10;
	  
	
	
	//assign segments = "0000011";
	//assign active_segment = "1110";
	
	
	
	//case (data_input):
	//	4'b0000 : segments <= "1111100" ; // 0
	//	4'b0001 : segments <= "1111001" ; // 1
	//	4'b0010 : segments <= "0100100" ; // 2
	//	4'b0011 : segments <= "0110000" ; // 3
	//	4'b0100 : segments <= "0011001" ; // 4
	//	4'b0101 : segments <= "0010010" ; // 5
	//	4'b0110 : segments <= "0000010" ; // 6
	//	4'b0111 : segments <= "1111000" ; // 7
	//	4'b1000 : segments <= "0000000" ; // 8
	//	4'b1001 : segments <= "0010000" ; // 9
	//endcase
    						 
						 
endmodule