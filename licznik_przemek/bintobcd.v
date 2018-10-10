module bintobcd (
  input [15:0] binary,
  output reg [3:0] tensOfThousands,
  output reg [3:0] thousands,
  output reg [3:0] hundreds,
  output reg [3:0] tens,
  output reg [3:0] ones
);

  integer i;
  always @(binary)
  begin
    tensOfThousands = 4'd0;
    thousands = 4'd0;
    hundreds = 4'd0;
    tens = 4'd0;
    ones = 4'd0;

    for (i = 15; i >= 0; i = i-1)
    begin
      // Add 3 to columns >= 5
      if (tensOfThousands >= 5)
        tensOfThousands = tensOfThousands + 3;
      
      if (thousands >= 5)
        thousands = thousands + 3;

      if (hundreds >= 5)
        hundreds = hundreds + 3;

      if (tens >= 5)
        tens = tens + 3;

      if (ones >= 5)
        ones = ones + 3;

      // Shift left one
      tensOfThousands = tensOfThousands << 1;
      tensOfThousands[0] = thousands[3];

      thousands = thousands << 1;
      thousands[0] = hundreds[3];

      hundreds = hundreds << 1;
      hundreds[0] = tens[3];

      tens = tens << 1;
      tens[0] = ones[3];

      ones = ones << 1;
      ones[0] = binary[i];
    end
  end

endmodule
