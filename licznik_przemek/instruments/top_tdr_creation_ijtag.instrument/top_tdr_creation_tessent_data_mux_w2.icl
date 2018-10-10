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
//       Created on: Thu Oct  4 04:17:11 PDT 2018
//--------------------------------------------------------

Module top_tdr_creation_tessent_data_mux_w2 {
 
  DataInPort  ijtag_select;
  DataInPort  ijtag_data_in[1:0];
  DataOutPort data_out[1:0] { 
    Attribute connection_rule_option = "allowed_no_destination";
    Source DM1; 
  }
 
  DataMux DM1[1:0] SelectedBy ijtag_select {
    1'b1 : ijtag_data_in[1:0];
  }
  Attribute tessent_use_in_dft_specification = "false";
  Attribute keep_active_during_scan_test     = "false";
  Attribute tessent_instrument_type          = "mentor::ijtag_node";
  Attribute tessent_signature                = "093ecc5023a7fb22101296cbf6d5c149";
}
