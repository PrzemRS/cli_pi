module top(	input clk,
				input nRst,
				input cnt,
				input backward,
				output [3:0] led,
				output [7:0] segments,
				output [3:0] active_segment
           	, input wire ijtag_tck, input wire ijtag_reset, input wire ijtag_ce, 
           	input wire ijtag_se, input wire ijtag_ue, input wire ijtag_sel, 
           	input wire ijtag_si, output wire ijtag_so);

  wire tdr0_data_out, tdr0_data_out_ts1, tdr0_data_out_ts2, tdr0_data_out_ts3, 
       tdr0_data_out_ts4;
  wire [2:0] data_out;
counter counter_inst(.clk(clk), .nRst(data_out[2]), .cnt(data_out[0]), .backward(data_out[1]), .led(led), .segments(segments), .active_segment(active_segment), .fi_en(tdr0_data_out_ts4));

  top_tdr_creation_tessent_tdr_tdr top_tdr_creation_tessent_tdr_tdr_inst(
      .ijtag_reset(ijtag_reset), .ijtag_sel(ijtag_sel), .ijtag_si(ijtag_si), .ijtag_ce(ijtag_ce), 
      .ijtag_se(ijtag_se), .ijtag_ue(ijtag_ue), .ijtag_tck(ijtag_tck), .led(led[3:0]), 
      .mux_sel(tdr0_data_out), .fi_en(tdr0_data_out_ts4), .nRst(tdr0_data_out_ts3), 
      .backward(tdr0_data_out_ts2), .cnt(tdr0_data_out_ts1), .ijtag_so(ijtag_so)
  );

  top_tdr_creation_tessent_data_mux_w3 top_tdr_creation_tessent_data_mux_0_inst(
      .ijtag_select(tdr0_data_out), .functional_data_in({nRst, backward, 
      cnt}), .ijtag_data_in({tdr0_data_out_ts3, tdr0_data_out_ts2, 
      tdr0_data_out_ts1}), .data_out(data_out[2:0])
  );
endmodule