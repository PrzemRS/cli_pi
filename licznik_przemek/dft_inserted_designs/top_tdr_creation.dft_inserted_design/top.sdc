#--------------------------------------------------------
#
#  Copyright Mentor Graphics Corporation
#  All Rights Reserved
#
#  THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY
#  INFORMATION WHICH IS THE PROPERTY OF MENTOR GRAPHICS
#  CORPORATION OR ITS LICENSORS AND IS SUBJECT
#  TO LICENSE TERMS.
#
#--------------------------------------------------------
#  File created by: Tessent Shell
#          Version: 2018.4-snapshot_2018.10.04_03.00
#       Created on: Thu Oct  4 04:18:21 PDT 2018
#--------------------------------------------------------

#
#  Procs table of content:
#
#    tessent_set_default_variables
#    tessent_constrain_top_mentor_ijtag_non_modal
#    tessent_constrain_top_non_modal
#    tessent_get_cells
#    tessent_get_flops
#    tessent_get_pins
#    tessent_map_to_verilog
#    tessent_remap_vhdl_path_list
#    tessent_get_mem_cells
#    tessent_get_clocks
#    tessent_get_preserve_instances
#    tessent_get_size_only_instances
#    tessent_get_optimize_instances
#
proc tessent_set_default_variables {} {
  global time_unit_multiplier tessent_tck_period tessent_tck_clocks_list tessent_clock_mapping tessent_input_delay tessent_output_delay tessent_hierarchy_separator tessent_path_cache tessent_timing_tool
  #
  # This proc defines the default value of the variables used in instrument timing constraints
  #

  # Time units assumed ns
  set time_unit_multiplier 1.0

  set tessent_tck_period 100.0

  set tessent_tck_clocks_list [list tessent_tck]

  array set tessent_clock_mapping {
    tessent_tck tessent_tck
  }

  set tessent_input_delay [expr 0.25*$tessent_tck_period]

  set tessent_output_delay [expr 0.25*$tessent_tck_period]

  set tessent_hierarchy_separator /

  array set tessent_path_cache {
  }

  switch -glob [file tail [info nameofexecutable]] {
    common_shell_exec {set tessent_timing_tool dc_shell}
    oasys*            {set tessent_timing_tool oasys}
    rc                {set tessent_timing_tool encounter}
    genus             {set tessent_timing_tool genus}
    default           {set tessent_timing_tool pt_shell}
  }
  

}
proc tessent_constrain_top_mentor_ijtag_non_modal {} {  
  #
  # Constraints for instrument mentor::ijtag
  #
  
  global time_unit_multiplier tessent_tck_period tessent_tck_clocks_list
  global tessent_clock_mapping tessent_input_delay tessent_output_delay
  
  if {[sizeof_collection [tessent_get_clocks $tessent_clock_mapping(tessent_tck) -quiet]] == 0} {
    create_clock ijtag_tck -period [expr $tessent_tck_period*$time_unit_multiplier] -name $tessent_clock_mapping(tessent_tck)
  }
  set mapped_tck_clock_list [list]
  foreach tck_clock $tessent_tck_clocks_list {
    lappend mapped_tck_clock_list $tessent_clock_mapping($tck_clock)
  }
  if {[sizeof_collection [tessent_get_clocks $mapped_tck_clock_list -quiet]] > 0} {
    set_clock_groups -asynchronous -group [tessent_get_clocks $mapped_tck_clock_list] -name tessent_tck_clock_group
  }
  set_false_path -from [get_ports ijtag_reset] 
  set_multicycle_path -hold 1 \
      -from [get_ports ijtag_sel] 
  set_input_delay  $tessent_input_delay  -clock $tessent_clock_mapping(tessent_tck) [get_ports "ijtag_ce"] -clock_fall
  set_input_delay  $tessent_input_delay  -clock $tessent_clock_mapping(tessent_tck) [get_ports "ijtag_se"] -clock_fall
  set_input_delay  $tessent_input_delay  -clock $tessent_clock_mapping(tessent_tck) [get_ports "ijtag_ue"]
  set_input_delay  $tessent_input_delay  -clock $tessent_clock_mapping(tessent_tck) [get_ports "ijtag_sel"] -clock_fall
  set_input_delay  $tessent_input_delay  -clock $tessent_clock_mapping(tessent_tck) [get_ports "ijtag_si"] -clock_fall
  set_output_delay $tessent_output_delay -clock $tessent_clock_mapping(tessent_tck) [get_ports "ijtag_so"]
  
}
proc tessent_constrain_top_non_modal {} {
  tessent_constrain_top_mentor_ijtag_non_modal
}
proc tessent_get_cells {path_list args} {
  set ob "{"; set cb "}"
  set actualArgs [list]
  set silent 0
  foreach argValue $args {
    if { $argValue eq "" } { continue }
    if { $argValue eq "-silent" } { set silent 1; continue }
    lappend actualArgs $argValue
  }
  # Quietly try verilog syntax first. If not found, try VHDL remapping
  set cell_col {}
  foreach unmappedPath $path_list {
    set cell_col_tmp [eval get_cells ${ob}[tessent_map_to_verilog $unmappedPath]${cb} $actualArgs -quiet]
    if { [sizeof_collection $cell_col_tmp] == 0 } {
      set cell_col_tmp [eval get_cells ${ob}[tessent_map_to_verilog [tessent_remap_vhdl_path_list $unmappedPath]]${cb} $actualArgs -quiet]
    } 
    append_to_collection cell_col $cell_col_tmp -unique
  }
  if {[sizeof_collection $cell_col] > 0} {
      return $cell_col
  } elseif {!$silent} {
      puts "Error tessent_get_cells: Can't find cell(s) ${path_list}"
  }
  return
 
}
proc tessent_get_flops {path_list args} {
  global tessent_timing_tool
  set ob "{"; set cb "}"
  set cell_col [eval tessent_get_cells ${ob}$path_list${cb} $args]

  switch -- $tessent_timing_tool {
    dc_shell  {set flop_col [filter_collection $cell_col "is_sequential == true"]}
    pt_shell  {set flop_col [filter_collection $cell_col "is_sequential == true"]}
    encounter {set flop_col [filter sequential true $cell_col]}
    genus     {set flop_col [filter_collection $cell_col "is_sequential == true"]}
    default   {set flop_col $cell_col}
  }

  return $flop_col
 
}
proc tessent_get_pins {path_list args} {
  global tessent_timing_tool
  set pin_col {}
  set actualArgs [list]
  set ob "{"; set cb "}"
  foreach argValue $args {
    if { $argValue eq "" } { continue }
    lappend actualArgs $argValue
  }
  foreach path $path_list {
    set pin_sep_index [string last / $path]
    set mapped_cells [eval tessent_get_cells ${ob}[string range $path 0 [expr $pin_sep_index - 1]]${cb} $actualArgs]
    foreach_in_collection mapped_cell $mapped_cells {
      switch $tessent_timing_tool {
        encounter {set mapped_cell_path [get_attribute name $mapped_cell]}
        genus     {set mapped_cell_path [vname $mapped_cell]}
        default   {set mapped_cell_path [get_attribute $mapped_cell full_name]}
      }
      append_to_collection pin_col [get_pins "${mapped_cell_path}[string range $path $pin_sep_index end]" -quiet]
    }
  }
  return $pin_col
  
}
proc tessent_map_to_verilog {path_list} {
  global tessent_hierarchy_separator tessent_custom_mapping_regsub

  set mapped_paths $path_list
  if {[array size tessent_custom_mapping_regsub] > 0} {
    foreach custom_re [array names tessent_custom_mapping_regsub] {
      set mapped_paths [regsub -all $custom_re $mapped_paths $tessent_custom_mapping_regsub($custom_re)]
    }
  }
  array set map_array {
    [ ?
    ] ?
    ) ?
    ( ?
    . ?
    - ?
  }
  if {$tessent_hierarchy_separator ne "/"} {
    set map_array(/) $tessent_hierarchy_separator
  }
  set mapped_paths [string map [array get map_array] $mapped_paths]
  return $mapped_paths
  
}
proc tessent_remap_vhdl_path_list {path_list} {
  global tessent_path_cache
  set remapped_path_list [list]
  foreach path $path_list {
    # Check if we have that full path cached
    if {[info exists tessent_path_cache($path)]} {
      set pathMapped $tessent_path_cache($path)
    } else {
      set pathMapped ""
      set pathUnmapped ""
      foreach sub_path [split $path "/"] {
        if {$pathUnmapped eq ""} {
          set slash ""
        } else {
          set slash "/"
        }
        append pathUnmapped $slash $sub_path
        # The only problematic paths are those with unrolled VHDL generate loops
        #   if the subpath is not a generate loop, we can continue without query'ing
        if {![regexp {[\])]\.} $sub_path]} {
          append pathMapped $slash $sub_path 
          continue
        }
        # Check if we have that hiercarchy cached
        if {[info exists tessent_path_cache($pathUnmapped)]} {
          set pathMapped $tessent_path_cache($pathUnmapped)
          continue
        }
        set pathMapped "$pathMapped/$sub_path"
        # since the sub_path has a closing brace and isn't cached, it might be a loop. Try verilog first
        if {[sizeof_collection [get_cells -quiet [tessent_map_to_verilog $pathMapped]]]} {
          set tessent_path_cache($pathUnmapped) $pathMapped
          continue
        } else {
          # no luck, try for an unrolled VHDL loop from HDLE, otherwise, we just keep going down the hierarchical path 
          #     (since all paths have escaping removed, we might have split in the middle of an escaped instance name)
          set pathMappedTemp [regsub {[\])]\.} $pathMapped {.}]
          if {[sizeof_collection [get_cells -quiet [tessent_map_to_verilog $pathMappedTemp]]]} {
            set tessent_path_cache($pathUnmapped) $pathMapped
            set pathMapped $pathMappedTemp
            continue
          }
        }
      }
    }
    lappend remapped_path_list $pathMapped 
  }
  return $remapped_path_list
 
}
proc tessent_get_mem_cells {inpath} {
  set out_cells [tessent_get_cells $inpath]
  foreach_in_collection cell $out_cells {
    if [get_attribute $cell is_hierarchical] {
      set cell_path [get_attribute $cell full_name]
      if {[sizeof_collection [get_cells -quiet "$cell_path/*"]]>0} {
        set out_cells [add_to_collection $out_cells [tessent_get_mem_cells "$cell_path/*"]]
      }
    }
  }
  return [filter_collection $out_cells "is_sequential==true"]
  
}
proc tessent_get_clocks {patternList args} {
  # Genus does not support more than one <pattern> for 'get_clocks <pattern>'
  set C {}
  foreach p $patternList {
    append_to_collection C [eval get_clocks $p $args] -unique
  }
  return $C
 
}
proc tessent_get_preserve_instances {select} {
  # The 'select' argument identifies a list of instances to be returned.
  # The instances must be preserved in the post-synthesis netlist in order to perform further actions on it:
  #   add_core_instances
  #   scan_insertion       superset of 'add_core_instances' list
  #   icl_extract          superset of 'scan_insertion' list

  set persistent_design_instance_glob_list {
    tessent_persistent_cell_*
  }

  set scan_instrument_instance_list {
  }

  set scan_related_instance_list {
  }

  set tcd_scan_instance_list {
  }

  set non_scan_instance_list {
    top_tdr_creation_tessent_tdr_tdr_inst
  }

  set icl_design_instance_list {
    top_tdr_creation_tessent_data_mux_0_inst
  }

  set keyList [list add_core_instances scan_insertion icl_extract]
  set concatDict {
    add_core_instances { persistent_design_instance_glob_list scan_instrument_instance_list scan_related_instance_list }
    scan_insertion     { tcd_scan_instance_list non_scan_instance_list }
    icl_extract        { icl_design_instance_list }
  }
  set instanceColl {}
  # Nothing to return when 'select' is unknown
  if { [lsearch -exact $keyList $select] < 0 } {
    return $instanceColl
  }
  # Assemble a superset list depending on the 'select' value
  # based on the list of list of variables names to concatenate
  # for each 'select' value.
  foreach {validSelect concatVarnameList} $concatDict {
    foreach concatVarname $concatVarnameList {
      set getCellsArg [expr {[string match *_glob_list $concatVarname] ? "-hierarchical" : ""}]
      foreach instancePattern [set $concatVarname] {
        append_to_collection instanceColl [tessent_get_cells $instancePattern -filter {is_hierarchical==true} $getCellsArg -silent] -unique
      }
    }
    if { $select eq $validSelect } {
      break
    }
  }
  return $instanceColl

}
proc tessent_get_size_only_instances {} {
  set persistent_cell_instance_glob_list {
    tessent_persistent_cell_*
  }

  set instanceColl {}
  foreach instancePattern $persistent_cell_instance_glob_list {
    append_to_collection instanceColl [get_cells $instancePattern -filter {is_hierarchical==false} -hierarchical -quiet] -unique
  }

  return $instanceColl
}
proc tessent_get_optimize_instances {} {
}
