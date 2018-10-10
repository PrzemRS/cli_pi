//-----------------------------------------------------
//  File created by: Tessent Shell
//          Version: 2018.4-snapshot_2018.10.04_03.00
//       Created on: Thu Oct  4 04:18:18 PDT 2018
//-----------------------------------------------------


Module top {
   // Created by ICL extraction
   CaptureEnPort ijtag_ce;
   ResetPort ijtag_reset {
      ActivePolarity 0;
   }
   ShiftEnPort ijtag_se;
   SelectPort ijtag_sel;
   ScanInPort ijtag_si;
   ScanOutPort ijtag_so {
      Source top_tdr_creation_tessent_tdr_tdr_inst.ijtag_so;
   }
   TCKPort ijtag_tck;
   UpdateEnPort ijtag_ue;
   ScanInterface my_interface {
      Port ijtag_ce;
      Port ijtag_reset;
      Port ijtag_se;
      Port ijtag_sel;
      Port ijtag_si;
      Port ijtag_so;
      Port ijtag_tck;
      Port ijtag_ue;
   }
   Attribute icl_extraction_date = "Thu Oct  4 04:18:18 PDT 2018";
   Attribute created_by_tessent_icl_extract = "true";
   Attribute tessent_design_id = "tdr_creation";
   Attribute tessent_design_level = "sub_block";
   Instance top_tdr_creation_tessent_data_mux_0_inst Of 
       top_tdr_creation_tessent_data_mux_w2 {
      InputPort ijtag_select = top_tdr_creation_tessent_tdr_tdr_inst.mux_sel;
      InputPort ijtag_data_in[1] = 
          top_tdr_creation_tessent_tdr_tdr_inst.backward;
      InputPort ijtag_data_in[0] = top_tdr_creation_tessent_tdr_tdr_inst.cnt;
      Attribute tessent_design_instance = 
          "top_tdr_creation_tessent_data_mux_0_inst";
   }
   Instance top_tdr_creation_tessent_tdr_tdr_inst Of 
       top_tdr_creation_tessent_tdr_tdr {
      InputPort ijtag_reset = ijtag_reset;
      InputPort ijtag_sel = ijtag_sel;
      InputPort ijtag_si = ijtag_si;
      InputPort ijtag_ce = ijtag_ce;
      InputPort ijtag_se = ijtag_se;
      InputPort ijtag_ue = ijtag_ue;
      InputPort ijtag_tck = ijtag_tck;
      InputPort led[3] = 'bx;
      InputPort led[2] = 'bx;
      InputPort led[1] = 'bx;
      InputPort led[0] = 'bx;
      Attribute tessent_design_instance = 
          "top_tdr_creation_tessent_tdr_tdr_inst";
   }
}

// instanced as top.top_tdr_creation_tessent_data_mux_0_inst
Module top_tdr_creation_tessent_data_mux_w2 {
   // ICL module read from source on or near line 17 of file '/wv/pszymans_nb/tdr.tshell/results.64/tsdb_outdir/instruments/top_tdr_creation_ijtag.instrument/top_tdr_creation_tessent_data_mux_w2.icl'
   DataInPort ijtag_select;
   DataInPort ijtag_data_in[1:0];
   DataOutPort data_out[1:0] {
      Source DM1;
      Attribute connection_rule_option = "allowed_no_destination";
   }
   Attribute tessent_use_in_dft_specification = "false";
   Attribute keep_active_during_scan_test = "false";
   Attribute tessent_instrument_type = "mentor::ijtag_node";
   Attribute tessent_signature = "093ecc5023a7fb22101296cbf6d5c149";
   DataMux DM1[1:0] SelectedBy ijtag_select {
      1'b1 : ijtag_data_in[1:0];
   }
}

// instanced as top.top_tdr_creation_tessent_tdr_tdr_inst
Module top_tdr_creation_tessent_tdr_tdr {
   // ICL module read from source on or near line 17 of file '/wv/pszymans_nb/tdr.tshell/results.64/tsdb_outdir/instruments/top_tdr_creation_ijtag.instrument/top_tdr_creation_tessent_tdr_tdr.icl'
   ResetPort ijtag_reset {
      ActivePolarity 0;
   }
   SelectPort ijtag_sel;
   ScanInPort ijtag_si;
   CaptureEnPort ijtag_ce;
   ShiftEnPort ijtag_se;
   UpdateEnPort ijtag_ue;
   TCKPort ijtag_tck;
   ScanOutPort ijtag_so {
      Source tdr[0];
   }
   DataInPort led[3:0] {
      Attribute connection_rule_option = "allowed_no_source";
   }
   DataOutPort mux_sel {
      Source tdr[3];
      Attribute connection_rule_option = "allowed_no_destination";
   }
   DataOutPort fi_en {
      Source tdr[2];
      Attribute connection_rule_option = "allowed_no_destination";
   }
   DataOutPort backward {
      Source tdr[1];
      Attribute connection_rule_option = "allowed_no_destination";
   }
   DataOutPort cnt {
      Source tdr[0];
      Attribute connection_rule_option = "allowed_no_destination";
   }
   ScanInterface client {
      Port ijtag_si;
      Port ijtag_so;
      Port ijtag_sel;
   }
   Attribute keep_active_during_scan_test = "true";
   Attribute tessent_use_in_dft_specification = "false";
   Attribute tessent_instrument_type = "mentor::ijtag_node";
   Attribute tessent_signature = "c1b878d81aa799697b98540887d53e4b";
   ScanRegister tdr[3:0] {
      ScanInSource ijtag_si;
      CaptureSource led[3:0];
      DefaultLoadValue 4'b0000;
      ResetValue 4'b0000;
   }
}
