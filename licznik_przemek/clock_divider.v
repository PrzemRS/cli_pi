module clock_divider#( parameter DivRatio = 5_000_000 )(clk_i, rst_i, clk_o);
  // I/O ports
  input clk_i, rst_i;
  output reg clk_o;
  // internal signal
  integer counter;
  // divide factor
  // module behavioral description
  always @(posedge clk_i or negedge rst_i)
    if (rst_i==1'b0)
      begin
      counter = 0;
      clk_o = 0;
    end
  else
    begin
      if (counter==(DivRatio-1))
        counter = 0;
        else
        counter = counter + 1;
     if (counter==(DivRatio/2))
  clk_o = 1;
  if (counter==0)
  clk_o = 0;
  end
endmodule