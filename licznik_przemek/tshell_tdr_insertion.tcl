read_verilog -f ../data/file_list
set_current_design top

set_design_level sub_block
check_design_rules

set spec [create_dft_specification]
set interface [add_config_element IjtagNetwork/HostScanInterface(my_interface) -in_wrapper $spec]
set tdr [add_config_element Tdr(tdr) -in_wrapper $interface]

read_config_data -in_wrapper $tdr -from_string {
  DataInPorts {
    connection(3:0) : counter_inst/led[3:0];
    port_naming : led[3:0];
  }
  DataOutPorts {
    connection(3) : counter_inst/fi_en;
    connection(2) : counter_inst/nRst;
    connection(1) : counter_inst/backward;
    connection(0) : counter_inst/cnt;
    port_naming : mux_sel, fi_en, nRst, backward, cnt;
  }
}
report_config_data
process_dft_specification