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

Module top_tdr_creation_tessent_tdr_tdr {
 
  ResetPort     ijtag_reset             { ActivePolarity 0;      }
  SelectPort    ijtag_sel;
  ScanInPort    ijtag_si;
  CaptureEnPort ijtag_ce;
  ShiftEnPort   ijtag_se;
  UpdateEnPort  ijtag_ue;
  TCKPort       ijtag_tck;
  ScanOutPort   ijtag_so                { Source tdr[0];         }
  DataInPort   led[3:0]                 {
    Attribute connection_rule_option = "allowed_no_source"; 
  }
  DataOutPort   mux_sel                 {
    Source tdr[4];
    Attribute connection_rule_option = "allowed_no_destination";
  }
  DataOutPort   fi_en                   {
    Source tdr[3];
    Attribute connection_rule_option = "allowed_no_destination";
  }
  DataOutPort   nRst                    {
    Source tdr[2];
    Attribute connection_rule_option = "allowed_no_destination";
  }
  DataOutPort   backward                {
    Source tdr[1];
    Attribute connection_rule_option = "allowed_no_destination";
  }
  DataOutPort   cnt                     {
    Source tdr[0];
    Attribute connection_rule_option = "allowed_no_destination";
  }
 
  ScanInterface client { 
    Port ijtag_si; 
    Port ijtag_so; 
    Port ijtag_sel;
  }
 
  Attribute keep_active_during_scan_test = "true";
 
  ScanRegister tdr[4:0] {
    ScanInSource     ijtag_si;
    CaptureSource    1'b0,
                     led[3:0];
    ResetValue       5'b00000;
    DefaultLoadValue 5'b00000;
  }
 
 
  Attribute tessent_use_in_dft_specification = "false";
  Attribute tessent_instrument_type          = "mentor::ijtag_node";
  Attribute tessent_signature                = "e034bcdd54ec3b63a6c55d833f5717a5";
}
