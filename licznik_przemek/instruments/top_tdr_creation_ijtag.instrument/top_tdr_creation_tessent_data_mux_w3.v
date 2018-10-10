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

module top_tdr_creation_tessent_data_mux_w3 (
  ijtag_select,
  functional_data_in,
  ijtag_data_in,
  data_out
);
 
input               ijtag_select;
input  [2:0]        functional_data_in;
input  [2:0]        ijtag_data_in;
output [2:0]        data_out;
 
assign data_out = (ijtag_select) ? ijtag_data_in : functional_data_in;
 
endmodule
