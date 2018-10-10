//--------------------------------------------------------
//
//  Copyright Mentor Graphics Corporation
//  All Rights Reserved
//
//  THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY
//  INFORMATION WHICH IS THE PROPERTY OF MENTOR GRAPHICS
//  CORPORATION OR ITS LICENSORS AND IS SUBJECT
//  TO LICENSE TERMS.
//
//--------------------------------------------------------
//  File created by: Tessent Shell
//          Version: 2018.4-snapshot_2018.10.04_03.00
//       Created on: Thu Oct  4 04:27:23 PDT 2018
//--------------------------------------------------------

module top_tdr_creation_tessent_tdr_tdr (
  ijtag_reset,
  ijtag_sel,
  ijtag_si,
  ijtag_ce,
  ijtag_se,
  ijtag_ue,
  ijtag_tck,
  led,
  mux_sel,
  fi_en,
  nRst,
  backward,
  cnt,
  ijtag_so
);
 
input               ijtag_reset;
input               ijtag_sel;
input               ijtag_si;
input               ijtag_ce;
input               ijtag_se;
input               ijtag_ue;
input               ijtag_tck;
input  [3:0]        led;
output              mux_sel;
output              fi_en;
output              nRst;
output              backward;
output              cnt;
output              ijtag_so;
 
reg    [4:0]        tdr;
reg                 retiming_so ;
reg                 mux_sel_latch;
reg                 fi_en_latch;
reg                 nRst_latch;
reg                 backward_latch;
reg                 cnt_latch;
 
 
assign mux_sel                          = mux_sel_latch;
assign fi_en                            = fi_en_latch;
assign nRst                             = nRst_latch;
assign backward                         = backward_latch;
assign cnt                              = cnt_latch;
 
// --------- ShiftRegister ---------
 
always @ (posedge ijtag_tck) begin
  if (ijtag_ce & ijtag_sel) begin
    tdr <= { 1'b0,
             led[3],
             led[2],
             led[1],
             led[0]};
  end else if (ijtag_se & ijtag_sel) begin
    tdr <= {ijtag_si,tdr[4:1]};
  end
end
 
assign ijtag_so = retiming_so;
always @ (ijtag_tck or tdr[0]) begin
  if (~ijtag_tck) begin
    retiming_so <= tdr[0];
  end
end
 
// --------- DataOutPort 4 ---------
always @ (negedge ijtag_tck or negedge ijtag_reset) begin
  if (~ijtag_reset) begin
    mux_sel_latch <= 1'b0;
  end else begin
    if (ijtag_ue & ijtag_sel) begin
      mux_sel_latch <= tdr[4];
    end
  end
end
 
// --------- DataOutPort 3 ---------
always @ (negedge ijtag_tck or negedge ijtag_reset) begin
  if (~ijtag_reset) begin
    fi_en_latch <= 1'b0;
  end else begin
    if (ijtag_ue & ijtag_sel) begin
      fi_en_latch <= tdr[3];
    end
  end
end
 
// --------- DataOutPort 2 ---------
always @ (negedge ijtag_tck or negedge ijtag_reset) begin
  if (~ijtag_reset) begin
    nRst_latch <= 1'b0;
  end else begin
    if (ijtag_ue & ijtag_sel) begin
      nRst_latch <= tdr[2];
    end
  end
end
 
// --------- DataOutPort 1 ---------
always @ (negedge ijtag_tck or negedge ijtag_reset) begin
  if (~ijtag_reset) begin
    backward_latch <= 1'b0;
  end else begin
    if (ijtag_ue & ijtag_sel) begin
      backward_latch <= tdr[1];
    end
  end
end
 
// --------- DataOutPort 0 ---------
always @ (negedge ijtag_tck or negedge ijtag_reset) begin
  if (~ijtag_reset) begin
    cnt_latch <= 1'b0;
  end else begin
    if (ijtag_ue & ijtag_sel) begin
      cnt_latch <= tdr[0];
    end
  end
end
 
endmodule
